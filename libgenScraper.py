
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def search_libgen(title, author):
    search_url = "https://libgen.li/index.php"
    params = {
        'req': f"{title} {author}",
        'res': 25,
        'column': 'def',
        'view': 'simple',
        'phrase': 1,
        'sort': 'year',
        'sortmode': 'DESC'
    }
    test_response = requests.get(search_url)

    test_google_response = requests.get('https://www.google.com/')
    print(f"Fetching google.com got response {test_google_response.status_code}.")

    response = requests.get(search_url, params=params)
    
    if response.status_code != 200:
        if response.status_code == 504:
            return 504
        print(f"The response status code was not 200, but the servers aren't down either! Here's the actual response we got: {response.status_code}.")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'tablelibgen'})

    if not table:
        print("No table was found!")
        return None

    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) > 8:
            if 'epub' in columns[-2].text.lower():  # Check if the format is EPUB
                first_mirror_link = columns[-1].find_all('a')[0]['href']  # Get the first mirror link
                mirror_url = urljoin(search_url, first_mirror_link)  # Convert to absolute URL
                download_link = get_download_link_from_mirror(mirror_url)
                if download_link:
                    print(f"download_link: {download_link}")
                    return download_link
    
    print("There were no epubs on the table!")
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

def download_epub(title, author_last_name):
    file_path = os.path.join('downloads', f'{title.strip()}.epub')
    download_link = search_libgen(title, author_last_name)
    if download_link == None:
        print("No download link found!")
        return None
    else:
        if download_link == 504:
            print("The servers are down!")
            return 504
        else:
            with requests.get(download_link, allow_redirects=True) as response:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
            return file_path