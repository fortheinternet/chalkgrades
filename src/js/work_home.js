document.addEventListener("DOMContentLoaded", function() {
    const token = getCookie("token")

    console.info("INFORMATION: Loading of JavaScript file 'work_home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    // Get URL Data
    const currentUrl = window.location.href
    const urlParts = currentUrl.split('/')

    let creator_username = urlParts[urlParts.length - 2]
    creator_username = decodeURIComponent(creator_username)

    const url = urlParts[urlParts.length - 1]
    const main = document.getElementById("main")

    // Get document stuff
    const username_fields = document.querySelectorAll(".username_field")
    const work_user = document.getElementById("work_user")
    const work_url = document.getElementById("work_url")
    const work_display_h4 = document.getElementById("work_display")
    const view_settings_btn = document.getElementById("view_settings_btn")

    const membersDiv = document.getElementById("members")
    const memberDiv = document.getElementById("member")

    const examDiv = document.getElementById("exam")
    const examsDiv = document.getElementById("exams")

    const clones = document.querySelectorAll('[data-origin="clone"]') 

    work_details = fetch_work_details(token, creator_username, url)
        .then(work_details => {
            if (work_details.error) {
                error = work_details.error
                console.error(error)

                if (error == "mal-25-1") {window.location.href = '/login'; removeCookie("token")}
                if (error == "w-mal-403") {window.location.href = '/home'}
                if (error == "w-mal-4000") {window.location.href = '/home'}
                
            }

            else {
                const username = work_details.username
                const work_display = work_details.display
                const realtime_access = work_details.realtime_access

                const members_data = work_details.members
                const exams_data = work_details.exams
                const user_id = work_details.user_id
                const user_role = work_details.user_role

                // Populate screen
                work_display_h4.textContent = work_display

                work_user.textContent = creator_username
                work_url.textContent = url

                if (user_role == "work_admin") {
                    view_settings_btn.style.display = "block";
                }

                console.info("User authenticated successfully as " + username)
                username_fields.forEach(username_field => {
                    username_field.textContent = username
                })

                clones.forEach(clone => {
                    clone.remove()
                });

                // members
                members_data.forEach(member => {
                    const { username, selected_role, selected_user_id } = member;
        
                    const memberClone = memberDiv.cloneNode(true);
                    memberClone.style.display = "flex";
        
                    memberClone.dataset.identifier = selected_user_id;
        
                    memberClone.querySelector("#member_user").textContent = username;
        
                    if (selected_role == "work_admin") {
                        memberClone.querySelector("#member_role").textContent = "teacher";
                    } else {
                        memberClone.querySelector("#member_role").textContent = "student";
                    }
        
                    memberClone.dataset.origin = "clone";
        
                    if(user_role == "work_admin") {
                        if(user_id == selected_user_id) {
                            memberClone.querySelector("#member_rm_span").textContent = "can't remove member";
                            memberClone.querySelector("#member_rm_lnk").dataset.action = "na";
                            memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                        } else {
                            memberClone.querySelector("#member_rm_span").textContent = "remove member";
                            memberClone.querySelector("#member_rm_lnk").dataset.action = "remove_member";
                            memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                        }
                    } else { 
                        if(user_id == selected_user_id) {
                            memberClone.querySelector("#member_rm_span").textContent = "leave workspace";
                            memberClone.querySelector("#member_rm_lnk").dataset.action = "leave";
                            memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                        } else {
                            memberClone.querySelector("#member_rm_span").textContent = "";
                            memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                        }
                    }
        
                    membersDiv.appendChild(memberClone);
        
                });
        
                // exams
                exams_data.forEach(exam => {
                    const { display_name, exam_id, visibility} = exam;
        
                    const examClone = examDiv.cloneNode(true);
                    examClone.style.display = "flex";
        
                    examClone.querySelector("#exam_display").textContent = display_name;
                    examClone.querySelector("#exam_visibility").textContent = visibility;
                    examClone.querySelector("#exam_link").href = "/" + creator_username + "/" + url + "/" + exam_id;
        
                    examClone.dataset.identifier = exam_id;
                    examClone.dataset.origin = "clone";
        
                    examsDiv.appendChild(examClone);
                });
        
                // realtime
                const ably = new Ably.Realtime({
                    authCallback: (anything_at_all, callback) => {
                        fetch(`https://chalk.fortheinternet.xyz/api/work/${creator_username}/${url}/home_realtime.json`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                token: token
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            callback(null, data.ably_token);
                        })
                        .catch(error => {
                            console.error(error);
                            callback(error, null);
                        });
                    }
                });                
                
                const channel = ably.channels.get(realtime_access);
        
                channel.subscribe(function(message) {
                    console.log('Received message:', message);
        
                    if (message.name == "member_join") {
                        const { username, selected_role, selected_user_id } = message.data
        
                        const memberClone = memberDiv.cloneNode(true);
                        memberClone.style.display = "flex";
        
                        memberClone.dataset.identifier = selected_user_id;
        
                        memberClone.querySelector("#member_user").textContent = username;
        
                        if (selected_role == "work_admin") {
                            memberClone.querySelector("#member_role").textContent = "teacher";
                        } else {
                            memberClone.querySelector("#member_role").textContent = "student";
                        }
        
                        memberClone.dataset.origin = "clone";
        
                        if(user_role == "work_admin") {
                            if(user_id == selected_user_id) {
                                memberClone.querySelector("#member_rm_span").textContent = "can't remove member";
                                memberClone.querySelector("#member_rm_lnk").dataset.action = "na";
                                memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                            } else {
                                memberClone.querySelector("#member_rm_span").textContent = "remove member";
                                memberClone.querySelector("#member_rm_lnk").dataset.action = "remove_member";
                                memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                            }
                        } else { 
                            if(user_id == selected_user_id) {
                                memberClone.querySelector("#member_rm_span").textContent = "leave workspace";
                                memberClone.querySelector("#member_rm_lnk").dataset.action = "leave";
                                memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                            } else {
                                memberClone.querySelector("#member_rm_span").textContent = "";
                                memberClone.querySelector("#member_rm_lnk").dataset.identifier = selected_user_id;
                            }
                        }
        
                        membersDiv.appendChild(memberClone);
        
                    } else if (message.name == "member_leave" || message.name == "member_remove") {
                        const { selected_user_id } = message.data
                        
                        if (selected_user_id == user_id) {
                            window.location.href = '/home';
                        } else {
                            const userElements = document.querySelectorAll(`[data-identifier="${selected_user_id}"]`);
                            userElements.forEach(element => {element.remove()});
                        }
                    }
                });
                
                ably.connection.on('connected', function() {
                    console.log('Ably connection established');
                });
                
                ably.connection.on('failed', function() {
                    console.error('Ably connection failed');
                });
                
                ably.connection.on('closed', function() {
                    console.log('Ably connection closed');
                });
        
                main.style.display = "flex"
                document.title = work_display + " - Chalk"
            }
        })
})

const token = getCookie("token")

function fetch_work_details(token, creator_username, url) {
    return fetch(`https://chalk.fortheinternet.xyz/api/work/${creator_username}/${url}/home.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token
        })
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch(error => {
        console.error('Error:', error)
    });
}


function remove_member(element) {
    const action = element.getAttribute('data-action');
    const identifier = element.getAttribute('data-identifier');

    if (action != "na") {
        const currentUrl = window.location.href;
        const urlParts = currentUrl.split('/');
    
        const creator_username = urlParts[urlParts.length - 2];
        const url = urlParts[urlParts.length - 1];
    
        console.table([
            ["identifier", identifier],
            ["action", action]
        ])
        
        fetch(`https://chalk.fortheinternet.xyz/api/work/${creator_username}/${url}/settings.json`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: action,
                    value: identifier,
                    token: token
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error == "w-mal-25-1") {
                    window.location.href = '/login';
                    removeCookie("token");
    
                } else {
                    const userElements = document.querySelectorAll(`[data-identifier="${identifier}"]`);
                    userElements.forEach(element => {
                        if(element.getAttribute('data-action') == "leave") {
                            window.location.href = '/home';
                        } else {
                            element.remove()
                        }            
                    });
                }
                    
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        console.warn("INFORMATION: You cannot remove this member.")
    }
}

function create_submit() {
    const createErrors = document.getElementById("create_errors");
    const createDisplay = document.getElementById("create_display")
    
    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');

    const creator_username = urlParts[urlParts.length - 2];
    const url = urlParts[urlParts.length - 1];

    fetch(`https://chalk.fortheinternet.xyz/api/exams/${creator_username}/${url}/create.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            exam_name: createDisplay.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            createErrors.textContent = data.message;

            if (data.error == "e-mal-25-1") {
                window.location.href = '/login';
                removeCookie("token");
            }
        } else {
            createErrors.textContent = "Test created successfully, you can go to the 'Exams' tab to check."
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function view_members() {
    const view_members = document.getElementById("view_members");
    const view_exams = document.getElementById("view_exams");
    const view_settings = document.getElementById("view_settings");
    
    view_members.style.display = "block";
    view_exams.style.display = "none";
    view_settings.style.display = "none";
    
}

function view_settings() {
    const view_members = document.getElementById("view_members");
    const view_exams = document.getElementById("view_exams");
    const view_settings = document.getElementById("view_settings");
    const create_exam = document.getElementById("create_exam");

    view_members.style.display = "none";
    view_exams.style.display = "none";
    view_settings.style.display = "block";
    create_exam.style.display = "block";
    
}

function view_exams() {
    const view_members = document.getElementById("view_members");
    const view_exams = document.getElementById("view_exams");
    const view_settings = document.getElementById("view_settings");

    view_members.style.display = "none";
    view_exams.style.display = "block";
    view_settings.style.display = "none";

}

function logout() {
    removeCookie("token")
    window.location.href = '/login';
}

function nav_user() {
    window.location.href = '/home';
}

// This code does not look professional, it looks like a cat fell asleep on the keyboard. But it works so it won't be fixed. Or at least not by me ¯\_(ツ)_/¯

function setCookie(cname, cvalue) {
    let d = new Date();
    d.setTime(d.getTime() + 10 * 365 * 24 * 60 * 60 * 1000);
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; expires=" + expires + "; path=/; SameSite=None; Secure";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function removeCookie(cname) {
    document.cookie = cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=None; Secure";
}
