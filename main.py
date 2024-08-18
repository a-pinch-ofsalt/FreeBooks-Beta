import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import google.auth
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from flask import Flask, jsonify

app = Flask(__name__)

CLIENT_SECRETS_FILE = 'google-api-keys/client_secret.json'


@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/drive.file'],
        redirect_uri='http://localhost:5000/callback'
    )

@app.route('/login')
def pirate_book(title, authorLastName):










def search_libgen(title, authorLastName):
    search_url = "https://libgen.li/index.php"
    params = {
        'req': f"{title} {authorLastName}",
        'res': 25,
        'column': 'def',
        'view': 'simple',
        'phrase': 1,
        'sort': 'year',
        'sortmode': 'DESC'
    }

    response = requests.get(search_url, params=params)
      
    if response.status_code != 200:
        if response.status_code == 504:
            return 504
        else:
            return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'tablelibgen'})

    if not table:
        return None

    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) > 8:
            if 'epub' in columns[-2].text.lower():  # Check if the format is EPUB
                first_mirror_link = columns[-1].find_all('a')[0]['href']  # Get the first mirror link
                mirror_url = urljoin(search_url, first_mirror_link)  # Convert to absolute URL
                download_link = get_download_link_from_mirror(mirror_url)
                if download_link:
                    return download_link

    return None

def get_download_link_from_mirror(mirror_url):
    response = requests.get(mirror_url)
    
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    
    if not table:
        return None

    # Look for the first <a> element within the first <tr> of the table's tbody
    download_link = table.find('tr').find('a')['href']
    download_link = urljoin(mirror_url, download_link)  # Convert to absolute URL
    
    if download_link:
        return download_link
    else:
        return None









@app.route('/pirate-book', methods=['POST'])
def pirate_book(title, author_last_name):
    status = None
    data = request.get_json()

    download_link = search_libgen(title, author_last_name)
    if download_link == 504:
        status = "Timed out"
    elif download_link is None:
        status = "Failed"

    



    


def upload_epub():
    if 'credentials' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    book_title = data.get('title')
    book_author_last_name = data.get('authorLastName')
    status = pirate_book(book_title, book_author_last_name)
    return jsonify({"message": status})


def pirate_book(title, author_last_name):
    

    filepath = download_epub(download_link)
    upload_book_to_google_drive(title, filepath)
    return "Success"


    


# Path to your OAuth 2.0 credentials file
CLIENT_SECRETS_FILE = "client_secret_1005985003754-346uaprpsccoueoip1gm6cd6rsbtk4ha.apps.googleusercontent.com.json"

# Scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Authentication flow to get credentials
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

# Build the Google Drive API service
drive_service = build('drive', 'v3', credentials=credentials)

# Folder name
folder_name = 'FreeBooks'

# Check if the folder already exists
query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
response = drive_service.files().list(q=query, fields='files(id, name)').execute()
folder = response.get('files', [])

if not folder:
    # Folder doesn't exist, create it
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
else:
    # Folder exists, retrieve its ID
    folder_id = folder[0].get('id')

def upload_book_to_google_drive(bookTitle, bookFilepath):
    file_metadata = {
        'name': bookTitle + '.epub', 
        'parents': [folder_id]  # Specify the folder ID
    }

    media = MediaFileUpload(bookFilepath, mimetype='application/epub+zip')

    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def download_epub(downloadLink, title):
     filepath = 'downloads/' + title + '.epub'
     response = requests.get(downloadLink, allow_redirects=True)
     with open(filepath, 'wb') as epub:
            epub.write(response.content)
     return filepath


    
if __name__ == '__main__':
    app.run(debug=True)