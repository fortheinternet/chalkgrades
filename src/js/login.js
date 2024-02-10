document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'login.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const user_token = getCookie("token")

    if(user_token) {
        window.location.href = '/home';
    }
})

function login_submit() {
    const usernameInput = document.getElementById('login_username');
    const passwordInput = document.getElementById('login_password');
    const loginErrors = document.getElementById('login_errors')

    const userData = {username: usernameInput.value, password: passwordInput.value}; 

    fetch('https://chalkgrades.vercel.app/api/logins/logins.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            loginErrors.textContent = data.message;
        } else {
            loginErrors.textContent = "";
            setCookie("token", data.token);
            window.location.href = '/home';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function signup_submit() {
    const usernameInput = document.getElementById('signup_username');
    const passwordInput = document.getElementById('signup_password');
    const passwordConfirmInput = document.getElementById('signup_repassword');
    const accessInput = document.getElementById('signup_access');
    const signupErrors = document.getElementById('signup_errors')

    const userData = {username: usernameInput.value, password: passwordInput.value, password_confirm: passwordConfirmInput.value, accesskey: accessInput.value};

    fetch('https://chalkgrades.vercel.app/api/logins/signups.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            signupErrors.textContent = data.message;
        } else {
            signupErrors.textContent = "";
            setCookie("token", data.token);
            window.location.href = '/home';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function nav_viewsignup() {
    const login = document.getElementById("login")
    const signups = document.getElementById("signups")

    login.style.display = "none"
    signups.style.display = "block"
}

function nav_viewlogin() {
    const login = document.getElementById("login")
    const signups = document.getElementById("signups")

    login.style.display = "block"
    signups.style.display = "none"
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