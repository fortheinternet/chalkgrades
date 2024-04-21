document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'login.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const token = getCookie("token")

    if (token) {
        window.location.href = '/home';
    }

    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme:dark)').matches)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }

    const main = document.getElementById("main")
    main.style.display = "flex"
})

const token = getCookie("token")

function login_submit() {
    const usernameInput = document.getElementById('login_username');
    const passwordInput = document.getElementById('login_password');

    fetch('https://chalk.fortheinternet.xyz/api/logins/logins.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: usernameInput.value,
            password: passwordInput.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("ISSUE: " + data.message)
            console.error(data.error + " - " + data.message)    
        }
        
        setCookie("token", data.token);
        window.location.href = '/home';
        
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

    fetch('https://chalk.fortheinternet.xyz/api/logins/signups.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: usernameInput.value,
            password: passwordInput.value,
            password_confirm: passwordConfirmInput.value,
            accesskey: accessInput.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("ISSUE: " + data.message)
            console.error(data.error + " - " + data.message)    
        }

        setCookie("token", data.token);
        window.location.href = '/home';
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function nav_viewlanding(lang) {
    if (lang == 'hu') {
        window.location.href = '/?lang=hu'
    } else {
        window.location.href = '/?lang=en'
    }
}

function nav_loginsignup() {
    console.log("You are already there!")
}

function nav_viewdocuments() {
    window.location.href = '';
}

function nav_viewrepository() {
    window.location.href = 'https://github.com/fortheinternet/chalkgrades';
}

function nav_changelang(lang) {
    if (lang == 'hu') {
        window.location.href = '/login?lang=hu'
    } else {
        window.location.href = '/login?lang=en'
    }
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
