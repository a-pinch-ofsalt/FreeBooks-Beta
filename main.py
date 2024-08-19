from flask import Flask, request, redirect, url_for, session, jsonify, render_template, send_file
from flask_cors import CORS
from flask_cors import cross_origin
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from libgenScraper import download_epub
import os
from google.oauth2.credentials import Credentials
from flask_session import Session
import requests
from google.oauth2.credentials import Credentials



app = Flask(__name__)
CORS(app, supports_credentials=True)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = "client_secret.json"
app.secret_key = os.urandom(64)

@app.route('/signin', methods=['GET'])
def authorize():
    print('hola!')

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Get the authorization code from Google
    auth_code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': auth_code,
        'client_id': '1005985003754-tge3gduo7qd6rtveknhajeehor8u012p.apps.googleusercontent.com',
        'client_secret': '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',
        'redirect_uri': url_for('oauth2callback', _external=True),
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(token_url, data=token_data)
    token_info = token_response.json()

    if 'error' in token_info:
        return f"An error occurred: {token_info['error_description']}"

    # Convert the token_info into a Credentials object
    credentials = Credentials(
        token=token_info['access_token'],
        refresh_token=token_info.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        scopes=['https://www.googleapis.com/auth/drive.file']
    )

    # Store the credentials in the session for later use
    session['credentials'] = credentials_to_dict(credentials)

    # Redirect the user to the book selection page
    return render_template('pirate.html', credentials=credentials_to_dict(credentials))

def credentials_to_dict(credentials):
    """Helper function to serialize credentials into a dictionary."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
"""
@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    # Redirect to the new pirating page
    return render_template('pirate.html')
"""
@app.route('/pirate_book', methods=['GET', 'POST'])
def pirate_book():
    print("YES")
    data = request.json
    book_title = data.get('title')
    author_last_name = data.get('authorLastName')
    credentials = data.get('credentials')
    print(f"BOIS WE DID IT. book_title book_title= {book_title}, author_last_name = {author_last_name}, credentials = {credentials}.")
    return 'lmao'

"""

@app.route('/get_book_info', methods=['GET'])
def get_book_info():
    # Retrieve the data from the session
    book_title = session.get('book_title', 'Unknown Title')
    author_last_name = session.get('author_last_name', 'Unknown Author')
    
    # Debugging: Print the retrieved data
    print(f"Retrieved from session: Title = {book_title}, Author = {author_last_name}")
    
    return jsonify({
        'bookTitle': book_title,
        'authorLastName': author_last_name
    })

@app.route('/pirate_book', methods=['POST'])
def pirate_book():
    # Get credentials from session and convert back to Credentials object
    credentials = credentials_from_dict(session['credentials'])
    print("AYEE WEVE GOT A FILTHY PIRATE EH")
    
    data = request.json
    book_title = data.get('title')
    author_last_name = data.get('authorLastName')
    
    # Process the data as needed
    print(f"Received Book Title: {book_title}")
    print(f"Received Author Last Name: {author_last_name}")
    
    # Download the book using libgenScraper's download_epub function
    file_path = download_epub(book_title, author_last_name)
    print(f'file_path = {file_path}')
    
    if not file_path:
        return jsonify({'message': 'Book not found'}), 404

    # Now upload the downloaded file to Google Drive
    if not session['credentials']:
        return redirect(url_for('authorize'))

    drive_service = build('drive', 'v3', credentials=credentials)
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='application/epub+zip')

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return jsonify({'message': 'File uploaded successfully!', 'fileId': file.get('id')})

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def credentials_from_dict(data):
    return Credentials(
        token=data.get('token'),
        refresh_token=data.get('refresh_token'),
        token_uri=data.get('token_uri'),
        client_id=data.get('client_id'),
        client_secret=data.get('client_secret'),
        scopes=data.get('scopes')
    )
"""

if __name__ == '__main__':
    app.run(port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
    




"""@app.route('/book_selection')
def book_selection():
    # Render the book selection page
    return render_template('pirate.html')

@app.route('/upload_book', methods=['POST'])
def upload_book():
    # Get book info from the form
    book_title = request.form.get('bookTitle')
    author_last_name = request.form.get('authorLastName')
    
    # Get the credentials from the session
    credentials = session.get('credentials')
    
    if not credentials:
        return jsonify({"error": "No credentials found. Please sign in again."}), 401
    
    # Download the book using the provided title and author
    file_path = download_epub(book_title, author_last_name)
    
    # Upload the book to Google Drive using the credentials and the file path
    success = upload_book_to_google_drive(credentials, file_path)
    
    if success:
        return "Book uploaded successfully!"
    else:
        return "Failed to upload the book.", 500"""