from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
import hashlib
import random
import re
import os
from supabase import create_client, Client
from datetime import datetime, timezone
from ably import AblyRest, AblyRealtime

load_dotenv()

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")
ably_key = os.getenv("ably_key")

accesskey_user = os.getenv("user_key")
accesskey_work = os.getenv("work_key")

password_salt = os.getenv("password_salt")
password_salt_2 = os.getenv("password_salt_2")

supabase: Client = create_client(supabase_url, supabase_key)
ably = AblyRest(ably_key)

app = Flask(__name__)

# Static Files

@app.errorhandler(404)
def page_not_found(error):
    return send_from_directory('src/pages', '404.html'), 404

@app.route('/')
def serve_root():
    return send_from_directory('src/pages', 'landing.html')

@app.route('/login')
def serve_login():
    return send_from_directory('src/pages', 'login.html')

@app.route('/home')
def serve_home():
    return send_from_directory('src/pages', 'home.html')

@app.route('/<string:creator_username>/<string:url>')
def serve_workspace_home(creator_username, url):
    return send_from_directory('src/pages', 'work_home.html')

@app.route('/<string:creator_username>/<string:url>/<string:id>')
def serve_id_home(creator_username, url, id):
    return send_from_directory('src/pages', 'exam_home.html')

@app.route('/src/styles/<path:filename>')
def serve_styles(filename):
    return send_from_directory('src/styles', filename)

@app.route('/src/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('src/js', filename)

@app.route('/src/output.css')
def serve_output():
    return send_from_directory('src', 'output.css')

@app.route('/src/favicon.png')
def serve_favicon():
    return send_from_directory('src', 'favicon.png')

# User Authentication Functions

def userauth(token):
    response = supabase.table('users_data').select('username','user_id').eq('token', token).execute().data

    username = response[0]['username'] if response else None
    user_id = response[0]['user_id'] if response else None

    conditions = [
        (not user_id, 'mal-25-1', 'Your token is invalid, as its not associated with a user account.')
    ]

    for condition in conditions:
        if condition[0]: return {'error': condition[1], 'message': condition[2]}

    return {'username': username, 'user_id': user_id}

def workauth(token, creator_username, url, required_role):
    user_data = userauth(token)

    if "error" in user_data:
        return user_data
    else:
        username = user_data.get("username")
        user_id = user_data.get("user_id")

    response = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = response[0]['user_id'] if response else None

    conditions = [
        (not creator_id, 'w-mal-4000', 'That workspace does not exist.')
    ]

    for condition in conditions:
        if condition[0]: return {'error': condition[1], 'message': condition[2]}

    response = supabase.table('work_data').select('work_id','display','auth').eq('url', url).eq('creator_id', creator_id).execute().data

    work_id = response[0]['work_id'] if response else None
    work_display = response[0]['display'] if response else None
    work_auth = response[0]['auth'] if response else None

    conditions = [
        (not work_id, 'w-mal-4000', 'That workspace does not exist.')
    ]

    for condition in conditions:
        if condition[0]: return {'error': condition[1], 'message': condition[2]}
    
    user_role = "none"
    if required_role != "none":
        response = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute().data
        user_role = response[0]['role'] if response else None

        conditions = [
            (required_role == "member" and user_role == None, 'w-mal-4000', 'That workspace does not exist.'),
            (required_role == "work_admin" and user_role == None, 'w-mal-4000', 'That workspace does not exist.'),
            (required_role == "work_admin" and user_role == "member", 'w-mal-403', 'Work: You have incorrect permissions.')
        ]

        for condition in conditions:
            if condition[0]: return {'error': condition[1], 'message': condition[2]}

    return {
        'username': username,
        'user_id': user_id,
        'creator_id': creator_id,
        'work_id': work_id,
        'work_display': work_display,
        'user_role': user_role,
        'work_auth': work_auth
    }

# Endpoints

@app.route('/api/logins/logins.json', methods=['POST'])
def handle_logins():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    response = supabase.table('users_data').select('auth, token').eq('username', username).execute().data

    conditions = [(not response, 'l-fatal-20', 'Login: User not found')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    auth = response[0]['auth'] if response else None
    token = response[0]['token'] if response else None

    salted_password = password_salt + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    conditions = [(sha256_hash != auth, 'l-mal-10', 'Login: Passwords dont match')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    return jsonify({
        'token': token
    })

@app.route('/api/logins/signups.json', methods=['POST'])
def handle_signups():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    accesskey = data.get('accesskey')

    response = supabase.table('users_data').select('username').eq('username', username).execute().data
    usernames = response[0]['username'] if response else None

    conditions = [
        (password != password_confirm, 's-mal-10', 'Signup: Passwords dont match'),
        (accesskey != accesskey_user, 's-mal-15', 'Signup: Bad access key'),
        (usernames, 's-mal-20', 'Signup: Username already taken'),
        (not re.match(r'^[A-Za-z\d_ -ÁáÍíŰűÉéŐőÚúÓóÜüÖö]{3,45}$', username), 's-mal-50', 'Signup: Invalid username'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
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
    token = data.get('token')

    # Authentication
    user_data = userauth(token)

    if "error" in user_data:
        return jsonify(user_data)
    else:
        username = user_data.get("username")
        user_id = user_data.get("user_id")

    # Endpoint Logic
    response = supabase.table('members_data').select('work_id').eq('member_id', user_id).execute().data
    workspace_info = []

    for workspace in response:
        work_id = workspace.get('work_id')

        response = supabase.table('work_data').select('creator_id','url','display').eq('work_id', work_id).execute()
        display_name = response.data[0].get('display')
        url = response.data[0].get('url')
        creator_id = response.data[0].get('creator_id')

        creator_info = supabase.table('users_data').select('username').eq('user_id', creator_id).execute()
        creator_username = creator_info.data[0].get('username')
        
        workspace_info.append({'display_name': display_name, 'url': url, 'creator_username': creator_username})

    return jsonify({
        'username': username,
        'workspaces': workspace_info
    })
    
@app.route('/api/work/create.json', methods=['POST'])
def handle_work_create():
    data = request.get_json()

    password = data.get('password')
    token = data.get('token')
    url = data.get('url')
    display = data.get('display')
    accesskey = data.get('accesskey')

    # Authentication
    user_data = userauth(token)

    if "error" in user_data:
        return jsonify(user_data)
    else:
        user_id = user_data.get("user_id")

    # Endpoint Logic
    salted_password = password_salt_2 + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    existing_workspaces = supabase.table('work_data').select('url').eq('creator_id', user_id).execute()
    existing_urls = [workspace['url'].lower() for workspace in existing_workspaces.data] if existing_workspaces.data else []

    conditions = [
        (accesskey != accesskey_work, 'w-mal-15', 'Work: Bad access key'),
        (url.lower() in existing_urls, 'w-mal-30', 'Work: url already exists for this user'),
        (not re.match(r'^[A-Za-z\d_-]{3,20}$', url), 'w-mal-31', 'Work: Invalid URL'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
    supabase.table("work_data").insert({"creator_id": user_id, "auth": sha256_hash, "url": url, "display": display}).execute()

    work_id = supabase.table('work_data').select('work_id').eq('creator_id', user_id).eq('url', url).execute().data[0]['work_id']
    supabase.table("members_data").insert({"member_id": user_id, "work_id": work_id, "role": "work_admin"}).execute()

    return jsonify({'success': True})

@app.route('/api/work/<string:creator_username>/<string:url>/join.json', methods=['POST']) # member_join
async def handle_work_join(creator_username, url):
    data = request.get_json()

    password = data.get('password')
    token = data.get('token')

    # Authentication
    work_data = workauth(token, creator_username, url, "none")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
    else:
        username = work_data.get("username")
        user_id = work_data.get("user_id")
        work_id = work_data.get("work_id")
        work_auth = work_data.get("work_auth")

    # Endpoint Logic
    salted_password = password_salt_2 + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    conditions = [(sha256_hash != work_auth, 'w-mal-55', 'Work: Invalid access credentials')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
     
    existing_member = supabase.table('members_data').select('member_id').eq('member_id', user_id).eq('work_id', work_id).execute().data

    conditions = [(existing_member, 'w-mal-60', 'Work: User is already a member of this workspace')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

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
    return jsonify({'success': True})

@app.route('/api/work/<string:creator_username>/<string:url>/home.json', methods=['POST'])
def handle_work_home(creator_username, url):
    data = request.get_json()
    token = data.get('token')

    # Authentication
    work_data = workauth(token, creator_username, url, "member")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
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

@app.route('/api/work/<string:creator_username>/<string:url>/home_realtime.json', methods=['POST'])
async def handle_work_ably_token(creator_username, url):
    data = request.get_json()
    token = data.get('token')

    # Authentication
    work_data = workauth(token, creator_username, url, "none")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
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

@app.route('/api/work/<string:creator_username>/<string:url>/settings.json', methods=['POST'])
async def handle_work_settings(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    value = data.get('value')
    action = data.get('action')

    # Authentication
    work_data = workauth(token, creator_username, url, "member")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
    else:
        user_id = work_data.get("user_id")
        creator_id = work_data.get("creator_id")
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
    
    if action == "display": # work_display
        conditions = [(user_role != "work_admin", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')]
        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
        supabase.table('work_data').update({'display': value}).eq('work_id', work_id).execute()
        return jsonify({'success': True})
    
    elif action == "url":
        existing_workspaces = supabase.table('work_data').select('url').eq('creator_id', creator_id).execute()
        existing_urls = [workspace['url'].lower() for workspace in existing_workspaces.data] if existing_workspaces.data else []

        conditions = [
            (value.lower() in existing_urls, 'w-mal-30-11', 'Work: url already exists for this user'),
            (not re.match(r'^[A-Za-z_]{1,20}$', value), 'w-mal-50', 'Work: Invalid url you silly'),
            (user_role != "work_admin", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

        supabase.table('work_data').update({'url': value}).eq('work_id', work_id).execute()
        return jsonify({'success': True})
    
    elif action == "leave": # member_leave
        conditions = [(user_role != "member", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')]
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
        return jsonify({'wip': 'Deleting workspaces is not finished yet, please contact your administrator.'})
    
    elif action == "remove_member": # member_remove
        exams_data = supabase.table('exams_data').select('exam_id').eq('work_id', work_id).execute().data

        conditions = [(user_role != "work_admin", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')]
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
        return jsonify({'error': 'You entered something incorrectly.'})

@app.route('/api/exams/<string:creator_username>/<string:url>/create.json', methods=['POST'])
def handle_exams_create(creator_username, url):
    data = request.get_json()

    token = data.get("token")
    exam_name = data.get("exam_name")

    # Authentication
    work_data = workauth(token, creator_username, url, "member")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
    else:
        work_id = work_data.get("work_id")
    
    # Endpoint Logic
    supabase.table('exams_data').insert({"display_name": exam_name, "work_id": work_id, "visibility": "private"}).execute()
    return jsonify({'success': True})

@app.route('/api/exams/<string:creator_username>/<string:url>/settings.json', methods=['POST'])
def handle_exam_settings(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    exam_id = data.get('value')
    action = data.get('action')

    # Authentication
    work_data = workauth(token, creator_username, url, "work_admin")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
    else:
        work_id = work_data.get("work_id")

    # Endpoint Logic
    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('status', "active").eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (session_id, 'e-mal-26-61', 'Exams: This exam has one or more active sessions so it cant be accessed traditionally')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    if action == "remove":
        supabase.table('options_data').delete().eq('exam_id', exam_id).execute()
        supabase.table('questions_data').delete().eq('exam_id', exam_id).execute()
        supabase.table('exams_data').delete().eq('exam_id', exam_id).eq('work_id', work_id).execute()

        return jsonify({'success': True})
    
    elif action == "toggle":
        supabase.table('exams_data').update({'visibility': 'public'}).eq('exam_id', exam_id).eq('work_id', work_id).execute()
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'You entered something incorrectly.'})

@app.route('/api/exams/<string:creator_username>/<string:url>/build.json', methods=['POST'])
def handle_exam_build(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    exam_id = data.get('exam_id')
    action = data.get('action')
    questions = data.get('questions', [])

    # Authentication
    work_data = workauth(token, creator_username, url, "work_admin")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
    else:
        work_id = work_data.get("work_id")

    # Endpoint Logic
    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('status', "active").eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (session_id, 'e-mal-26-61', 'Exams: This exam has one or more active sessions so it cant be accessed traditionally')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
    supabase.table('options_data').delete().eq('exam_id', exam_id).execute()
    supabase.table('questions_data').delete().eq('exam_id', exam_id).execute()

    for question_data in questions:
        question_order = question_data.get('order')
        question_content = question_data.get('content')
        question_description = question_data.get('description')
        question_type = question_data.get('type')

        supabase.table('questions_data').insert({'exam_id': exam_id, 'question_order': question_order, 'content': question_content, 'description': question_description, "type": question_type}).execute()

        question_current_data = supabase.table('questions_data').select('question_id').eq('exam_id', exam_id).eq('question_order', question_order).execute()
        question_id = question_current_data.data[0]['question_id'] if question_current_data.data else None

        if question_type in ['multi', 'select']:
            options = question_data.get('options', [])

            orders = []
            for option_data in options:
                option_order = option_data.get('order')

                existing_data = supabase.table('options_data').select('option_order').eq('exam_id', exam_id).eq('question_id', question_id).execute().data
                existing_orders = [item['option_order'] for item in existing_data]

                conditions = [
                    (option_order in existing_orders, 'e-mal-99-00', 'Exams: One or more of the orders are duplicated.'),
                    (option_order in orders, 'e-mal-99-11', 'Exams: One or more of the orders are duplicated.')
                ]

                for condition in conditions:
                    if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

                orders.append(option_order)
            
            for option_content in options:
                content = option_content.get('content', '')
                order = option_content.get('order', '')

                supabase.table('options_data').insert({'question_id': question_id, 'content': content, 'exam_id': exam_id, 'option_order': order}).execute()

    return jsonify({'success': True})

@app.route('/api/exams/<string:creator_username>/<string:url>/home.json', methods=['POST'])
def handle_exam_home(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    exam_id = data.get('exam_id')

    # Authentication
    work_data = workauth(token, creator_username, url, "member")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
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
        (not user_role, 'e-mal-20', 'Exams: You do not have the proper permissions to change exam configurations.'),
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (user_role != "work_admin" and exam_visibility != "public", 'exam_not_public', 'You are only allowed to view public exams, not private ones.')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

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

@app.route('/api/exams/<string:creator_username>/<string:url>/start.json', methods=['POST'])
def handle_exam_start(creator_username, url):
    data = request.get_json()
    
    token = data.get('token')
    exam_id = data.get('value')

    # Authentication
    work_data = workauth(token, creator_username, url, "MIN_PERM_LVL")

    if "error" in work_data:
        error = work_data.get("error")
        responses = ["mal-25-1", "w-mal-403", "w-mal-4000"]

        if error in responses:
            return jsonify(work_data)

        return jsonify({"message":"you encountered a rare error! ^-^ you should contact a maintainer :3 read.cv/thelocaltemp"}), 500
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
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (exam_visibility != "public", 'e-mal-22-01', 'Exams: You are only allowed to start public exams.'),
        (session_id, 'e-mal-26-60', 'Exams: You already started this exam!')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

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