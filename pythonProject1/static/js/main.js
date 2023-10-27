/* Full Screen */
const fullscreenButton = document.getElementById('VLXD-header__full');
const htmlElement = document.documentElement;

fullscreenButton.addEventListener('click', () => {
  if (document.fullscreenElement) {
	document.exitFullscreen();
  } else {
	htmlElement.requestFullscreen();
  }
});


/* Dark Mode */
const button = document.getElementById("VLXD-dark-light-button");
const action = document.querySelectorAll("#VLXD-sidebarmenu__dark, #VLXD-dark-light");

button.addEventListener("click", function() {
    action.forEach((el) => {
        el.classList.toggle("active");
    });
    localStorage.setItem("isDark", action[0].classList.contains("active"));
});

if (localStorage.getItem("isDark") === "true") {
    action.forEach((el) => {
        el.classList.add("active");
    });
}




/* VLXD Sidebar Menu */
const cs_button = document.querySelectorAll(".VLXD__sicon");
const cs_action = document.querySelectorAll(".VLXD-smenu, .VLXD-header, .VLXD-adashboard");

cs_button.forEach(button => {
    button.addEventListener("click", function() {
        cs_action.forEach((el) => {
            el.classList.toggle("VLXD-close");
        });
        localStorage.setItem("iscicon", cs_action[0].classList.contains("VLXD-close"));
    });
});

if (localStorage.getItem("iscicon") === "true") {
    cs_action.forEach((el) => {
        el.classList.add("VLXD-close");
    });
}

