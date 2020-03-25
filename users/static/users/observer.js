const header = document.getElementsByClassName(".nav-bar");
const sectionOne = document.getElementsByClassName(".header");

const sectionOneOptions = {
    rootMargin: "-200px 0px 0px 0px"
};
const sectionOneObserver = new IntersectionObserver(function (entries, sectionOneObserver) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            header.classList.remove("nav-bar");
            header.classList.add("nav-scrolled");
        } else {
            header.classList.remove("nav-scrolled");
            header.classList.add("nav-bar");
        }
    });
}, sectionOneOptions);

sectionOneObserver.observe(sectionOne);