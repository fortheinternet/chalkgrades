document.addEventListener("DOMContentLoaded", function() {
    const token = getCookie("token")
    
    console.info("INFORMATION: Loading of JavaScript file 'home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const main = document.getElementById("main")

    const workspaceDiv = document.getElementById("workspace");
    const workspacesDiv = document.getElementById("workspaces");
    const username_fields = document.querySelectorAll(".username_field")

    user_details = fetch_user_details(token)
        .then(user_details => {
            if (user_details.error) {
                error = user_details.error
                console.error(error)
                
                if (error == "invalid-token") {window.location.href = '/login'; removeCookie("token")}
            }

            else {
                username = user_details.username
                workspaces_data = user_details.workspaces

                console.info("User authenticated successfully as " + username)
                username_fields.forEach(username_field => {
                    username_field.textContent = username;
                })

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
   
                main.style.display = "block"
                document.title = username + " - Chalk"

            }
        })

    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme:dark)').matches)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
})

const token = getCookie("token")

function fetch_user_details(token) {
    return fetch('https://chalk.fortheinternet.xyz/api/logins/home.json', {
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
            return data;
        })
        .catch(error => {
            console.error('Error:', error);
    });
}

function create_new_workspace() {
    const create_section = document.getElementById("create_workspace")
    const join_section = document.getElementById("join_workspace")
    const work_section = document.getElementById("workspaces_wrap")

    create_section.style.display = "block";
    join_section.style.display = "none";
    work_section.style.display = "none";
}

function join_new_workspace() {
    const create_section = document.getElementById("create_workspace")
    const join_section = document.getElementById("join_workspace")
    const work_section = document.getElementById("workspaces_wrap")

    create_section.style.display = "none";
    join_section.style.display = "block";
    work_section.style.display = "none";
}

function view_workspaces() {
    const create_section = document.getElementById("create_workspace")
    const join_section = document.getElementById("join_workspace")
    const work_section = document.getElementById("workspaces_wrap")

    create_section.style.display = "none";
    join_section.style.display = "none";
    work_section.style.display = "block";
}

function logout() {
    removeCookie("token")
    window.location.href = '/login';
}

function nav_user() {
    window.location.href = '/home';
}

function theme(input) {
    if (input == "remove") {
        localStorage.removeItem('theme')
    }

    if (input == "light") {
        localStorage.theme = 'light'
    }

    if (input == "dark") {
        localStorage.theme = 'dark'
    }
    
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
}

function create_submit() {
    const createDisplay = document.getElementById("create_display");
    const createURL = document.getElementById("create_url");
    const createPassword = document.getElementById("create_password");
    const createAccess = document.getElementById("create_access");

    fetch('https://chalk.fortheinternet.xyz/api/work/create.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            display: createDisplay.value,
            url: createURL.value,
            password: createPassword.value,
            accesskey: createAccess.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            if (data.error == "invalid-token") {
                window.location.href = '/login';
                removeCookie("token");
            }

            alert("ISSUE: " + data.message)
            console.error(data.error + " - " + data.message)
        } else {
            window.location.href = `/${username}/${createURL.value}`
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function join_submit() {
    const joinwork_admin = document.getElementById("join_work_admin");
    const joinURL = document.getElementById("join_url");
    const joinPassword = document.getElementById("join_password");

    work_admin_value = joinwork_admin.value;
    url_value = joinURL.value;


    fetch(`https://chalk.fortheinternet.xyz/api/work/${work_admin_value}/${url_value}/join.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            password: joinPassword.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            if (data.error == "invalid-token") {
                window.location.href = '/login';
                removeCookie("token");
            }

            alert("ISSUE: " + data.message)
            console.error(data.error + " - " + data.message)
        } else {
            window.location.href = `/${work_admin_value}/${url_value}`
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
