document.getElementById('submit').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default form submission
    // Get the book title and author last name from the form fields
    const bookTitle = document.getElementById('bookTitle').value;
    const authorLastName = document.getElementById('authorLastName').textContent;

    // Assuming the token_info is stored as a data attribute or retrieved from a session
    const credentials = document.getElementById('access').textContent;
    alert(`token_info = ${credentials}`)

    // Prepare the data to be sent in the request
    const requestData = {
        title: bookTitle,
        authorLastName: authorLastName,
        credentials: credentials
    };

    // Send the data to the server
    fetch('https://freebooks-b7fl.onrender.com/pirate_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
        credentials: 'include'  // Ensure cookies are included in the request
    })
    .then(response => response.json())
    .then(response => {
        if (response.ok) {
            console.log('Success:', data);
            return response.json();
        } else {
            throw new Error('Failed to upload the book');
        }
    })
    .then(data => {
        // Handle success (data contains the server response)
        console.log('Book uploaded successfully:', data);
    })
    .catch(error => {
        // Handle errors
        console.error('Error:', error);
    });
});
