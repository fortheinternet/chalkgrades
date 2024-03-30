document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'exam_home.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const user_token = getCookie("token")

    if (user_token) {
        load_examhomedotjson()
    } else {
        window.location.href = '/login';
    }
})

let alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

function load_examhomedotjson() {
    const username_fields = document.querySelectorAll(".username_field")
    const work_user = document.getElementById("work_user")
    const work_url = document.getElementById("work_url")
    const work_display = document.getElementById("work_display")

    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');

    let creator_username = urlParts[urlParts.length - 2];
    creator_username = decodeURIComponent(creator_username)

    const url = urlParts[urlParts.length - 1];

    const user_token = getCookie("token")
    const userData = {token: user_token}

    const main = document.getElementById("main")
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