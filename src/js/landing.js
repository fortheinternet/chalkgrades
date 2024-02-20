document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'landing.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );
})

function nav_loginsignup() {
    window.location.href = '/login';
}

function nav_viewdocuments() {
    window.location.href = 'http://carpaltunnel.notion.site/About-the-project-375b56b34c8c44b8b5d233be4a36e9a5?pvs=73';
}

function nav_viewrepository() {
    window.location.href = 'http://github.com/thelocaltemp/chalkgrades';
}