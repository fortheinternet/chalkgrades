from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timezone
from ably import AblyRest, AblyRealtime

import hashlib
import random
import re
import os

load_dotenv()

allowed_origin = os.getenv("allowed_origin")
supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")
ably_key = os.getenv("ably_key")

access_code_user = os.getenv("user_key")
access_code_work = os.getenv("work_key")

password_salt = os.getenv("password_salt")
password_salt_2 = os.getenv("password_salt_2")

supabase: Client = create_client(supabase_url, supabase_key)
ably = AblyRest(ably_key)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": allowed_origin}})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"],
    storage_uri="memory://",
)

# User Authentication Functions

def userauth(token):
    response = supabase.table('users_data').select('username','user_id').eq('token', token).execute().data

    username = response[0]['username'] if response else None
    user_id = response[0]['user_id'] if response else None

    conditions = [
        (not user_id, 'invalid-token', 'Your token is invalid, as its not associated with a user account.', '401')
    ]

    for condition in conditions:
        if condition[0]: return {'error': condition[1], 'message': condition[2], 'code': condition[3]}

    return {'username': username, 'user_id': user_id}

def workauth(token, work_admin_username, urn, required_role):
    user_data = userauth(token)

    if "error" in user_data:
        return user_data
    else:
        username = user_data.get("username")
        user_id = user_data.get("user_id")

    response = supabase.table('users_data').select('user_id').eq('username', work_admin_username).execute().data
    work_admin_id = response[0]['user_id'] if response else None

    conditions = [
        (not work_admin_id, 'not-exists', 'That resource does not exist.', '404')
    ]

    for condition in conditions:
        if condition[0]: return {'error': condition[1], 'message': condition[2], 'code': condition[3]}

    response = supabase.table('work_data').select('work_id','display','auth').eq('urn', urn).eq('work_admin_id', work_admin_id).execute().data

    work_id = response[0]['work_id'] if response else None
    work_display = response[0]['display'] if response else None
    work_auth = response[0]['auth'] if response else None

    conditions = [
        (not work_id, 'not-exists', 'That resource does not exist.', '404')
    ]

    for condition in conditions:
        if condition[0]: return {'error': condition[1], 'message': condition[2], 'code': condition[3]}
    
    user_role = "none"
    if required_role != "none":
        response = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute().data
        user_role = response[0]['role'] if response else None

        conditions = [
            (required_role == "member" and user_role == None, 'not-exists', 'That resource does not exist.', '404'),
            (required_role == "work_admin" and user_role == None, 'not-exists', 'That resource does not exist.', '404'),
            (required_role == "work_admin" and user_role == "member", 'bad-permissions', 'You have incorrect permissions.', '403')
        ]

        for condition in conditions:
            if condition[0]: return {'error': condition[1], 'message': condition[2], 'code': condition[3]}

    return {
        'username': username,
        'user_id': user_id,
        'work_admin_id': work_admin_id,
        'work_id': work_id,
        'work_display': work_display,
        'user_role': user_role,
        'work_auth': work_auth
    }

# Endpoints

@app.route('/api/logins/logins.json', methods=['POST'])
def handle_logins():
    data = request.get_json()
    required_values = ['username', 'password']

    username = data.get('username')
    password = data.get('password')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    response = supabase.table('users_data').select('auth, token').eq('username', username).execute().data

    conditions = [(not response, 'user-not-exist', 'That user does not exist.', '400')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]

    auth = response[0]['auth'] if response else None
    token = response[0]['token'] if response else None

    salted_password = password_salt + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    conditions = [(sha256_hash != auth, 'bad-password', 'The password provided is incorrect.', '400')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]

    return jsonify({
        'token': token
    })

@app.route('/api/logins/signups.json', methods=['POST'])
def handle_signups():
    data = request.get_json()
    required_values = ['username', 'password', 'password_confirm', 'access_code']

    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    access_code = data.get('access_code')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400
        
    response = supabase.table('users_data').select('username').eq('username', username).execute().data
    usernames = response[0]['username'] if response else None

    system_usernames = ['test', 'admin'] 

    conditions = [
        (password != password_confirm, 'confirmation-no-match', 'The passwords you entered did not match.', '400'),
        (access_code != access_code_user, 'bad-access', 'The access code provided is incorrect.', '400'),
        (username in system_usernames, 'username-system', 'That username is system reserved. Please choose another.', '400'),
        (usernames, 'username-taken', 'The username you chose is already taken. Please choose another.', '400'),
        (not re.match(r'^[A-Za-z\d_ -ÁáÍíŰűÉéŐőÚúÓóÜüÖö]{3,45}$', username), 'invalid-username', 'The username you chose does not meet standard requirements.', '400'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]
        
    salted_password = password_salt + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    token = None
    while not token or supabase.table('users_data').select('username').eq('token', token).execute().data:
        token = random.randint(10**15, (10**16)-1)

    supabase.table("users_data").insert({"username": username, "auth": sha256_hash, "token": token}).execute()

    return jsonify({
        'token': token
    })

        
@app.route('/api/logins/home.json', methods=['POST'])
def handle_home():
    data = request.get_json()
    required_values = ['token']

    token = data.get('token')
    
    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    user_data = userauth(token)

    if "error" in user_data:
        return jsonify({
            'error': user_data.get('error'),
            'message': user_data.get('message')
        }), user_data.get('code')
    else:
        username = user_data.get("username")
        user_id = user_data.get("user_id")

    # Endpoint Logic
    response = supabase.table('members_data').select('work_id').eq('member_id', user_id).execute().data
    workspace_info = []

    for workspace in response:
        work_id = workspace.get('work_id')

        response = supabase.table('work_data').select('work_admin_id','urn','display').eq('work_id', work_id).execute()
        display_name = response.data[0].get('display')
        urn = response.data[0].get('urn')
        work_admin_id = response.data[0].get('work_admin_id')

        work_admin_info = supabase.table('users_data').select('username').eq('user_id', work_admin_id).execute()
        work_admin_username = work_admin_info.data[0].get('username')
        
        workspace_info.append({'display_name': display_name, 'urn': urn, 'work_admin_username': work_admin_username})

    return jsonify({
        'username': username,
        'workspaces': workspace_info
    })
    
@app.route('/api/work/create.json', methods=['POST'])
def handle_work_create():
    data = request.get_json()
    required_values = ['password', 'token', 'urn', 'display', 'access_code']

    password = data.get('password')
    token = data.get('token')
    urn = data.get('urn')
    display = data.get('display')
    access_code = data.get('access_code')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    user_data = userauth(token)

    if "error" in user_data:
        return jsonify({
            'error': user_data.get('error'),
            'message': user_data.get('message')
        }), user_data.get('code')
    else:
        user_id = user_data.get("user_id")

    # Endpoint Logic
    salted_password = password_salt_2 + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    existing_workspaces = supabase.table('work_data').select('urn').eq('work_admin_id', user_id).execute()
    existing_urns = [workspace['urn'].lower() for workspace in existing_workspaces.data] if existing_workspaces.data else []

    conditions = [
        (access_code != access_code_work, 'bad-access', 'The access code provided is incorrect.', '400'),
        (urn.lower() in existing_urns, 'work-already-exists', 'That workspace resource (aka slug/urn) already exists for this user.', '400'),
        (not re.match(r'^[A-Za-z\d_-]{3,20}$', urn), 'invalid-work-resource', 'That workspace resource does not meet standard requirements.', '400'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]
        
    supabase.table("work_data").insert({"work_admin_id": user_id, "auth": sha256_hash, "urn": urn, "display": display}).execute()

    work_id = supabase.table('work_data').select('work_id').eq('work_admin_id', user_id).eq('urn', urn).execute().data[0]['work_id']
    supabase.table("members_data").insert({"member_id": user_id, "work_id": work_id, "role": "work_admin"}).execute()

    return jsonify({
        'success': True
    }), 200

@app.route('/api/work/<string:work_admin_username>/<string:urn>/join.json', methods=['POST']) # member_join
async def handle_work_join(work_admin_username, urn):
    data = request.get_json()
    required_values = ['password','token']

    password = data.get('password')
    token = data.get('token')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "none")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        username = work_data.get("username")
        user_id = work_data.get("user_id")
        work_id = work_data.get("work_id")
        work_auth = work_data.get("work_auth")

    # Endpoint Logic
    salted_password = password_salt_2 + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    conditions = [
        (sha256_hash != work_auth, 'bad-password', 'Your password is incorrect.', '400')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]
     
    existing_member = supabase.table('members_data').select('member_id').eq('member_id', user_id).eq('work_id', work_id).execute().data

    conditions = [
        (existing_member, 'already-member', 'You are already a member of that workspace!', '400')
    ]
    
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]

    # Realtime Endpoint Logic
    existing_row = supabase.table('realtime_pages').select('*').eq('work_id', work_id).execute().data

    if existing_row:
        realtime_access = existing_row[0]['access']
    else:
        realtime_access = None
        while not realtime_access or supabase.table('realtime_pages').select('access').eq('access', realtime_access).execute().data:
            realtime_access = random.randint(10**15, (10**16)-1)
    
        supabase.table('realtime_pages').insert({'work_id': work_id, 'access': realtime_access}).execute()
    
    supabase.table("members_data").insert({"member_id": user_id, "work_id": work_id, "role": "member"}).execute()
    
    channel = ably.channels.get(realtime_access)
    channel_message = {
        "username": username,
        "selected_role": "member",
        "selected_user_id": user_id
    }

    await channel.publish('member_join', channel_message)
    return jsonify({
        'success': True
    }), 200

@app.route('/api/work/<string:work_admin_username>/<string:urn>/home.json', methods=['POST'])
def handle_work_home(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token']

    token = data.get('token')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "member")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        username = work_data.get("username")
        user_id = work_data.get("user_id")
        work_id = work_data.get("work_id")
        work_display = work_data.get("work_display")
        user_role = work_data.get("user_role")

    # Endpoint Logic
    members_data = supabase.table('members_data').select('member_id', 'role').eq('work_id', work_id).execute().data

    members_response = []
    for member_data in members_data:
        member_id = member_data.get('member_id')
        member_role = member_data.get('role')

        response = supabase.table('users_data').select('username').eq('user_id', member_id).execute()
        member_username = response.data[0].get('username')

        members_response.append({
            'username': member_username,
            'selected_role': member_role,
            'selected_user_id': member_id
        })

    if user_role == "member":
        exams_data = supabase.table("exams_data").select('exam_id').eq('work_id', work_id).eq('visibility', "public").execute()
        exam_ids = exams_data.data
    
    elif user_role == "work_admin":
        exams_data = supabase.table("exams_data").select('exam_id').eq('work_id', work_id).execute()
        exam_ids = exams_data.data
            
    exams = []
    for exam in exam_ids:
        exam_id = exam.get('exam_id')

        response = supabase.table('exams_data').select('display_name','visibility').eq('exam_id', exam_id).execute()

        exam_name = response.data[0]['display_name'] if response.data else None
        visibility = response.data[0]['visibility'] if response.data else None

        exams.append({
            'display_name': exam_name,
            'visibility': visibility,
            'exam_id': exam_id
        })

    # Realtime Endpoint Logic
    existing_row = supabase.table('realtime_pages').select('*').eq('work_id', work_id).execute().data

    if existing_row:
        realtime_access = existing_row[0]['access']
    else:
        realtime_access = None
        while not realtime_access or supabase.table('realtime_pages').select('access').eq('access', realtime_access).execute().data:
            realtime_access = random.randint(10**15, (10**16)-1)
    
        supabase.table('realtime_pages').insert({'work_id': work_id, 'access': realtime_access}).execute()

    return jsonify({
        'display': work_display,
        'username': username,
        'user_id': user_id,
        'user_role': user_role,
        'members': members_response,
        'exams': exams,
        'realtime_access': realtime_access
    })

@app.route('/api/work/<string:work_admin_username>/<string:urn>/home_realtime.json', methods=['POST'])
async def handle_work_ably_token(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token']

    token = data.get('token')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "none")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        work_id = work_data.get("work_id")

    # Realtime Endpoint Logic
    existing_row = supabase.table('realtime_pages').select('*').eq('work_id', work_id).execute().data

    if existing_row:
        realtime_access = existing_row[0]['access']
    else:
        realtime_access = None
        while not realtime_access or supabase.table('realtime_pages').select('access').eq('access', realtime_access).execute().data:
            realtime_access = random.randint(10**15, (10**16)-1)
    
        supabase.table('realtime_pages').insert({'work_id': work_id, 'access': realtime_access}).execute()

    token_details = await ably.auth.create_token_request({'ttl': 3600000, 'capability': {realtime_access: ['subscribe']}})
    token_details_dict = token_details.to_dict()

    return jsonify({
        'ably_token': token_details_dict
    })

@app.route('/api/work/<string:work_admin_username>/<string:urn>/settings.json', methods=['POST'])
async def handle_work_settings(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token', 'value', 'action']

    token = data.get('token')
    value = data.get('value')
    action = data.get('action')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "member")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        user_id = work_data.get("user_id")
        work_admin_id = work_data.get("work_admin_id")
        work_id = work_data.get("work_id")
        user_role = work_data.get("user_role")

    # Realtime Endpoint Logic
    existing_row = supabase.table('realtime_pages').select('*').eq('work_id', work_id).execute().data

    if existing_row:
        realtime_access = existing_row[0]['access']
    else:
        realtime_access = None
        while not realtime_access or supabase.table('realtime_pages').select('access').eq('access', realtime_access).execute().data:
            realtime_access = random.randint(10**15, (10**16)-1)
    
        supabase.table('realtime_pages').insert({'work_id': work_id, 'access': realtime_access}).execute()

    # Settings
        
    if action == "display": # work_display
        conditions = [(user_role != "work_admin", 'bad-permissions', 'You have incorrect permissions.')]
        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
        supabase.table('work_data').update({'display': value}).eq('work_id', work_id).execute()
        return jsonify({'success': True})
    
    elif action == "urn":
        existing_workspaces = supabase.table('work_data').select('urn').eq('work_admin_id', work_admin_id).execute()
        existing_urns = [workspace['urn'].lower() for workspace in existing_workspaces.data] if existing_workspaces.data else []

        conditions = [
            (value.lower() in existing_urns, 'work-already-exists', 'That workspace resource (aka slug/urn) already exists for this user.', '400'),
            (not re.match(r'^[A-Za-z\d_-]{3,20}$', value), 'invalid-work-resource', 'That workspace resource does not meet standard requirements.', '400'),
            (user_role != "work_admin", 'bad-permissions', 'You have incorrect permissions.', '400')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

        supabase.table('work_data').update({'urn': value}).eq('work_id', work_id).execute()
        return jsonify({'success': True})
    
    elif action == "leave": # member_leave
        conditions = [(user_role != "member", 'bad-permissions', 'You have incorrect permissions.', '400')]
        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
        supabase.table('members_data').delete().eq('work_id', work_id).eq('member_id', user_id).execute()

        channel = ably.channels.get(realtime_access)
        channel_message = {
            "selected_user_id": user_id
        }
        await channel.publish('member_leave', channel_message)

        return jsonify({'success': True})
    
    elif action == "delete": # work_detete
        return jsonify({'message': 'This feature is not implemented. You can help expand the functionality of the project by opening a pull request - github.com/fortheinternet/chalkgrades/'})
    
    elif action == "remove_member": # member_remove
        exams_data = supabase.table('exams_data').select('exam_id').eq('work_id', work_id).execute().data

        conditions = [(user_role != "work_admin", 'bad-permissions', 'You have incorrect permissions.', '400')]
        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

        for exam in exams_data:
            exam_id = exam.get('exam_id')
            supabase.table('sessions_data').delete().eq('exam_id', exam_id).eq('user_id', value).execute()
        
        supabase.table('members_data').delete().eq('work_id', work_id).eq('member_id', value).execute()

        channel = ably.channels.get(realtime_access)
        channel_message = {
            "selected_user_id": value
        }
        await channel.publish('member_remove', channel_message)

        return jsonify({'success': True})
    
    else:
        return jsonify({'error': 'You entered something incorrectly.'}), 400

@app.route('/api/exams/<string:work_admin_username>/<string:urn>/create.json', methods=['POST'])
def handle_exams_create(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token', 'exam_name']

    token = data.get("token")
    exam_name = data.get("exam_name")

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "work_admin")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        work_id = work_data.get("work_id")
    
    # Endpoint Logic
    supabase.table('exams_data').insert({"display_name": exam_name, "work_id": work_id, "visibility": "private"}).execute()
    return jsonify({'success': True})

@app.route('/api/exams/<string:work_admin_username>/<string:urn>/settings.json', methods=['POST'])
def handle_exam_settings(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token', 'value', 'action']

    token = data.get('token')
    exam_id = data.get('value')
    action = data.get('action')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "work_admin")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        work_id = work_data.get("work_id")

    # Endpoint Logic
    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('status', "active").eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (exam_work_id != work_id, 'not-exists', 'That resource does not exist.', '404'),
        (session_id, 'has-active-sessions', 'This exam has one or more active sessions, so its settings cannot be modified.', '400')
    ]

    for condition in conditions: 
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]

    # Settings

    exam_data = supabase.table('exams_data').select('visibility').eq('exam_id', exam_id).execute()
    visibility = exam_data.data[0]['visibility'] if exam_data.data else None

    if action == "remove":
        supabase.table('options_data').delete().eq('exam_id', exam_id).execute()
        supabase.table('questions_data').delete().eq('exam_id', exam_id).execute()
        supabase.table('exams_data').delete().eq('exam_id', exam_id).eq('work_id', work_id).execute()

        return jsonify({'success': True})
    
    elif action == "toggle":        
        if visibility == "private":
            supabase.table('exams_data').update({'visibility': 'public'}).eq('exam_id', exam_id).eq('work_id', work_id).execute()
        else:
            supabase.table('exams_data').update({'visibility': 'private'}).eq('exam_id', exam_id).eq('work_id', work_id).execute()

        return jsonify({'success': True})
    else:
        return jsonify({'error': 'You entered something incorrectly.'}), 400

@app.route('/api/exams/<string:work_admin_username>/<string:urn>/build.json', methods=['POST'])
def handle_exam_build(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token', 'value', 'questions'] # TODO: add action in future if used

    token = data.get('token')
    exam_id = data.get('value')
    action = data.get('action')
    questions = data.get('questions', [])

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "work_admin")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        work_id = work_data.get("work_id")

    # Endpoint Logic
    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (exam_work_id != work_id, 'not-exists', 'That resource does not exist.', '404'),
        (session_id, 'has-any-sessions', 'This exam has one or more sessions, so its questions cannot be modified.', '400')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]
    
    # Deletes existing data!
    supabase.table('options_data').delete().eq('exam_id', exam_id).execute()
    supabase.table('questions_data').delete().eq('exam_id', exam_id).execute()

    for question_data in questions:
        question_order = question_data.get('order')
        question_content = question_data.get('content')
        question_description = question_data.get('description')
        question_type = question_data.get('type')

        supabase.table('questions_data').insert({'exam_id': exam_id, 'question_order': question_order, 'content': question_content, 'description': question_description, "type": question_type}).execute()

        response = supabase.table('questions_data').select('question_id').eq('exam_id', exam_id).eq('question_order', question_order).execute()
        question_id = response.data[0]['question_id'] if response.data else None

        if question_type in ['multi', 'select']:
            options = question_data.get('options', [])

            orders = []
            for option_data in options:
                option_order = option_data.get('order')

                conditions = [
                    (option_order in orders, 'syntax-fatal-orderdupe', 'One or more of the orders are duplicated. This error should not occur naturally using the website, please open a GitHub issue.', '400')
                ]

                for condition in conditions:
                    if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]

                orders.append(option_order)
            
            for option_content in options:
                content = option_content.get('content', '')
                order = option_content.get('order', '')

                supabase.table('options_data').insert({'question_id': question_id, 'content': content, 'exam_id': exam_id, 'option_order': order}).execute()

    return jsonify({'success': True})

@app.route('/api/exams/<string:work_admin_username>/<string:urn>/home.json', methods=['POST'])
def handle_exam_home(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token', 'value']

    token = data.get('token')
    exam_id = data.get('value')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "member")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        username = work_data.get("username")
        work_id = work_data.get("work_id")
        work_display = work_data.get("work_display")
        user_role = work_data.get("user_role")

    # Endpoint Logic
    exam_work_data = supabase.table('exams_data').select('work_id', 'visibility', 'display_name').eq('exam_id', exam_id).execute()

    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None
    exam_visibility = exam_work_data.data[0]['visibility'] if exam_work_data.data else None
    exam_display = exam_work_data.data[0]['display_name'] if exam_work_data.data else None

    conditions = [
        (exam_work_id != work_id, 'not-exists', 'That resource does not exist.', 404),
        (user_role != "work_admin" and exam_visibility != "public", 'not-exists', 'That resource does not exist.', 404)
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]

    questions_data = supabase.table('questions_data').select('question_order', 'content', 'description', 'type', 'question_id').eq('exam_id', exam_id).execute().data

    formatted_questions = []
    for question in questions_data:
        question_id = question.get('question_id')
        
        options_data = supabase.table('options_data').select('content', 'option_order').eq('question_id', question_id).execute().data
        formatted_options = [{"content": option['content'], "option_order": option['option_order']} for option in options_data]
        
        formatted_question = {"order": question.get('question_order'), "content": question.get('content'), "description": question.get('description'), "type": question.get('type'), "options": formatted_options}
        formatted_questions.append(formatted_question)

    sessions_data = session_data = supabase.table('sessions_data').select('session_id', 'status', 'user_id').eq('exam_id', exam_id).execute().data

    student_sessions = []
    for session_data in sessions_data:
        student_id = session_data.get('user_id')

        student_data = supabase.table('users_data').select('username').eq('user_id', student_id).execute()
        student_username = student_data.data[0]['username'] if student_data.data else None

        formatted_session = {"status": session_data.get('status'), "username": student_username, "session_id": session_data.get('session_id')}
        student_sessions.append(formatted_session)

    if user_role == "member":    
        response_data = {
            'work_display': work_display,
            'exam_display': exam_display,
            'visibility': exam_visibility,
            'user_role': user_role,
            'username': username
        }
    elif user_role == "work_admin":
        response_data = {
            'work_display': work_display,
            'exam_display': exam_display,
            'visibility': exam_visibility,
            'user_role': user_role,
            'username': username,
            'questions': formatted_questions,
            'sessions': student_sessions
        }

    # Realtime Endpoint Logic
    existing_row = supabase.table('realtime_pages').select('*').eq('exam_id', exam_id).execute().data

    if existing_row:
        realtime_access = existing_row[0]['access']
    else:
        realtime_access = None
        while not realtime_access or supabase.table('realtime_pages').select('access').eq('access', realtime_access).execute().data:
            realtime_access = random.randint(10**15, (10**16)-1)
    
        supabase.table('realtime_pages').insert({'work_id': work_id, 'access': realtime_access}).execute()


    supabase.table('realtime_pages').insert({'exam_id': exam_id, 'access': realtime_access}).execute()

    return jsonify(response_data)

@app.route('/api/exams/<string:work_admin_username>/<string:urn>/start.json', methods=['POST'])
def handle_exam_start(work_admin_username, urn):
    data = request.get_json()
    required_values = ['token', 'value']

    token = data.get('token')
    exam_id = data.get('value')

    for value in required_values:
        if data.get(value) is None:
            return jsonify({'error': 'syntax-fatal-formatting', 'message': 'Your request is malformed, meaning one of the values are missing. This error should not occur naturally using the website, please open a GitHub issue.'}), 400

    # Authentication
    work_data = workauth(token, work_admin_username, urn, "MIN_PERM_LVL")

    if "error" in work_data:
        return jsonify({
            'error': work_data.get('error'),
            'message': work_data.get('message')
        }), work_data.get('code')
    else:
        user_id = work_data.get("user_id")
        work_id = work_data.get("work_id")

    # Endpoint Logic
    exam_work_data = supabase.table('exams_data').select('work_id', 'visibility').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None
    exam_visibility = exam_work_data.data[0]['visibility'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('user_id', user_id).eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (exam_work_id != work_id, 'not-exists', 'That resource does not exist.', '404'),
        (exam_visibility != "public", 'not-exists', 'That resource does not exist.', '404'),
        (session_id, 'already-started', 'You already started this exam!', '400')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]}), condition[3]

    supabase.table('sessions_data').insert({'user_id': user_id, 'exam_id': exam_id, 'status': "active"}).execute() # inserts the session as active
    questions_data = supabase.table('questions_data').select('question_order', 'content', 'description', 'type', 'question_id').eq('exam_id', exam_id).execute().data

    formatted_questions = []
    for question in questions_data:
        question_id = question.get('question_id')
        
        options_data = supabase.table('options_data').select('content', 'option_order').eq('question_id', question_id).execute().data
        formatted_options = [{"content": option['content'], "option_order": option['option_order']} for option in options_data]
        
        formatted_question = {"order": question.get('question_order'), "content": question.get('content'), "description": question.get('description'), "type": question.get('type'), "options": formatted_options}
        formatted_questions.append(formatted_question)

    return jsonify({'questions': formatted_questions})