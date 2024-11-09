function updateFileName(inputId, displayId) {
  const input = document.getElementById(inputId);
  const display = document.getElementById(displayId);
  if (input.files.length > 0) {
    display.textContent = input.files[0].name; // Show the selected file name
  } else {
    display.textContent = ''; // Clear if no file is selected
  }
}

function downloadPDF() {
  const link = document.createElement("a");
  link.href = "zeroOne.pdf";  // Path to your PDF file
  link.download = "Startup Book.pdf";    // The name of the downloaded file
  link.click();
}
