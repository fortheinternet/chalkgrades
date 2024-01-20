document.addEventListener("DOMContentLoaded", function() {
    console.info("INFORMATION: Loading of JavaScript file 'landing.js' was successful.")
    console.warn(
        '%cWARNING: Pasting any script into this console will give attackers access to your account authentication details. If you know what you are doing you should come working here, details at read.cv/pvcsd',
        'font-weight: bold;'
    );
})

function nav_loginsignup() {
    window.location.href = '/login';
}

function nav_viewdocuments() {
    window.location.href = 'http://diamond-range-a70.notion.site/API-Documentation-05975f405fa64aba85871eb976e63832';
}