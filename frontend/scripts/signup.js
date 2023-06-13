/* J a v a S c r i p t */
/* Signup form submission and POST request handler */

// Signup request handle
$(document).ready(function() {
    $('form').submit(function(event) {
      event.preventDefault(); // Prevent the default form submission
  
      // Get the form data
      var formData = {
        first_name: $('#first_name').val(),
        last_name: $('#last_name').val(),
        email: $('#email').val(),
        username: $('#username').val(),
        password: $('#password').val(),
        password_confirm: $('#password_confirm').val(),
        date_of_birth: $('#date_of_birth').val()
      };
  
      // Send the AJAX request
      $.ajax({
        type: 'POST',
        url: '/signupapi', // Relative path
        data: JSON.stringify(formData), // Convert the data to JSON
        contentType: 'application/json', // Set the request content type to JSON
        xhrFields: {
          withCredentials: true // Enable sending cookies with the request
        },
        success: function(response) {
          // Clear previous messages
          $('#backend-message').empty();

          if (response.backend_message === "success" && response.status === true) {
            // Display success message
            $('#backend-message').text(response.backend_message);
          // deepcode ignore DuplicateIfBody: <This will return a different message from backend and its not duplicated>
          } else {
            // Display error message
            $('#backend-message').text(response.backend_message);
          }
        },
        error: function() {
          // Handle error
          $('#backend-message').text('An error occurred during signup.');
        }
      });
    });
  });
