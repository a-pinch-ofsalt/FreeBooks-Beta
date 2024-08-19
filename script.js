document.getElementById('bookForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const bookTitle = document.getElementById('bookTitle').value;
    const authorLastName = document.getElementById('authorLastName').value;

    // Send the data to the backend to store in the session
    fetch('https://localhost:5000/store_book_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: bookTitle, authorLastName: authorLastName }),
        credentials: 'include'
    })
    .then(response => {
        if (response.ok) {
            // Redirect to the pirating page
            window.location.href = 'https://localhost:5000/authorize';
        } else {
            console.error('Failed to store book info');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
