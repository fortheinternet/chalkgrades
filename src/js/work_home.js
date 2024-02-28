document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'work_home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const user_token = getCookie("token")

    if (user_token) {
        load_workhomedotjson()
    } else {
        window.location.href = '/login';
    }
})

function load_workhomedotjson() {
    const username_fields = document.querySelectorAll(".username_field")
    const work_user = document.getElementById("work_user")
    const work_url = document.getElementById("work_url")
    const work_display = document.getElementById("work_display")

    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');

    const creator_username = urlParts[urlParts.length - 2];
    const url = urlParts[urlParts.length - 1];

    const user_token = getCookie("token")
    const userData = {token: user_token}

    const main = document.getElementById("main")

    fetch(`https://chalkgrades.vercel.app/api/work/${creator_username}/${url}/home.json`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error == "w-mal-25-1") {
                window.location.href = '/login';
                removeCookie("token");

            } else if (data.error == "w-mal-25-11") {
                window.location.href = 'https://en.wikipedia.org/wiki/HTTP_404';

            } else if (data.error == "w-mal-26") {
                window.location.href = '/home';

            } else {
                username = data.username;
                console.info("User authenticated successfully as " + username)
                username_fields.forEach(username_field => {
                    username_field.textContent = username;
                })
                work_display.textContent = data.display;

                work_user.textContent = creator_username;
                work_url.textContent = url;

                const membersDiv = document.getElementById("members")
                const memberDiv = document.getElementById("member")

                const examDiv = document.getElementById("exam")
                const examsDiv = document.getElementById("exams")
                
                const members_data = data.members;
                const exams_data = data.exams;
                const user_id = data.user_id;
                const user_role = data.user_role;

                console.table([
                    ["members_data", members_data],
                    ["exams_data", exams_data],
                    ["user_id", user_id],
                    ["user_role", user_role]
                ])
                
                const view_settings_btn = document.getElementById("view_settings_btn")

                if (user_role == "superuser") {
                    view_settings_btn.style.display = "block";
                }

                anyClones = document.querySelectorAll('[data-origin="clone"]') 

                anyClones.forEach(clone => {
                    clone.remove()
                });
                
                members_data.forEach(member => {
                    const { username, selected_role, selected_user_id } = member;

                    const memberClone = memberDiv.cloneNode(true);
                    memberClone.style.display = "flex";

                    memberClone.querySelector("#member_user").textContent = username;
                    memberClone.querySelector("#member_role").textContent = selected_role;

                    memberClone.dataset.identifier = selected_user_id;
                    memberClone.dataset.origin = "clone";

                    if(user_role == "superuser") {
                        if(user_id == selected_user_id) {
                            memberClone.querySelector("#member_rm_span").textContent = "can't remove member";
                            memberClone.querySelector("#member_rm_lnk").dataset.action = "na";
                        } else {
                            memberClone.querySelector("#member_rm_span").textContent = "remove member";
                            memberClone.querySelector("#member_rm_lnk").dataset.action = "remove_member";
                        }
                    } else { 
                        if(user_id == selected_user_id) {
                            memberClone.querySelector("#member_rm_span").textContent = "leave workspace";
                            memberClone.querySelector("#member_rm_lnk").dataset.action = "leave";
                        } else {
                            memberClone.querySelector("#member_rm_span").textContent = "";
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

                main.style.display = "flex"
                document.title = data.display + " - Chalk"
            }
        })
        .catch(error => {
            console.error('Error:', error);
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
    
        const user_token = getCookie("token")
    
        const userData = {
            token: user_token,
            action: action,
            value: identifier
        }
    
        fetch(`https://chalkgrades.vercel.app/api/work/${creator_username}/${url}/settings.json`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
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

    const examData = {token: getCookie("token"), exam_name: createDisplay.value};

    fetch(`https://chalkgrades.vercel.app/api/exams/${creator_username}/${url}/create.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(examData)
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

    load_workhomedotjson()
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

    load_workhomedotjson()
}

function view_exams() {
    const view_members = document.getElementById("view_members");
    const view_exams = document.getElementById("view_exams");
    const view_settings = document.getElementById("view_settings");

    view_members.style.display = "none";
    view_exams.style.display = "block";
    view_settings.style.display = "none";

    load_workhomedotjson()
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
