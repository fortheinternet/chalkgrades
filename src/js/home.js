document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const user_token = getCookie("token")

    if(user_token) {
        load_homedotjson()
    } else {
        window.location.href = '/login';
    }
})

function load_homedotjson() {
    const workspaceDiv = document.getElementById("workspace");
    const workspacesDiv = document.getElementById("workspaces");
    const username_fields = document.querySelectorAll(".username_field")

    const loading = document.getElementById("loading")
    const main = document.getElementById("main")

    const user_token = getCookie("token")
    const userData = {token: user_token};

    fetch('https://chalkgrades.vercel.app/api/logins/home.json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error == "h-mal-10") {
                window.location.href = '/login';
                removeCookie("token");
            } else {
                username = data.username;
                console.info("User authenticated successfully as " + username)
                username_fields.forEach(username_field => {
                    username_field.textContent = username;
                })

                const workspaces_data = data.workspaces;
                const workspaceClones = workspacesDiv.querySelectorAll('[data-origin="clone"]')

                workspaceClones.forEach(workspaceClone => {
                    workspaceClone.remove()
                });

                workspaces_data.forEach(workspace => {
                    const { display_name, creator_username, url } = workspace;

                    const workspaceClone = workspaceDiv.cloneNode(true);

                    workspaceClone.querySelector("#workspace_display").textContent = display_name;
                    workspaceClone.querySelector("#workspace_creator").textContent = creator_username;
                    workspaceClone.querySelector("#workspace_url").textContent = url;
                    workspaceClone.querySelector("#workspace_link").href = "/" + creator_username + "/" + url;

                    workspaceClone.dataset.origin = "clone";
                    
                    workspacesDiv.appendChild(workspaceClone);
                    workspaceClone.style.display = "flex";

                });

                main.style.display = "flex"
                loading.style.display = "none"
                document.title = username + " - Chalk"

            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function create_new_workspace() {
    const create_section = document.getElementById("create_workspace");
    const join_section = document.getElementById("join_workspace");
    const work_section = document.getElementById("workspaces_wrap");

    const work_section_c1 = document.getElementById("create_errors");
    const work_section_c2 = document.getElementById("create_url");
    const work_section_c3 = document.getElementById("create_password");
    const work_section_c4 = document.getElementById("create_display");
    const work_section_c5 = document.getElementById("create_access");


    work_section_c1.textContent = "Workspaces are for classes you attend. You must have an access credential to create a workspace."
    work_section_c2.value = ""
    work_section_c3.value = ""
    work_section_c4.value = ""
    work_section_c5.value = ""

    create_section.style.display = "block";
    join_section.style.display = "none";
    work_section.style.display = "none";
}

function join_new_workspace() {
    const create_section = document.getElementById("create_workspace");
    const join_section = document.getElementById("join_workspace");
    const work_section = document.getElementById("workspaces_wrap");

    const work_section_j1 = document.getElementById("join_errors");
    const work_section_j2 = document.getElementById("join_superuser");
    const work_section_j3 = document.getElementById("join_url");
    const work_section_j4 = document.getElementById("join_password");

    work_section_j1.textContent = "Workspaces are for classes you attend. You must have an access credential to create a workspace."
    work_section_j2.value = ""
    work_section_j3.value = ""
    work_section_j4.value = ""


    create_section.style.display = "none";
    join_section.style.display = "block";
    work_section.style.display = "none";
}

function view_workspaces() {
    const create_section = document.getElementById("create_workspace");
    const join_section = document.getElementById("join_workspace");
    const work_section = document.getElementById("workspaces_wrap");

    create_section.style.display = "none";
    join_section.style.display = "none";
    work_section.style.display = "block";

    load_homedotjson()
}

function logout() {
    removeCookie("token")
    window.location.href = '/login';
}

function nav_user() {
    window.location.href = '/home';
}

//

function create_submit() {
    const createErrors = document.getElementById("create_errors");
    const createDisplay = document.getElementById("create_display");
    const createURL = document.getElementById("create_url");
    const createPassword = document.getElementById("create_password");
    const createAccess = document.getElementById("create_access");

    const workData = {token: getCookie("token"), display: createDisplay.value, url: createURL.value, password: createPassword.value, accesskey: createAccess.value}; 

    fetch('https://chalkgrades.vercel.app/api/work/create.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(workData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            createErrors.textContent = data.message;

            if (data.error == "w-mal-20") {
                window.location.href = '/login';
                removeCookie("token");
            }
        } else {
            window.location.href = `/${username}/${createURL.value}`
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function join_submit() {
    const joinErrors = document.getElementById("join_errors");
    const joinSuperuser = document.getElementById("join_superuser");
    const joinURL = document.getElementById("join_url");
    const joinPassword = document.getElementById("join_password");

    superuser_value = joinSuperuser.value;
    url_value = joinURL.value;

    const workData = {token: getCookie("token"), password: joinPassword.value};

    fetch(`https://chalkgrades.vercel.app/api/work/${superuser_value}/${url_value}/join.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(workData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            joinErrors.textContent = data.message;

            if (data.error == "w-mal-25-1") {
                window.location.href = '/login';
                removeCookie("token");
            }
        } else {
            window.location.href = `/${superuser_value}/${url_value}`
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
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
