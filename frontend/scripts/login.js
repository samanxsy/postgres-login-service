/* J a v a S c r i p t */
/* Login form submission and POST request handler */

// Login request handle
$(document).ready(function() {
    $('form').submit(function(event) {
      event.preventDefault(); // Prevent the default form submission
  
      // Get the form data
      var formData = {
        username: $('#username').val(),
        password: $('#password').val()
      };
  
      // Send the AJAX request
      $.ajax({
        type: 'POST',
        url: '/loginapi',
        data: JSON.stringify(formData), // Convert the data to JSON
        contentType: 'application/json', // Set the request content type to JSON
        success: function(response) {
          // Clear previous error message
          $('#backend-message').empty();
        
          if (response.status === false) {
            // Display error message
            $('#backend-message').text(response.backend_message);
          } else {
            var loggedInUser = response.username;
            localStorage.setItem('LoggedInUser', loggedInUser);
            window.location.href = '/profile.html';
          }
        },
        error: function() {
          // Handle error
          $('#backend-message').text('An error occurred during login.');
        }
      });
    });
  });
