// Password Match Check
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(event) {
      var password = document.getElementById('password').value;
      var passwordConfirm = document.getElementById('password_confirm').value;
  
      if (password !== passwordConfirm) {
        event.preventDefault();
        alert('Passwords do not match!');
      }
    });
  });
