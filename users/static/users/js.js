const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".right-nav-bar");
const links = document.querySelectorAll(".nav-links");


hamburger.addEventListener('click', () => {
    navLinks.classList.toggle("open");
    links.forEach(link => {
        link.classList.toggle("fade");
    });
});