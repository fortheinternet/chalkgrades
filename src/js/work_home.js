document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'work_home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/pvcsd',
        'font-weight: bold;'
    );

    const user_token = getCookie("token")

    if(user_token) {
        load_workhomedotjson()
    } else {
        window.location.href = '/login';
    }
})

function load_workhomedotjson() {
    const membersDiv = document.getElementById("members")
    const memberDiv = document.getElementById("member")

    const username_field = document.getElementById("username_field")
    const work_user = document.getElementById("work_user")
    const work_url = document.getElementById("work_url")
    const work_display = document.getElementById("work_display")

    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');

    const creator_username = urlParts[urlParts.length - 2];
    const url = urlParts[urlParts.length - 1];

    const user_token = getCookie("token")
    const userData = {token: user_token}

    fetch(`http://localhost:3000/api/work/${creator_username}/${url}/home.json`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error === "w-mal-25-1") {
                window.location.href = '/login';
                removeCookie("token");

            } else if (data.error === "w-mal-25-11") {
                window.location.href = 'https://en.wikipedia.org/wiki/HTTP_404';

            } else {
                console.info("User authenticated successfully as " + data.username)
                username_field.textContent = data.username;
                work_display.textContent = data.display;

                work_user.textContent = creator_username;
                work_url.textContent = url;

                const members_data = data.members;
                
                membersDiv.innerHTML = '';

                members_data.forEach(member => {
                    const { username, role } = member;

                    const memberClone = memberDiv.cloneNode(true);
                    memberClone.style.display = "block";

                    memberClone.querySelector("#member_user").textContent = username;
                    memberClone.querySelector("#member_role").textContent = role;

                    membersDiv.appendChild(memberClone);
                });
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
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function removeCookie(cname) {
    document.cookie = cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=None; Secure";
}