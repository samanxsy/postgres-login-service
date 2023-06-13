/* J a v a s C r i p t */
/* Session Authentication and profile content loading */

$(document).ready(function() {
  // Check if the user is authenticated
  var username = localStorage.getItem('LoggedInUser');

  $.ajax({
    type: 'POST',
    url: '/auth',
    data: JSON.stringify({"username": username}),
    contentType: 'application/json',
    success: function(response) {
      if (response.status === true) {
        // User is authenticated, load the username
        $("#username").text(response.username);
        $('#welcome-message').text('Welcome, ' + username + '!');
      } else {
        // User is not authenticated, redirect to login page
        window.location.href = '/login.html';
      }
    },
    error: function() {
      // Handle error
      console.error('An error occurred during authentication.');
    }
  });
});
