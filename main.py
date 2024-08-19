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

app = Flask(__name__)
CORS(app)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = "client_secret.json"
app.secret_key = "1234"

# Configure the session to use filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'  # Directory to store session files

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # or 'None' if needed for cross-origin
app.config['SESSION_COOKIE_SECURE'] = False    # Set to True if using HTTPS

@app.route('/store_book_info', methods=['POST'])
def store_book_info():
    print("help")
    data = request.json
    session['book_title'] = data.get('title')
    session['author_last_name'] = data.get('authorLastName')
    
    print(f"Stored in session: {session['book_title']} by {session['author_last_name']}")
    
    return jsonify({'message': 'Book info stored successfully'})

@app.route('/authorize')
def authorize():

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

    # Redirect to Google's OAuth consent page
    return redirect(authorization_url)



@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    # Redirect to the new pirating page
    return render_template('pirating.html')

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


if __name__ == '__main__':
    app.run(port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))