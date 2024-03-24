document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'landing.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/thelocaltemp',
        'font-weight: bold;'
    );
})

function nav_viewlanding() {
    console.log("You are already there!")
}

function nav_loginsignup() {
    window.location.href = '/login';
}

function nav_viewdocuments() {
    window.location.href = 'https://fortheinternet.notion.site/chalkgrades-documentation-a264ead5fa0542f7938d76ed67e45667?pvs=4';
}

function nav_viewrepository() {
    window.location.href = 'https://github.com/fortheinternet/chalkgrades';
}