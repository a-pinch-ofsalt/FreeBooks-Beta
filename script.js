document.getElementById('bookForm').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent any default action

    // Redirect the browser to the Flask route that initiates the OAuth flow
    window.location.href = 'https://localhost:5000/signin';
});
