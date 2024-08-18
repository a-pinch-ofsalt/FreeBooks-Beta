document.addEventListener('DOMContentLoaded', function() {
    const bookTitle = localStorage.getItem('bookTitle');
    const authorLastName = localStorage.getItem('authorLastName');

    if (bookTitle && authorLastName) {
        document.getElementById('pirateStatus').innerText = `Downloading "${bookTitle}" by ${authorLastName}...`;

        fetch('https://localhost:5000/pirate_book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: bookTitle, authorLastName: authorLastName }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById('pirateStatus').innerText = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('pirateStatus').innerText = 'An error occurred during the pirating process!';
        });
    } else {
        document.getElementById('pirateStatus').innerText = 'No book information available!';
    }
});
