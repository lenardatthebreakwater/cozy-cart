//for the navbar menu logic on smaller screen devices
const navBarBurger = document.querySelector("#navBarBurger");
const navBarMenu = document.querySelector("#navBarMenu");

navBarBurger.addEventListener("click", () => {
	navBarMenu.classList.toggle("is-active");
})


//for checkout form logic
const checkoutForm = document.querySelector("#checkoutForm")
const checkoutFormOpenBtn = document.querySelector("#checkoutFormOpenBtn")
const checkoutFormCloseBtn = document.querySelector("#checkoutFormCloseBtn")

checkoutFormOpenBtn.addEventListener("click", (e) => {
	e.preventDefault()
	checkoutForm.classList.add("is-active")
})

checkoutFormCloseBtn.addEventListener("click", (e) => {
	e.preventDefault()
	checkoutForm.classList.remove("is-active")
})
