subMenu = document.getElementById("subMenu");
navPic = document.getElementById("nav-pic");

navPic.addEventListener("click", toggleMenu);

function toggleMenu(){
    subMenu.classList.toggle("open-menu");
}
