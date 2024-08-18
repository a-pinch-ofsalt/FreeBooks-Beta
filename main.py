from flask import Flask, jsonify, request, redirect, url_for
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

from libgenScraper import search_libgen, download_epub
from driveUploader import upload_book_to_google_drive

app = Flask(__name__)

CLIENT_SECRETS_FILE = 'google-api-keys/client_secret.json'

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/drive.file'],
        redirect_uri='http://localhost:5000/callback'
    )
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/drive.file'],
        redirect_uri='http://localhost:5000/callback'
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    service = build('drive', 'v3', credentials=credentials)
    
    return 'Logged in successfully. Ready to upload.'

@app.route('/pirate_book', methods=['POST'])
def pirate_book():
    data = request.get_json()  # Extract data from request body
    title = data.get('title')
    authorLastName = data.get('authorLastName')
    
    download_link = search_libgen(title, authorLastName)
    if download_link:
        file_path = download_epub(download_link)
        if file_path:
            result = upload_book_to_google_drive(file_path)
            if result:
                return jsonify({'status': 'success', 'message': 'File uploaded to Google Drive successfully!'})
            else:
                return jsonify({'status': 'error', 'message': 'Failed to upload to Google Drive.'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to download EPUB file.'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to find a valid download link.'})

if __name__ == '__main__':
    app.run(debug=True)
