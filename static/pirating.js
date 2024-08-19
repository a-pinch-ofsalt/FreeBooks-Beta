document.addEventListener('DOMContentLoaded', function() {
    // Fetch the book data from the server-side session
    fetch('https://localhost:5000/get_book_info', {
        method: 'GET',
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            if (data.bookTitle && data.authorLastName) {
                document.getElementById('pirateStatus').innerText = `Downloading "${data.bookTitle}" by ${data.authorLastName}...`;
            } else {
                document.getElementById('pirateStatus').innerText = 'No book information available!';
            }
        })
        .catch(error => {
            console.error('Error fetching book info:', error);
            document.getElementById('pirateStatus').innerText = 'An error occurred!';
        });
});
