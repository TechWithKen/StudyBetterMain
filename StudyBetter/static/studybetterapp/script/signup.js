const togglePassword = document.getElementById('togglePassword');
const passwordField = document.getElementById('password');

// Add an event listener to the checkbox to toggle visibility
togglePassword.addEventListener('change', function () {
    // Check the state of the checkbox to determine visibility
    passwordField.type = this.checked ? 'text' : 'password';
});