from flask import Flask, request, redirect, url_for, session, jsonify, render_template, send_file
from flask_cors import CORS
from flask_cors import cross_origin
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from libgenScraper import download_epub
from driveUploader import upload_book_to_google_drive
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

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@app.route('/signin', methods=['GET'])
def authorize():
    print('hola!')

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='online',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Recreate the flow object
    print(f"Request URL: {request.url}")
    print(f"Request arguments: {request.args}")
    print(f"Session state: {session.get('state')}")
    
    if 'code' not in request.args:
        return "Missing authorization code. Please try the sign-in process again."
    
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    
    
    # Debugging: Print the URL received
    print(f"Callback URL received: {request.url}")
    """
        # Ensure that the code is in the URL
    if 'code' not in request.args:
        return "Missing authorization code. Please try the sign-in process again."""
    client_secret = "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"
    # Exchange the authorization code for an access token
    flow.fetch_token(authorization_response=request.url, client_secret=client_secret, code=request.args.get('code'), state=session['state'])

    # Get credentials and store them in the session
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    
    print(f'CODE IS LITERALLY {request.args.get("code")}')

    # Redirect to the book selection page
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

@app.route('/pirate_book', methods=['GET', 'POST'])
def pirate_book():
    print("YES")
    data = request.json
    book_title = data.get('title')
    author_last_name = data.get('authorLastName')
    credentials = data.get('credentials')
    
    epub_filepath = download_epub(book_title, author_last_name)
    if (epub_filepath == None):
        print("File was not found.")
        return "File was not found"
    else:
        if (epub_filepath == 504):
            print("Servers are down right now.")
            return "Servers are down right now."
        print(f"epub_filepath = {epub_filepath}")
        upload_book_to_google_drive(epub_filepath, credentials)
        return "Success!"
        
    
if __name__ == '__main__':
    app.run(port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))