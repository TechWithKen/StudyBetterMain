const animatedText = document.getElementById("animated-text");
const placeMessage = "Upload your study materials and let us "
const messages = [
  "Upload your study materials and let us predict your exam questions!",
  "Upload your study materials and let us summarize it for you!",
  "Upload your study materials and let us help you pass!"
];

let messageIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typingSpeed = 50;  // Typing speed
let deletingSpeed = 50;  // Deleting speed
let pauseDuration = 1500; // Pause between messages

function typeMessage() {
  const currentMessage = messages[messageIndex];

  if (isDeleting) {
    animatedText.textContent = currentMessage.slice(0, charIndex--);
    if (charIndex === 28) {
      isDeleting = false;
      messageIndex = (messageIndex + 1) % messages.length ;
      setTimeout(typeMessage, typingSpeed);
    } else {
      setTimeout(typeMessage, deletingSpeed);
    }
  } else {
    animatedText.textContent = currentMessage.slice(0, charIndex++);
    if (charIndex === currentMessage.length) {
      isDeleting = true;
      setTimeout(typeMessage, pauseDuration);
    } else {
      setTimeout(typeMessage, typingSpeed);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => typeMessage());
