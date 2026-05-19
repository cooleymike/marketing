document.addEventListener('DOMContentLoaded', function() {

    var myInput = document.getElementById("id_password1");
    // ... your strength code ...
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");
    if (myInput) {
        myInput.onfocus = function () {
            document.getElementById("message").classList.remove("hidden");
        };
        myInput.onblur = function () {
            document.getElementById("message").classList.add("hidden");
        };
        myInput.onkeyup = function () {
            if (!letter || !capital || !number || !length) {
                return;
            }
            // Validate lowercase letters
            var lowerCaseLetters = /[a-z]/g;
            if (myInput.value.match(lowerCaseLetters)) {
                letter.classList.remove("invalid");
                letter.classList.add("valid");
            } else {
                letter.classList.remove("valid");
                letter.classList.add("invalid");
            }

            // Validate capital letters
            var upperCaseLetters = /[A-Z]/g;
            if (myInput.value.match(upperCaseLetters)) {
                capital.classList.remove("invalid");
                capital.classList.add("valid");
            } else {
                capital.classList.remove("valid");
                capital.classList.add("invalid");
            }

            // Validate numbers
            var numbers = /[0-9]/g;
            if (myInput.value.match(numbers)) {
                number.classList.remove("invalid");
                number.classList.add("valid");
            } else {
                number.classList.remove("valid");
                number.classList.add("invalid");
            }

            // Validate length
            if (myInput.value.length >= 8) {
                length.classList.remove("invalid");
                length.classList.add("valid");
            } else {
                length.classList.remove("valid");
                length.classList.add("invalid");
            }

        };
    }
    var myInput2 = document.getElementById("id_password2");
    if (myInput2) {
        myInput2.onkeyup = function () {
            checkMatch();
        }
    }

// Function to check if passwords match
    function checkMatch() {
        var matchStatus = document.getElementById("password-match-status");
        var matchText = document.getElementById("match-text");
        var matchIcon = document.getElementById("match-icon");

        if (myInput.value === myInput2.value && myInput.value !== "") {
            matchStatus.classList.remove("hidden");
            matchIcon.classList.remove("invalid");
            matchIcon.classList.add("valid");
            matchText.textContent = "Passwords Match!";
        } else if (myInput2.value !== "") {
            matchStatus.classList.remove("hidden");
            matchIcon.classList.remove("valid");
            matchIcon.classList.add("invalid");
            matchText.textContent = "Passwords Not Match!";
        } else {
            matchStatus.classList.add("hidden");
        }
    }
});