from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_book_to_google_drive(file_path, credentials):
    try:
        # Use the credentials passed as an argument
        service = build('drive', 'v3', credentials=credentials)

        file_metadata = {'name': file_path.split('/')[-1]}
        media = MediaFileUpload(file_path, mimetype='application/epub+zip')

        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
