document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'landing.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );

    const main = document.getElementById("main")
    main.style.display = "flex"

    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme:dark)').matches)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
})

function nav_viewlanding() {
    console.log("You are already there!")
}

function nav_loginsignup(lang) {
    if (lang == 'hu') {
        window.location.href = '/login?lang=hu'
    } else {
        window.location.href = '/login?lang=en'
    }
}

function nav_viewdocuments() {
    window.location.href = 'https://fortheinternet.notion.site/chalkgrades-documentation-a264ead5fa0542f7938d76ed67e45667?pvs=4';
}

function nav_viewrepository() {
    window.location.href = 'https://github.com/fortheinternet/chalkgrades';
}

function nav_changelang(lang) {
    if (lang == 'hu') {
        window.location.href = '/?lang=hu'
    } else {
        window.location.href = '/?lang=en'
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