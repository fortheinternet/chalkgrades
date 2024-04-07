document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'exam_home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const token = getCookie("token")

    if (token) {
        load_examhomedotjson()
    } else {
        window.location.href = '/login';
    }
})

const token = getCookie("token")

function load_examhomedotjson() {
    const username_fields = document.querySelectorAll(".username_field")
    const work_user = document.getElementById("work_user")
    const work_url = document.getElementById("work_url")
    const work_display = document.getElementById("work_display")

    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');

    let creator_username = urlParts[urlParts.length - 3];
    creator_username = decodeURIComponent(creator_username)

    const url = urlParts[urlParts.length - 2];
    const exam_id = urlParts[urlParts.length - 1]

    const main = document.getElementById("main")

    fetch(`https://chalk.fortheinternet.xyz/api/exams/${creator_username}/${url}/home.json`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: token,
                    exam_id: exam_id
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error == "w-mal-25-1") {
                    window.location.href = '/login';
                    removeCookie("token");
    
                } else if (data.error == "w-mal-4000") {
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
                    
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
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