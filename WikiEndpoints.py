# Imports and Installs
import os
import re
import json
import requests
from tqdm import tqdm
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, jsonify, request

# Flask App
app = Flask(__name__)
CORS(app)

# Constants
URLs_TO_DROP = [
    'https://developer.wikimedia.org/',
    'https://www.mediawiki.org/',
    'https://www.wikipedia.org/',
    'https://foundation.wikimedia.org/wiki/Home',
    'https://species.wikimedia.org/wiki/Wikispecies:Administrators',
    'https://hsb.wikipedia.org/wiki/Diskusija_z_wu\u017eiwarjom:J_budissin',
]

URL_STRINGS_TO_DROP = [
    'Administrator',
    'logout',
    'login',
    'remove credentials',
    'export',
    'contribute',
    'edit',
    'http://',
    'mailto:',
    'tel:',
    'file:',
    'ftp://',
    'ftps://',
]

TITLES_TO_DROP = [
    'log in',
    'logout',
    'remove credentials',
    'export',
    'contribute',
    'edit',
    'history',
    'view source',
    'the portal administrator view',
    'user',
    'administrator',
    'random page',
    'view source',
    'the portal administrator view'
]

WIKI_BASE_URL = "https://wiki.alkit.se/<VERSION_NUMBER>/index.php/Main_Page"
RELEASE_HISTORIES = {
    'software': "https://wice-sysdoc.alkit.se/index.php/WICE_WCU_Software_Revision_History",    # Approach : Get listed version numbers and generate URLs
    'portal': 'https://wice-sysdoc.alkit.se/index.php/WICE_Portal_Release_notes',               # No specific approach mentioned for this history
    'm2m': 'https://wice-sysdoc.alkit.se/index.php/M2M_release_notes',                          # No specific approach mentioned for this history
    'masterbox': 'https://wice-sysdoc.alkit.se/index.php/MasterBox_release_notes',              # No specific approach mentioned for this history
    }

WICE_WIKI_VERSIONS = {}              # {'version_number': 'url'}
UNAVAILABLE_WICE_WIKI_VERSIONS = {}  # {'version_number': 'url'}

# Controller Functions
def useUrl_Checker(url:str):
    """
    Checks if the URL should be dropped based on the URL strings and URLs to drop.
    Returns False if the URL should be dropped, True otherwise.
    """
    for url_string in URL_STRINGS_TO_DROP:
        if url_string in url:
            return False
    for url_to_drop in URLs_TO_DROP:
        if url.strip() == url_to_drop.strip():
            return False
    return True

def useTitle_Checker(title:str):
    """ 
    Checks if the title should be dropped based on the titles to drop.
    Returns False if the title should be dropped, True otherwise.
    """
    for title_to_drop in TITLES_TO_DROP:
        if title.strip() == title_to_drop.strip():
            return False
    return True

def check_url_exists(url:str):
    """
    Checks if the url exists by making a HEAD request.
    Returns True if the url exists, False otherwise.
    """
    response = requests.head(url)
    if response.status_code == 200:
        if "Not Found" in response.text:
            return " Not Found"
        return True
    return False

def resolve_relative_url(href:str, current:str, base_url:str=None):
    """
    Placeholder for URL resolver that converts relative URLs to absolute.
    Implementation to be added later.

    Args:
        relative_url (str): The potentially relative URL to resolve.
        base_url (str, optional): The base URL to resolve against.

    Returns:
        str: The resolved absolute URL (currently returns input unmodified).
    """
    if not base_url:
        return href
    if 'Main_Page' in href:
      return base_url
    if href.startswith(("http://", "https://", "mailto:", "tel:")):
        return href                            # already absolute
    if href.startswith("/"):
        return urljoin(current, href)
    return urljoin(base_url, href)

def extract_hyperlinks(html_content, source_url:str):
    """
    Extracts all hyperlinks and their associated text from HTML content.

    Args:
        html_content (str): HTML string to parse.

    Returns:
        list: A list of dicts each containing 'title' (the link text) and 'url' (the link href).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    unique_urls = [source_url]
    parsed_links = [source_url]
    # Get hyperlinks from main page
    for anchor in soup.find_all('a', href=True):
        text = anchor.get_text(strip=True)
        url = resolve_relative_url(href=anchor['href'], current=source_url, base_url=source_url)
        if useUrl_Checker(url) and useTitle_Checker(text):
            unique_urls.append(url)
            links.append({
                'title': text,
                'url': url
            })
    # Map all hyperlinks from Subpages
    while len(parsed_links) < len(unique_urls):
        for url in unique_urls:
            # Check if the url has already been parsed
            if url not in parsed_links:
                # Add the url to the parsed links
                parsed_links.append(url)
                # Fetch the html content of the sub page
                html_content_temp = fetch_html_from_url(url)
                # Parse the html content of the sub page and extract the hyperlinks
                # Append hyperlinks to unique urls and final list
                tempSoup = BeautifulSoup(html_content_temp, "html.parser")
                for anchor in tempSoup.find_all('a', href=True):
                    text = anchor.get_text(strip=True)
                    temp_url = resolve_relative_url(href=anchor['href'], current=url, base_url=source_url)
                    if useUrl_Checker(temp_url) and useTitle_Checker(text):
                        unique_urls.append(temp_url)
                        links.append({
                            'title': text,
                            'url': temp_url
                        })
    return links

def html_to_text(html_content):
    """
    Converts HTML content to plain text using BeautifulSoup.

    Args:
        html_content (str): HTML string to convert.

    Returns:
        str: Text content extracted from HTML.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator='\n', strip=True)

def fetch_html_from_url(url):
    """
    Fetches HTML content from the given URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content as a string.

    Raises:
        Exception: If the GET request fails or an HTTP error occurs.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_version_map_full(v_type:str='software'):
    """
    Fetches the version map full from the given URL using an HTTP GET request.
    Returns all wice wiki versions
    """
    if v_type == 'software':
        release_history_url = RELEASE_HISTORIES['software']
        release_history_html = fetch_html_from_url(release_history_url)
        release_history_soup = BeautifulSoup(release_history_html, "html.parser")
        # get all cards using the tag <pre>
        version_numbers = []
        pre_cards = release_history_soup.find_all('pre')
        for pre_card in tqdm(pre_cards, desc='\nExtracting version numbers from software release history'):
            # Extract version number from the pre_card's text.
            version_match = re.search(r'Version\s*([\d\.]+)', pre_card.text)
            if version_match:
                version_number = version_match.group(1)
                # Remove the last digit (security update digit) from the version number, if present
                version_number = '.'.join(version_number.split('.')[:2])
                # Get the url for the version
                version_url = WIKI_BASE_URL.replace('<VERSION_NUMBER>', 'wice'+version_number.replace('.', ''))
                # If version already mapped, skip checks and continue
                if (version_number in WICE_WIKI_VERSIONS.keys()) or (version_number in UNAVAILABLE_WICE_WIKI_VERSIONS.keys()):
                    continue
                # Check if the url exists
                checkFlag = check_url_exists(version_url)
                if checkFlag==True:
                    version_numbers.append(version_number)
                    WICE_WIKI_VERSIONS[str(version_number)] = version_url
                else:
                    # If the url does not exist, skip this version
                    UNAVAILABLE_WICE_WIKI_VERSIONS[str(version_number)] = str(version_url)+' - '+str(checkFlag)
                    continue
                version_numbers.append(version_number)
                WICE_WIKI_VERSIONS[str(version_number)] = version_url
            else:
                # If not found, skip this card
                continue
    # TODO: Decide what to do for other Base Urls
    print('Unavailable versions: ', json.dumps(UNAVAILABLE_WICE_WIKI_VERSIONS, indent=4))
    return WICE_WIKI_VERSIONS

def get_url_to_version(version_number:str):
    """
    Fetches the url for the given version number.
    """
    version_maps = get_version_map_full()
    if version_number in version_maps.keys():
      return version_maps[version_number]
    else:
      return None

# Endpoints
@app.route('/health-check')
def healthCheck():
    return jsonify({'status': 'ok'}), 200

@app.route('/get_version_map_full')
def getVersionMapFull():
    version_maps = get_version_map_full(v_type='software')
    if version_maps:
        return jsonify(version_maps), 200
    else:
        return jsonify({'error': 'No version maps found'}), 404

@app.route('/does_version_exist/<version_number>')
def doesVersionExist(version_number):
    version_maps = get_version_map_full()
    if version_number in version_maps.keys():
        return jsonify({'version_exists': True}), 200
    else:
        return jsonify({'version_exists': False}), 404

@app.route('/get_url_to_version/<version_number>')
def getUrlToVersion(version_number):
    url = get_url_to_version(version_number)
    if url:
        return jsonify({'url': url}), 200
    else:
        return jsonify({'error': 'No url found for version number'}), 404

@app.route('/get_url_content', methods=['POST'])
def getUrlContent():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'No url provided'}), 400
    
    try:
        html_content = fetch_html_from_url(url)
    except Exception as e:
        return jsonify({'error': 'Error fetching html content: '+str(e)}), 500

    try:
        text_content = html_to_text(html_content)
    except Exception as e:
        return jsonify({'error': 'Error converting html to text: '+str(e)}), 500
    
    try:
        hyperlinks = extract_hyperlinks(html_content, url)
    except Exception as e:
        return jsonify({'error': 'Error extracting hyperlinks: '+str(e)}), 500
    
    if text_content:
        return jsonify({'contentOfPage': text_content, 'hyperlinksFromPage': hyperlinks}), 200
    else:
        return jsonify({'error': 'No content found for url'}), 404

if __name__ == '__main__':
    debug = os.getenv('DEBUG', True)
    port = os.getenv('PORT', 5000)
    host = os.getenv('HOST', '0.0.0.0')
    app.run(debug=debug, port=port, host=host, load_dotenv=True)