document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('loginForm');
  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Validate the email field
    var emailInput = document.getElementById('email');
    if (!emailInput.checkValidity()) {
      alert('Please enter a valid email address.');
      return;
    }

    // Disable the submit button
    var submitButton = document.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    // Send the verification email using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          alert('Verification email sent successfully.');
        } else {
          alert('Failed to send verification email. Please try again later.');
        }
        submitButton.disabled = false;
      }
    };
    xhr.send(new FormData(form));
  });
});
