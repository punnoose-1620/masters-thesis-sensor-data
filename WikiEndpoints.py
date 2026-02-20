# Imports and Installs
import os
import re
import json
import time
import requests
import subprocess
from tqdm import tqdm
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, jsonify, request

# Flask App
app = Flask(__name__)
CORS(app)

request_bot_limit = 0
bot_limit_reached = False
duplicate_urls = 0
duplicate_titles = 0

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
    'download',
    ';',
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    '<',
    '>',
    '|',
    '\\'
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
    'the portal administrator view',
    'https://',
    'http://',
    'mailto:',
    'tel:',
    'file:',
    'ftp://',
    'ftps://',
    'download',
    ';',
    '(',
    ')',
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
COMPLETE_MAP = {}                     # {'version_number': [{'url': url, 'title': title}]}  --> List of Verified URLs for the given version number

# Controller Functions
def remove_duplicates_from_list(list:list):
    for item in list:
        itemIndex = list.index(item)
        for item2 in list[itemIndex+1:]:
            if item == item2:
                list.remove(item2)
    return list

def remove_duplicates_from_list_of_dicts(list:list):
    before_length = len(list)
    for item in list:
        itemIndex = list.index(item)
        for item2 in list[itemIndex+1:]:
            if item['url'] == item2['url']:
                list.remove(item2)
    after_url_length = len(list)
    global duplicate_urls
    duplicate_urls += before_length-after_url_length
    for item in list:
        itemIndex = list.index(item)
        for item2 in list[itemIndex+1:]:
            if item['title'] == item2['title']:
                list.remove(item2)
    after_title_length = len(list)
    global duplicate_titles
    duplicate_titles += before_length-after_title_length
    return list

def get_version_number_from_url(url:str):
    url_split = url.split('/')
    wice_from_url = url_split[3]
    if wice_from_url.startswith('wice'):
        return wice_from_url.replace('wice', '')
    return None

def add_to_complete_map(url:str, title:str, version_number:str):
    """
    Adds the url to the complete map for the given version number.
    Map is used to store all urls verified to exist.
    Map Structure: {'version_number': [{'url': url, 'title': title}]}
    """
    if version_number not in COMPLETE_MAP.keys():
        COMPLETE_MAP[version_number] = [{'url': url, 'title': title}]
    COMPLETE_MAP[version_number].append({'url': url, 'title': title})

def check_complete_map(url:str, version_number:str):
    """
    Checks if the url is already in the complete map for the given version number. This map contains all urls verified to exist.
    Returns :
    - True if the url is in the complete map
    - False if url is not verified to exist
    """
    if version_number in COMPLETE_MAP.keys():
        for item in COMPLETE_MAP[version_number]:
            if item['url'] == url:
                return True
    return False

def useUrl_Checker(url:str):
    """
    Checks if the URL should be dropped based on the URL strings and URLs to drop.
    Returns False if the URL should be dropped, True otherwise.
    """
    if url.strip() == '':
        return False
    if re.search(r'[A-Za-z0-9_]+:[A-Za-z0-9_]+', url):
        return False
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
        if title.strip().lower() == title_to_drop.strip().lower():
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
    if re.search(r'[A-Za-z0-9_]+:[A-Za-z0-9_]+', href):
        return ''
    if not base_url:
        return href
    if 'Main_Page' in href:
      return base_url
    if href.startswith(("http://", "https://", "mailto:", "tel:")):
        return href                            # already absolute
    if href.startswith("/"):
        return urljoin(current, href)
    return urljoin(base_url, href)

def get_title_for_url(links:list, url:str):
    for link in links:
        if link['url'] == url:
            return link['title']
    return None

def extract_hyperlinks(html_content, source_url:str, version_number:str):
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
    
    print('Unique URLs: ')
    unique_urls = remove_duplicates_from_list(unique_urls)
    for url in unique_urls:
        print(url)
    # Map all hyperlinks from Subpages
    while len(parsed_links) < len(unique_urls):
        for url in unique_urls:
            url = url.strip()
            # Check if the url has already been parsed
            if url not in parsed_links:
                # Add the url to the parsed links
                parsed_links.append(url)
                if version_number is not None:
                    if check_complete_map(url, version_number):   # If the url is already verified to exist, skip the checks
                        links = COMPLETE_MAP[version_number]
                        for item in links:
                            url = item['url']
                            parsed_links.append(url)
                # Fetch the html content of the sub page
                try:
                    html_content_temp = fetch_html_from_url(url)
                    # Parse the html content of the sub page and extract the hyperlinks
                    # Append hyperlinks to unique urls and final list
                    tempSoup = BeautifulSoup(html_content_temp, "html.parser")
                    for anchor in tempSoup.find_all('a', href=True):
                        text = anchor.get_text(strip=True)
                        temp_url = resolve_relative_url(href=anchor['href'], current=url, base_url=source_url)
                        if useUrl_Checker(temp_url) and useTitle_Checker(text) and (temp_url.strip() not in unique_urls) and (temp_url.strip() not in parsed_links):
                            unique_urls.append(temp_url.strip())
                            if version_number is not None:
                                add_to_complete_map(temp_url.strip(), text.strip(), version_number)
                            links.append({
                                'title': text.strip(),
                                'url': temp_url.strip()
                            })
                except Exception as e:
                    print('\nError fetching html content of sub page (URL: '+url+'): '+str(e))
                    if url in unique_urls:
                        unique_urls.remove(url)
                    if url in parsed_links:
                        parsed_links.remove(url)
                    if url in links:
                        links.remove({
                            'title': get_title_for_url(links, url),
                            'url': temp_url
                        })
                    if 'too many requests' in str(e).lower():
                        print('\n\nBot Limit Reached for Wiki Requests: ', request_bot_limit)
                        bot_limit_reached = True
                        links = remove_duplicates_from_list_of_dicts(links)
                        return links

            unique_urls = remove_duplicates_from_list(unique_urls)
            links = remove_duplicates_from_list_of_dicts(links)
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
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    )
    response.raise_for_status()
    # If the response content does not include the bot limit, append it at the end
    global request_bot_limit
    response_text = response.text
    if "too many requests" not in response_text.lower():
        request_bot_limit += 1

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
        print(' ')
        for pre_card in tqdm(pre_cards, desc='Extracting version numbers from software release history'):
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
    print('\nUnavailable versions: ', json.dumps(UNAVAILABLE_WICE_WIKI_VERSIONS, indent=4))
    print('\nAvailable versions: ', json.dumps(WICE_WIKI_VERSIONS, indent=4))
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
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the WICE Wiki API. This API is used to resolve version numbers, urls and get contents from the WICE Wiki Pages.'}), 200

@app.route('/health-check')
def healthCheck():
    last_commit_message = "Unable to retrieve commit message"
    try:
        result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], capture_output=True, text=True)
        last_commit_message = result.stdout.strip()
    except Exception as e:
        last_commit_message = f"Unable to retrieve commit message: {e}"
    return jsonify({'status': 'ok', 'last_commit_message': last_commit_message}), 200

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
    
    global bot_limit_reached
    global request_bot_limit
    global duplicate_urls
    global duplicate_titles
    bot_limit_reached = False
    request_bot_limit = 0
    duplicate_urls = 0
    duplicate_titles = 0
    start_time = time.time()

    version_number = get_version_number_from_url(url)

    try:
        html_content = fetch_html_from_url(url)
    except Exception as e:
        return jsonify({'error': 'Error fetching html content: '+str(e)}), 500

    try:
        text_content = html_to_text(html_content)
    except Exception as e:
        return jsonify({'error': 'Error converting html to text: '+str(e)}), 500
    
    try:
        hyperlinks = extract_hyperlinks(html_content, url, version_number)
    except Exception as e:
        return jsonify({'error': 'Error extracting hyperlinks: '+str(e)}), 500
    
    end_time = time.time()
    execution_time = end_time - start_time

    print('\n\nDuplicates removed by URL: '+str(duplicate_urls))
    print('Duplicates removed by Titles: '+str(duplicate_titles))
    print('Version number: ',version_number)
    print('Total SubUrls Found: ',len(hyperlinks))

    if text_content:
        returnValue = {
            'contentOfPage': text_content, 
            'hyperlinksFromPage': hyperlinks,
            'execution_time': execution_time
            }
        if bot_limit_reached:
            returnValue['bot_limit_reached'] = bot_limit_reached
            returnValue['request_bot_limit'] = request_bot_limit
        return jsonify(returnValue), 200
    else:
        return jsonify({'error': 'No content found for url'}), 404

# Populate the version map when instance is started
get_version_map_full(v_type='software')

if __name__ == '__main__':
    debug = os.getenv('DEBUG', True)
    port = os.getenv('PORT', 5000)
    host = os.getenv('HOST', '0.0.0.0')
    app.run(debug=debug, port=port, host=host, load_dotenv=True)