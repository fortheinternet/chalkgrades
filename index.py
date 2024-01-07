from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
import hashlib
import random
import re
import os
from supabase import create_client, Client
from datetime import datetime, timezone

load_dotenv()

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")

supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return send_from_directory('src/pages', '404.html'), 404

# these serve sites
@app.route('/')
def serve_root():
    return send_from_directory('src/pages', 'landing.html')

@app.route('/login')
def serve_login():
    return send_from_directory('src/pages', 'login.html')

@app.route('/home')
def serve_home():
    return send_from_directory('src/pages', 'home.html')

# these serve files
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

# Logins

@app.route('/api/logins/logins.json', methods=['POST'])
def handle_logins():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    result = supabase.table('users_data').select('auth, token').eq('username', username).execute().data

    # ROUND 1 OF CONDITIONS
    conditions = [(not result, 'l-fatal-20', 'Login: User not found')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    auth = result[0]['auth'] if result else None
    token = result[0]['token'] if result else None

    salted_password = 'e10reGEXspace' + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    # ROUND 2 OF CONDITIONS
    conditions = [(sha256_hash != auth, 'l-mal-10', 'Login: Passwords dont match')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    return jsonify({'token': token})


@app.route('/api/logins/signups.json', methods=['POST'])
def handle_signups():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    accesskey = data.get('accesskey')

    response = supabase.table('users_data').select('username').execute()
    all_usernames = [user['username'] for user in response.data] if response.data else []

    conditions = [
        (password != password_confirm, 's-mal-10', 'Signup: Passwords dont match'),
        (accesskey != "77000", 's-mal-15', 'Signup: Bad access key'),
        (username.lower() in map(str.lower, all_usernames), 's-mal-20', 'Signup: Username already taken'),
        (not re.match(r'^[A-Za-z\d_]{3,16}$', username), 's-mal-50', 'Signup: Invalid username'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
    salted_password = 'e10reGEXspace' + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    token = None
    while not token or supabase.table('users_data').select('username').eq('token', token).execute().data:
        token = random.randint(10**15, (10**16)-1)

    supabase.table("users_data").insert({"username": username, "auth": sha256_hash, "token": token}).execute()

    return jsonify({'token': token})

        
@app.route('/api/logins/home.json', methods=['POST'])
def handle_home():
    data = request.get_json()
    token = data.get('token')

    result = supabase.table('users_data').select('username','user_id').eq('token', token).execute().data
    username = result[0]['username'] if result else None
    user_id = result[0]['user_id'] if result else None

    # conditions checker
    conditions = [(not username, 'h-mal-10', 'Home: Invalid token')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_data = supabase.table('members_data').select('work_id').eq('member_id', user_id).execute().data
    
    workspace_info = []
    for workspace_entry in work_data:
        work_id = workspace_entry.get('work_id')

        result = supabase.table('work_data').select('creator_id','url','display').eq('work_id', work_id).execute()
        display_name = result.data[0].get('display')
        url = result.data[0].get('url')
        creator_id = result.data[0].get('creator_id')

        creator_info = supabase.table('users_data').select('username').eq('user_id', creator_id).execute()
        creator_username = creator_info.data[0].get('username')
        
        workspace_info.append({'display_name': display_name, 'url': url, 'creator_username': creator_username})

    return jsonify({'username': username, 'workspaces': workspace_info})

# @ Logins
# I /api/logins/

# I Workspaces
# @ /api/work
    
@app.route('/api/work/create.json', methods=['POST'])
def handle_work_create():
    data = request.get_json()

    password = data.get('password')
    token = data.get('token')
    url = data.get('url')
    display = data.get('display')
    accesskey = data.get('accesskey')

    #

    salted_password = '32joi1' + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    #

    creator_response = supabase.table('users_data').select('user_id').eq('token', token).execute()
    creator_id = creator_response.data[0]['user_id'] if creator_response.data else None

    # ROUND 1 OF CONDITIONS
    conditions = [
        (not creator_id, 'w-mal-20', 'Work: Invalid token'),
        (accesskey != "newclass", 'w-mal-15', 'Work: Bad access key'),
    ]
    
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
    
    existing_workspaces = supabase.table('work_data').select('url').eq('creator_id', creator_id).execute()
    existing_urls = [workspace['url'].lower() for workspace in existing_workspaces.data] if existing_workspaces.data else []

    conditions = [
        (url.lower() in existing_urls, 'w-mal-30', 'Work: url already exists for this user'),
        (not re.match(r'^[A-Za-z\d_]{3,20}$', url), 'w-mal-31', 'Work: Invalid URL'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
    
    #
    
    supabase.table("work_data").insert({"creator_id": creator_id, "auth": sha256_hash, "url": url, "display": display}).execute()

    work_id = supabase.table('work_data').select('work_id').eq('creator_id', creator_id).eq('url', url).execute().data[0]['work_id']

    supabase.table("members_data").insert({"member_id": creator_id, "work_id": work_id, "role": "superuser"}).execute()
    return jsonify({'success': 'Work: Workspace created successfully'})

@app.route('/api/work/<string:creator_username>/<string:url>/join.json', methods=['POST'])
def handle_work_join(creator_username, url):
    data = request.get_json()

    password = data.get('password')
    token = data.get('token')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute()
    user_id = user_data.data[0]['user_id'] if user_data.data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute()
    creator_id = creator_data.data[0]['user_id'] if creator_data.data else None

    # ROUND 1 OF CONDITIONS
    conditions = [
        (not user_id, 'w-mal-25-1', 'Work: Invalid token', 'r1'),
        (not creator_id, 'w-mal-25-11', 'Work: That workspace does not exist', 'r1'),
    ]

    for condition in conditions:
        if condition[0] and condition[3] == "r1": return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id','auth').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None
    work_auth = work_query.data[0]['auth'] if work_query.data else None

    # ROUND 2 OF CONDITIONS
    conditions = [(not work_id, 'w-mal-25-2', 'Work: That workspace does not exist', 'r2')]
    for condition in conditions:
        if condition[0] and condition[3] == "r2": return jsonify({'error': condition[1], 'message': condition[2]})

    salted_password = '32joi1' + password
    sha256_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    # ROUND 3 OF CONDITIONS
    conditions = [(sha256_hash != work_auth, 'w-mal-55', 'Work: Invalid access credentials', 'r3')]
    for condition in conditions:
        if condition[0] and condition[3] == "r3": return jsonify({'error': condition[1], 'message': condition[2]})

    #
        
    existing_member = supabase.table('members_data').select('member_id').eq('member_id', user_id).eq('work_id', work_id).execute().data

    conditions = [(existing_member, 'w-mal-60', 'Work: User is already a member of this workspace', 'r4')]
    for condition in conditions:
        if condition[0] and condition[3] == "r4": return jsonify({'error': condition[1], 'message': condition[2]})
    
    #

    supabase.table("members_data").insert({"member_id": user_id, "work_id": work_id, "role": "member"}).execute()
    return jsonify({'success': 'Work: Workspace joined successfully'})

@app.route('/api/work/<string:creator_username>/<string:url>/home.json', methods=['POST'])
def handle_work_home(creator_username, url):
    data = request.get_json()
    token = data.get('token')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # ROUND 1 OF CONDITIONS
    conditions = [
        (not user_id, 'w-mal-25-1', 'Work: Invalid token', 'r1'),
        (not creator_id, 'w-mal-25-11', 'Work: That workspace does not exist', 'r1'),
    ]

    for condition in conditions:
        if condition[0] and condition[3] == "r1": return jsonify({'error': condition[1], 'message': condition[2]})
        
    work_query = supabase.table('work_data').select('work_id','display').eq('url', url).eq('creator_id', creator_id).execute().data

    work_id = work_query[0]['work_id'] if work_query else None
    display = work_query[0]['display'] if work_query else None

    # ROUND 2 OF CONDITIONS
    conditions = [
        (not work_id, 'w-mal-25-2', 'Work: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute().data
    user_role = user_role_data[0]['role'] if user_role_data else None

    # ROUND 3 OF CONDITIONS
    conditions = [(not user_role, 'w-mal-26', 'Work: You are not a member of that workspace')]
    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    members_data = supabase.table('members_data').select('member_id', 'role').eq('work_id', work_id).execute().data

    members_response = []
    for member_data in members_data:
        member_id = member_data.get('member_id')
        member_role = member_data.get('role')

        result = supabase.table('users_data').select('username').eq('user_id', member_id).execute()
        member_username = result.data[0].get('username')

        members_response.append({
            'username': member_username,
            'role': member_role
        })
        
    return jsonify({'display': display, 'members': members_response})

@app.route('/api/work/<string:creator_username>/<string:url>/settings.json', methods=['POST'])
def handle_work_settings(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    value = data.get('value')
    action = data.get('action')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'w-mal-25-1', 'Work: Invalid token'),
        (not creator_id, 'w-mal-25-11', 'Work: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'w-mal-25-2', 'Work: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute().data
    user_role = user_role_data[0]['role'] if user_role_data else None

    conditions = [
        (not user_role, 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    if action == "santa":
        conditions = [
            (user_role != "superuser", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

        return jsonify({'message':'Ho ho ho! please message me on discord @pvcsd and explain what you were supposed to be doing when you found this'})
    
    elif action == "display":
        conditions = [
            (user_role != "superuser", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
        supabase.table('work_data').update({'display': value}).eq('work_id', work_id).execute()
        return jsonify({'success': 'Work: Settings updated successfully'})
    
    elif action == "url":
        existing_workspaces = supabase.table('work_data').select('url').eq('creator_id', creator_id).execute()
        existing_urls = [workspace['url'].lower() for workspace in existing_workspaces.data] if existing_workspaces.data else []

        conditions = [
            (value.lower() in existing_urls, 'w-mal-30-11', 'Work: url already exists for this user'),
            (not re.match(r'^[A-Za-z_]{1,20}$', value), 'w-mal-50', 'Work: Invalid url you silly'),
            (user_role != "superuser", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

        supabase.table('work_data').update({'url': value}).eq('work_id', work_id).execute()
        return jsonify({'success': 'Work: Settings updated successfully'})
    
    elif action == "leave":
        conditions = [
            (user_role == "superuser", 'w-mal-20-2', 'Work: You do not have the correct permissions to exit this workspace.')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
        supabase.table('members_data').delete().eq('work_id', work_id).eq('member_id', user_id).execute()
        return jsonify({'success': 'Work: Left workspace successfully'})
    
    elif action == "delete":
        conditions = [
            (user_role != "superuser", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
        
        supabase.table('members_data').delete().eq('work_id', work_id).execute()
        supabase.table('work_data').delete().eq('work_id', work_id).execute()

        return jsonify({'success': 'Work: Removed workspace successfully'})
    
    elif action == "remove_member":
        conditions = [
            (user_role != "superuser", 'w-mal-20', 'Work: You do not have the proper permissions to change settings.')
        ]

        for condition in conditions:
            if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

        supabase.table('members_data').delete().eq('work_id', work_id).eq('member_id', value).execute()
        supabase.table('posts_data').delete().eq('work_id', work_id).eq('user_id', value).execute()
        supabase.table('sessions_data').delete().eq('work_id', work_id).eq('user_id', value).execute()

            
# @ Workspaces
# I /api/work/

# I Discussions & Bulletins
# @ /api/discuss

@app.route('/api/discuss/<string:creator_username>/<string:url>/post.json', methods=['POST'])
def handle_discuss_post(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    message = data.get('value')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute()
    user_id = user_data.data[0]['user_id'] if user_data.data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute()
    creator_id = creator_data.data[0]['user_id'] if creator_data.data else None

    # ROUND 1 OF CONDITIONS
    conditions = [
        (not user_id, 'd-mal-25-1', 'Discussions: Invalid token', 'r1'),
        (not creator_id, 'd-mal-25-11', 'Discussions: That workspace does not exist', 'r1'),
    ]

    for condition in conditions:
        if condition[0] and condition[3] == "r1": return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # ROUND 2 OF CONDITIONS
    conditions = [(not work_id, 'd-mal-25-2', 'Discussions: That workspace does not exist', 'r2')]
    for condition in conditions:
        if condition[0] and condition[3] == "r2": return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    # ROUND 3 OF CONDITIONS
    conditions = [(not user_role, 'd-mal-20', 'Discussions: You do not have the proper permissions to post messages.', 'r3')]
    for condition in conditions:
        if condition[0] and condition[3] == "r3": return jsonify({'error': condition[1], 'message': condition[2]})
        
    current_utc_time = datetime.now(timezone.utc)
    formatted_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    supabase.table("posts_data").insert({"user_id": user_id, "work_id": work_id, "content": message, "creation_date": formatted_time}).execute()
    return jsonify({'success': 'Discuss: Post created successfully'})

@app.route('/api/discuss/<string:creator_username>/<string:url>/home.json', methods=['POST'])
def handle_discuss_home(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    # page = data.get('page')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute()
    user_id = user_data.data[0]['user_id'] if user_data.data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute()
    creator_id = creator_data.data[0]['user_id'] if creator_data.data else None

    # ROUND 1 OF CONDITIONS
    conditions = [
        (not user_id, 'd-mal-25-1', 'Discussions: Invalid token', 'r1'),
        (not creator_id, 'd-mal-25-11', 'Discussions: That workspace does not exist', 'r1'),
    ]

    for condition in conditions:
        if condition[0] and condition[3] == "r1": return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # ROUND 2 OF CONDITIONS
    conditions = [(not work_id, 'd-mal-25-2', 'Discussions: That workspace does not exist', 'r2')]

    for condition in conditions:
        if condition[0] and condition[3] == "r2": return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    # ROUND 3 OF CONDITIONS
    conditions = [(not user_role, 'd-mal-20-10', 'Discussions: You do not have the proper permissions to access messages.', 'r3')]

    for condition in conditions:
        if condition[0] and condition[3] == "r3": return jsonify({'error': condition[1], 'message': condition[2]})

    posts_data = supabase.table("posts_data").select('post_id').eq('work_id', work_id).execute()
    post_ids = posts_data.data

    posts = []
    for post in post_ids:
        post_id = post.get('post_id')
        result = supabase.table('posts_data').select('user_id','post_id','content','creation_date').eq('post_id', post_id).execute()

        user_id = result.data[0].get('user_id')
        content = result.data[0].get('content')
        creation_date = result.data[0].get('creation_date')
        post_id = result.data[0].get('post_id')

        result = supabase.table('users_data').select('username').eq('user_id', user_id).execute()
        username = result.data[0]['username'] if result.data else None

        posts.append({
            'username': username,
            'content': content,
            'creation_date': creation_date,
            'post_id': post_id
        })
    
    return jsonify({'posts': posts})

@app.route('/api/discuss/<string:creator_username>/<string:url>/settings.json', methods=['POST'])
def handle_discuss_settings(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    value = data.get('value')
    action = data.get('action')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'd-mal-25-1', 'Discussions: Invalid token'),
        (not creator_id, 'd-mal-25-11', 'Discussions: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'd-mal-25-2', 'Discussions: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute().data
    user_role = user_role_data[0]['role'] if user_role_data else None

    conditions = [
        (not user_role or user_role != "superuser", 'd-mal-20', 'Discussions: You do not have the proper permissions to change settings.')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    if action == "santa":
        return jsonify({'message':'Ho ho ho! please message me on discord @pvcsd and explain what you were supposed to be doing when you found this'})
    
    elif action == "remove":
        supabase.table('posts_data').delete().eq('post_id', value).eq('work_id', work_id).execute()
        return jsonify({'success': 'Discussions: Settings removed successfully'})
    
@app.route('/api/exams/<string:creator_username>/<string:url>/create.json', methods=['POST'])
def handle_exams_create(creator_username, url):
    data = request.get_json()

    token = data.get("token")
    exam_name = data.get("exam_name")

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token'),
        (not creator_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute().data
    user_role = user_role_data[0]['role'] if user_role_data else None

    conditions = [
        (not user_role or user_role != "superuser", 'e-mal-20', 'Exams: You do not have the proper permissions to create tests.')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})
    
    supabase.table('exams_data').insert({"display_name": exam_name, "work_id": work_id, "visibility": "private"}).execute()
    return jsonify({'success': 'Exams: Created test successfully'})

@app.route('/api/exams/<string:creator_username>/<string:url>/home.json', methods=['POST'])
def handle_exams_home(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    # page = data.get('page')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute()
    user_id = user_data.data[0]['user_id'] if user_data.data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute()
    creator_id = creator_data.data[0]['user_id'] if creator_data.data else None

    # ROUND 1 OF CONDITIONS
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token', 'r1'),
        (not creator_id, 'e-mal-25-5', 'Exams: That workspace does not exist', 'r1'),
    ]

    for condition in conditions:
        if condition[0] and condition[3] == "r1": return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # ROUND 2 OF CONDITIONS
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist', 'r2')
    ]

    for condition in conditions:
        if condition[0] and condition[3] == "r2": return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    # ROUND 3 OF CONDITIONS
    conditions = [
        (not user_role, 'e-mal-20-10', 'Exams: You do not have the proper permissions to access tests.', 'r3')
    ]
    
    for condition in conditions:
        if condition[0] and condition[3] == "r3": return jsonify({'error': condition[1], 'message': condition[2]})

    if user_role == "member":
        exams_data = supabase.table("exams_data").select('exam_id').eq('work_id', work_id).eq('visibility', "public").execute()
        exam_ids = exams_data.data

        exams = []
        for exam in exam_ids:
            exam_id = exam.get('exam_id')

            result = supabase.table('exams_data').select('display_name','visibility').eq('exam_id', exam_id).execute()

            exam_name = result.data[0]['display_name'] if result.data else None
            visibility = result.data[0]['visibility'] if result.data else None

            exams.append({
                'display_name': exam_name,
                'visibility': visibility,
                'exam_id': exam_id
            })
    
        return jsonify({'exams': exams})
        
    elif user_role == "superuser":
        exams_data = supabase.table("exams_data").select('exam_id').eq('work_id', work_id).execute()
        exam_ids = exams_data.data

        exams = []
        for exam in exam_ids:
            exam_id = exam.get('exam_id')

            result = supabase.table('exams_data').select('display_name','visibility').eq('exam_id', exam_id).execute()

            exam_name = result.data[0]['display_name'] if result.data else None
            visibility = result.data[0]['visibility'] if result.data else None

            exams.append({
                'display_name': exam_name,
                'visibility': visibility,
                'exam_id': exam_id
            })
    
    return jsonify({'exams': exams})

@app.route('/api/exams/<string:creator_username>/<string:url>/settings.json', methods=['POST'])
def handle_exam_settings(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    exam_id = data.get('value')
    action = data.get('action')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token'),
        (not creator_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('status', "active").eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (not user_role or user_role != "superuser", 'e-mal-20', 'Exams: You do not have the proper permissions to change settings.'),
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (session_id, 'e-mal-26-61', 'Exams: This exam has one or more active sessions so it cant be accessed traditionally')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    if action == "santa":
        return jsonify({'message':'Ho ho ho! please message me on discord @pvcsd and explain what you were supposed to be doing when you found this'})
    
    elif action == "remove":
        supabase.table('options_data').delete().eq('exam_id', exam_id).execute()
        supabase.table('questions_data').delete().eq('exam_id', exam_id).execute()
        supabase.table('exams_data').delete().eq('exam_id', exam_id).eq('work_id', work_id).execute()

        return jsonify({'success': 'Exams: Settings removed successfully'})
    
    elif action == "toggle":
        supabase.table('exams_data').update({'visibility': 'public'}).eq('exam_id', exam_id).eq('work_id', work_id).execute()
        return jsonify({'success': 'Exams: Settings updated successfully'})

@app.route('/api/exams/<string:creator_username>/<string:url>/build.json', methods=['POST'])
def handle_exam_build(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    exam_id = data.get('exam_id')
    action = data.get('action')
    questions = data.get('questions', [])

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token'),
        (not creator_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (not user_role or user_role != "superuser", 'e-mal-20', 'Exams: You do not have the proper permissions to change exam configurations.'),
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (session_id, 'e-mal-26-61', 'Exams: This exam has one or more active sessions so it cant be accessed traditionally')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    # cut
        
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

                # check for conditions
                for condition in conditions:
                    if condition[0]:
                        return jsonify({'error': condition[1], 'message': condition[2]})

                orders.append(option_order)
            
            for option_content in options:
                content = option_content.get('content', '')
                order = option_content.get('order', '')

                supabase.table('options_data').insert({'question_id': question_id, 'content': content, 'exam_id': exam_id, 'option_order': order}).execute()

    return jsonify({'success': 'Exam: Questions added successfully'})

@app.route('/api/exams/<string:creator_username>/<string:url>/access.json', methods=['POST'])
def handle_exam_access(creator_username, url):
    data = request.get_json()
    
    token = data.get('token')
    exam_id = data.get('value')
    creator_username = data.get('creator')
    url = data.get('url')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token'),
        (not creator_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('status', "active").eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (not user_role or user_role != "superuser", 'e-mal-20', 'Exams: You do not have the proper permissions to change exam configurations.'),
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (session_id, 'e-mal-26-61', 'Exams: This exam has one or more active sessions so it cant be accessed traditionally')
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

    return jsonify({'questions': formatted_questions})

@app.route('/api/exams/start.json', methods=['POST'])
def handle_exam_start():
    data = request.get_json()
    
    token = data.get('token')
    exam_id = data.get('value')
    creator_username = data.get('creator')
    url = data.get('url')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token'),
        (not creator_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    exam_work_data = supabase.table('exams_data').select('work_id', 'visibility').eq('exam_id', exam_id).execute()

    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None
    exam_visibility = exam_work_data.data[0]['visibility'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id').eq('user_id', user_id).eq('exam_id', exam_id).execute()
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (not user_role or user_role == "superuser", 'e-mal-20', 'Exams: You do not have the proper permissions to start an exam.'),
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

@app.route('/api/exams/<string:creator_username>/<string:url>/check_stat.json', methods=['POST'])
def handle_exam_check_stat(creator_username, url):
    data = request.get_json()
    
    token = data.get('token')
    exam_id = data.get('value')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token'),
        (not creator_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    exam_work_data = supabase.table('exams_data').select('work_id', 'visibility').eq('exam_id', exam_id).execute()

    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None
    exam_visibility = exam_work_data.data[0]['visibility'] if exam_work_data.data else None

    session_data = supabase.table('sessions_data').select('session_id', 'status').eq('exam_id', exam_id).eq('user_id', user_id).execute()

    session_status = session_data.data[0]['status'] if session_data.data else None
    session_id = session_data.data[0]['session_id'] if session_data.data else None

    conditions = [
        (not user_role, 'e-mal-20', 'Exams: You do not have the proper permissions to check an exam.'),
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.'),
        (exam_visibility != "public", 'e-mal-22-01', 'Exams: You are only allowed to check public exams.'),
        (session_id, 'e-mal-20-21', 'Exams: You have not started this exam yet!')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    return jsonify({'status': session_status})

@app.route('/api/exams/<string:creator_username>/<string:url>/check_stu_list.json', methods=['POST'])
def handle_exam_check_stu_list(creator_username, url):
    data = request.get_json()

    token = data.get('token')
    exam_id = data.get('value')
    action = data.get('action')

    user_data = supabase.table('users_data').select('user_id').eq('token', token).execute().data
    user_id = user_data[0]['user_id'] if user_data else None

    creator_data = supabase.table('users_data').select('user_id').eq('username', creator_username).execute().data
    creator_id = creator_data[0]['user_id'] if creator_data else None

    # CONDITIONS ROUND 1
    conditions = [
        (not user_id, 'e-mal-25-1', 'Exams: Invalid token'),
        (not creator_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    work_query = supabase.table('work_data').select('work_id').eq('url', url).eq('creator_id', creator_id).execute()
    work_id = work_query.data[0]['work_id'] if work_query.data else None

    # CONDITIONS ROUND 2
    conditions = [
        (not work_id, 'e-mal-25-2', 'Exams: That workspace does not exist'),
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    user_role_data = supabase.table('members_data').select('role').eq('member_id', user_id).eq('work_id', work_id).execute()
    user_role = user_role_data.data[0]['role'] if user_role_data.data else None

    exam_work_data = supabase.table('exams_data').select('work_id').eq('exam_id', exam_id).execute()
    exam_work_id = exam_work_data.data[0]['work_id'] if exam_work_data.data else None

    conditions = [
        (not user_role or user_role != "superuser", 'e-mal-20', 'Exams: You do not have the proper permissions to change settings.'),
        (exam_work_id != work_id, '>:(', 'Exams: You are only allowed to modify exams in your workspace.')
    ]

    for condition in conditions:
        if condition[0]: return jsonify({'error': condition[1], 'message': condition[2]})

    sessions_data = session_data = supabase.table('sessions_data').select('session_id', 'status', 'user_id').eq('exam_id', exam_id).execute().data

    student_sessions = []
    for session_data in sessions_data:
        student_id = session_data.get('user_id')

        student_data = supabase.table('users_data').select('username').eq('user_id', student_id).execute()
        student_username = student_data.data[0]['username'] if student_data.data else None

        formatted_session = {"status": session_data.get('status'), "username": student_username, "session_id": session_data.get('session_id')}
        student_sessions.append(formatted_session)

    return jsonify({'sessions': student_sessions})



# Glad you're here!

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)