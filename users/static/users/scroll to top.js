var btt = document.getElementById("back-to-top"),

body = document.body,
docElem = document.documentElement,
offset = 100,
scrollPos, docHeight, 
isFirefox = navigator.userAgent.toLowerCase().indexOf("safari") > -1;

//Calculate document height
docHeight = Math.max (body.scrollHeight, body.offsetHeight, docElem.clientHeight, docElem.scrollHeight, docElem.offsetHeight);
if (docHeight != 'undefined') {
    offset = docHeight/4;
}

//Add scroll event listener
window.addEventListener("scroll", function(event){
    scrollPos = body.scrollTop || docElem.scrollTop;

    btt.className = (scrollPos > offset) ? "visible" : "";
});

//Add scroll event listener
btt.addEventListener("click",function(event){
    event.preventDefault();

    if(isFirefox){
        docElem.scrollTop = 0;
    } body.scrollTop = 0;
});