const navBarBurger = document.querySelector("#navBarBurger");
const navBarMenu = document.querySelector("#navBarMenu");

navBarBurger.addEventListener("click", () => {
	navBarMenu.classList.toggle("is-active");
})