document.getElementById('requestButton').addEventListener('click', function() {
    fetch('/run-python-script', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'An error occurred!';
    });
});
