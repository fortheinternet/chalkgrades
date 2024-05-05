document.addEventListener("DOMContentLoaded", function() {
    const token = getCookie("token")

    window.addEventListener('resize', function() {
        const nav = document.querySelector('nav');
        if (window.innerWidth >= 1024) { nav.style.display = "flex"}
    });

    console.info("INFORMATION: Loading of JavaScript file 'work_home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at github.com/fortheinternet',
        'font-weight: bold;'
    );

    // Get URL Data
    const currentUrl = window.location.href
    const urlParts = currentUrl.split('/')

    let creator_username = urlParts[urlParts.length - 3]
    creator_username = decodeURIComponent(creator_username)

    const url = urlParts[urlParts.length - 2]
    const exam_id = urlParts[urlParts.length - 1]

    const main = document.getElementById("main")

    // Get document stuff
    const username_fields = document.querySelectorAll(".username_field")
    const work_display_field = document.getElementById("work_display")
    const exam_display_h4 = document.getElementById("exam_display")

    const view_start = document.getElementById("view_start")
    const view_sessions = document.getElementById("view_sessions")

    const view_sessions_btn = document.getElementById("view_sessions_btn")
    const view_questions_btn = document.getElementById("view_questions_btn")
    const view_settings_btn = document.getElementById("view_settings_btn")

    // Settings

    const make_public = document.getElementById("make_public")
    const make_private = document.getElementById("make_private")
    const is_public = document.getElementById("is_public")
    const is_private = document.getElementById("is_private")

    const clones = document.querySelectorAll('[data-origin="clone"]') 

    exam_details = fetch_exam_details(token, creator_username, url, exam_id)
        .then(exam_details => {
            if (exam_details.error) {
                error = exam_details.error
                console.error(error)

                if (error == "invalid-token") {window.location.href = '/login'; removeCookie("token")}
                if (error == "bad-permissions") {window.location.href = '/home'}
                if (error == "not-exists") {window.location.href = '/home'}
            }

            else {
                const username = exam_details.username
                const exam_display = exam_details.exam_display
                const work_display = exam_details.work_display

                const sessions_data = exam_details.sessions
                const visibility = exam_details.visibility
                const user_id = exam_details.user_id
                const user_role = exam_details.user_role

                // Populate screen
                exam_display_h4.textContent = exam_display

                work_display_field.textContent = work_display

                if (user_role == "work_admin") {
                    view_sessions.style.display = "block"
                    view_sessions_btn.style.display = "block";
                    view_questions_btn.style.display = "block";
                    view_settings_btn.style.display = "block";
                    view_start.style.display = "none"
                }

                console.info("User authenticated successfully as " + username)
                username_fields.forEach(username_field => {
                    username_field.textContent = username
                })

                console.log(visibility)

                if (visibility == "public") {
                    is_public.style.display = "block"
                    make_private.style.display = "block"
                } else {
                    is_private.style.display = "block"
                    make_public.style.display = "block"
                }

                clones.forEach(clone => {
                    clone.remove()
                });
        
                main.style.display = "block"
                document.title = exam_display + " - Chalk"
            }
        })
        
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme:dark)').matches)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }

})

function fetch_exam_details(token, creator_username, url, exam_id) {
    return fetch(`http://localhost:3000/api/exams/${creator_username}/${url}/home.json`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            value: exam_id
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

function toggle(visibility) {
    const token = getCookie("token")

    // Get URL Data
    const currentUrl = window.location.href
    const urlParts = currentUrl.split('/')

    let creator_username = urlParts[urlParts.length - 3]
    creator_username = decodeURIComponent(creator_username)

    const url = urlParts[urlParts.length - 2]
    const exam_id = urlParts[urlParts.length - 1]

    // Toggle loading

    const toggle_loading = document.getElementById("toggle_loading")
    toggle_loading.style.display = "block"

    fetch(`http://localhost:3000/api/exams/${creator_username}/${url}/settings.json`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: "toggle",
                    value: exam_id,
                    token: token
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error == "invalid-token") {
                    window.location.href = '/login';
                    removeCookie("token");
    
                } else {
                    if (visibility == "private") {
                        is_public.style.display = "none"
                        make_private.style.display = "none"
                        
                        is_private.style.display = "block"
                        make_public.style.display = "block"
                    } else {
                        is_private.style.display = "none"
                        make_public.style.display = "none"
                        
                        is_public.style.display = "block"
                        make_private.style.display = "block"
                    }

                    toggle_loading.style.display = "none"
                }
                    
            })
            .catch(error => {
                console.error('Error:', error);
            });
}

function view_sessions() {
    const view_sessions = document.getElementById("view_sessions");
    const view_questions = document.getElementById("view_questions");
    const view_settings = document.getElementById("view_settings");
    
    view_sessions.style.display = "block";
    view_questions.style.display = "none";
    view_settings.style.display = "none";
}

function view_questions() {
    const view_sessions = document.getElementById("view_sessions");
    const view_questions = document.getElementById("view_questions");
    const view_settings = document.getElementById("view_settings");
    
    view_sessions.style.display = "none";
    view_questions.style.display = "block";
    view_settings.style.display = "none";
}

function view_settings() {
    const view_sessions = document.getElementById("view_sessions");
    const view_questions = document.getElementById("view_questions");
    const view_settings = document.getElementById("view_settings");
    
    view_sessions.style.display = "none";
    view_questions.style.display = "none";
    view_settings.style.display = "block";
}

function logout() {
    removeCookie("token")
    window.location.href = '/login';
}

function nav_work() {
    var currentURL = window.location.href;
    var urlSegments = currentURL.split('/');
    urlSegments.pop();
    var newURL = urlSegments.join('/');
    window.location.href = newURL;
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

function navbar(option) {
    const nav = document.querySelector('nav');

    if (option === 'hide' && window.innerWidth <= 1024 ) {
        nav.style.display = "none";
    }
    
    if (option === 'show' && window.innerWidth <= 1024) {
        nav.style.display = "flex";
    }
}

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
