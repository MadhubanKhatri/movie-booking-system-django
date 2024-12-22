// let username = document.getElementById('name')
// let contact_num = document.getElementById('contact_num')
// let email = document.getElementById('email')
// let password = document.getElementById('password')
// let isValidated = false;

function validateForm() {
    // Get input values
    const username = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const contact = document.getElementById("contact_num").value;
    const password = document.getElementById("password").value;
    const submitButton = document.getElementById("register_btn");

    // Validation checks
    const isUsernameValid = username.length >= 8;
    const isEmailValid = email.includes("@");
    const isContactValid = /^\d{10}$/.test(contact);
    const isPasswordValid = password.length >= 12;

    // Enable or disable the button based on validation
    if (isUsernameValid && isEmailValid && isContactValid && isPasswordValid) {
        submitButton.removeAttribute("disabled");
    } else {
        submitButton.setAttribute("disabled", "true");
    }
}