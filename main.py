from flask import Flask, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from libgenScraper import download_epub
import os

app = Flask(__name__)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = "client_secret.json"
app.secret_key = os.urandom(24)

@app.route('/authorize')
def authorize():
    print("Someone is asking for authorization!")
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
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
    return redirect('/pirating.html')


@app.route('/pirate_book', methods=['POST'])
def pirate_book():
    print("AYEE WEVE GOT A FILTHY PIRATE EH")
    title = request.json.get('title')
    author_last_name = request.json.get('authorLastName')
    
    # Download the book using libgenScraper's download_epub function
    file_path = download_epub(title, author_last_name)
    print(f'file_path = {file_path}')
    
    if not file_path:
        return jsonify({'message': 'Book not found'}), 404

    # Now upload the downloaded file to Google Drive
    if not session['credentials']:
        return redirect(url_for('authorize'))

    drive_service = build('drive', 'v3', credentials=session['credentials'])
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

if __name__ == '__main__':
    app.run(port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))