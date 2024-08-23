document.getElementById('bookForm').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent any default action
    /*
    fetch('http://localhost:8001/signin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: 'I am a banana!' })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success: ', data);
    })
    .catch((error) => {
        console.error('Error: ', error);
    })
*/
    // Redirect the browser to the Flask route that initiates the OAuth flow
    window.location.href = 'https://freebooks-beta.vercel.app/signin';
});
