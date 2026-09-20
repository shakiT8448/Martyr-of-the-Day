function closePopup() {
  const popup = document.getElementById("dailyPopup");

  if (popup) {
    popup.style.display = "none";
  }
}
document.addEventListener("DOMContentLoaded", function () {
  const closeButton = document.getElementById("closePopupButton");
  const popup = document.getElementById("dailyPopup");

  if (closeButton && popup) {
    closeButton.addEventListener("click", function () {
      popup.style.display = "none";
    });
  }
});
