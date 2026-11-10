document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".message").forEach((message) => {
    window.setTimeout(() => { message.style.opacity = "0"; message.style.transition = "opacity .4s"; }, 4500);
  });
});
