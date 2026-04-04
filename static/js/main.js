console.log("main.js loaded");

// JavaScript for character count in story and comment textareas
function setupCounter(textareaId, counterId) {
  const textarea = document.getElementById(textareaId);
  const counter = document.getElementById(counterId);
    // If either the textarea or counter element is not found, exit the function
  if (!textarea || !counter) return;
// Update the counter with the current length of the textarea content
  function updateCount() {
    counter.textContent = textarea.value.length;
  }
// Add an event listener to the textarea to update the counter on input
  textarea.addEventListener("input", updateCount);
  updateCount();
}
// Initialize the counters when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function () {
  setupCounter("story-text", "story-count");
  setupCounter("comment-text", "comment-count");
});


// JavaScript for star rating in comment form
document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll("#star-rating span");
  const input = document.querySelector("input[name='rating']");
// Add click event listeners to each star
  stars.forEach((star) => {
    star.addEventListener("click", function () {
      const value = this.getAttribute("data-value");
      input.value = value;
// Update the star display based on the selected rating
      stars.forEach((s, index) => {
        s.textContent = index < value ? "★" : "☆";
      });
    });
  });
});