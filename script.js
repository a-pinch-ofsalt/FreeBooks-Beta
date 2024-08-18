document.getElementById('bookForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const bookTitle = document.getElementById('bookTitle').value;
    const authorLastName = document.getElementById('authorLastName').value;

    // Store the values in localStorage
    localStorage.setItem('bookTitle', bookTitle);
    localStorage.setItem('authorLastName', authorLastName);
    
    // Redirect to the authorization URL
    window.location.href = 'https://localhost:5000/authorize';
});
