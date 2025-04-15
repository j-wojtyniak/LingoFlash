"use strict";

function handleFileUpload() {
  const fileInput = document.querySelector("#file-upload");
  const fileName = document.querySelector(".file-name");

  fileInput?.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      fileName.textContent = fileInput.files[0].name;
    } else {
      fileName.textContent = "No file chosen";
    }
  });
}

function handleFlashCardFeedback() {
  const soundCorrect = new Audio("static/sounds/correct.mp3");
  const soundWrong = new Audio("static/sounds/incorrect.mp3");
  const soundReveal = new Audio("static/sounds/reveal.mp3");

  const card = document.querySelector(".top-rectangle");
  const word = document.querySelector(".app-name--flashcard");

  const status = card.dataset.status;

  if (!card || !word) {
    return;
  }

  if (status === "correct") {
    card.style.backgroundColor = "#4CAF50";
    word.textContent = "Correct!";
    soundCorrect.play();
  }
  if (status === "incorrect") {
    card.style.backgroundColor = "#E53935";
    word.textContent = "Incorrect!";
    soundWrong.play();
  }

  if (status === "correct" || status === "incorrect") {
    setTimeout(() => {
      window.location.href = "/flashcard";
    }, 1500);
  }

  const buttonReveal = document.querySelector("#button-reveal");
  buttonReveal.addEventListener("click", () => {
    word.textContent = word.dataset.answer;
    card.style.backgroundColor = "#9F58F6";
    soundReveal.play();

    setTimeout(() => {
      window.location.href = "/flashcard";
    }, 1500);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  console.log("DOM ZALADOWANY");
  handleFileUpload();
  handleFlashCardFeedback();
});
