let timerInterval;
let seconds = 0;

function startTimer() {
  stopTimer(); // Hentikan timer sebelumnya
  seconds = 0;
  const timerDisplay = document.getElementById("timer");
  timerInterval = setInterval(() => {
    seconds++;
    const mins = Math.floor(seconds / 60)
      .toString()
      .padStart(2, "0");
    const secs = (seconds % 60).toString().padStart(2, "0");
    timerDisplay.textContent = `${mins}:${secs}`;
  }, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
}

function handleNewGame() {
  localStorage.setItem("startNewGame", "true");
}

function checkAndStartTimer() {
  if (localStorage.getItem("startNewGame") === "true") {
    localStorage.setItem("startNewGame", "false");
    startTimer();
  }
}

function handleFormSubmit(event) {
  const timerInput = document.getElementById("time_taken");
  timerInput.value = seconds; // Kirim waktu ke server
  stopTimer();
}

document.addEventListener("DOMContentLoaded", () => {
  checkAndStartTimer();
});
