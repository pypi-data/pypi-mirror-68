$(document).ready(function () {
  // $("li:eq(0)").addClass("active");
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");
  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
});
