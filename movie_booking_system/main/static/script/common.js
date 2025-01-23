function validateForm() {
    // Get input values
    const username = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const contact = document.getElementById("contact_num").value;
    const password = document.getElementById("password").value;
    const submitButton = document.getElementById("register_btn");
    const listItems = document.querySelectorAll('.list_container ul li');

    // Validation checks
    const isUsernameValid = username.length >= 8;
    const isEmailValid = email.includes("@");
    const isContactValid = /^\d{10}$/.test(contact);
    const isPasswordValid = password.length >= 12;
    
    if(username){
        (username.length < 8) ? listItems[0].style.color = 'red' : listItems[0].style.color = '#32CD32'; 
    }
    if(email){
        (!isEmailValid) ? listItems[1].style.color = 'red' : listItems[1].style.color = '#32CD32'; 
    }
    if(contact){
        (!isContactValid) ? listItems[2].style.color = 'red' : listItems[2].style.color = '#32CD32'; 
    }
    if(password){
        (!isPasswordValid) ? listItems[3].style.color = 'red' : listItems[3].style.color = '#32CD32'; 
    }
    // Enable or disable the button based on validation
    if (isUsernameValid && isEmailValid && isContactValid && isPasswordValid) {
        submitButton.removeAttribute("disabled");
    } else {
        submitButton.setAttribute("disabled", "true");
    }
}