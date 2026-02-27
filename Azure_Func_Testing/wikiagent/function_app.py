import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import re
from urllib.parse import urljoin
import threading
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)




#  sample http trigger function

# @app.route(route="http_trigger")
# def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )



#  Function : To fetch the content of the wiki page
# Session for wiki scraping: reuse connection and default headers
scraperSession = requests.Session()
SCRAPER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
scraperSession.headers.update(SCRAPER_HEADERS)

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
    'Admin',
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
    'editor',
    'edit',
    'google',
    'wikipedia',
    'mediawiki',
    'foundation',
    '_blank',
    'confero.alkit',
    'github.com',
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

IMAGE_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.webp',
]

VIDEO_EXTENSIONS = [
    '.mp4',
    '.avi',
    '.mov',
    '.wmv',
    '.flv',
]

AUDIO_EXTENSIONS = [
    '.mp3',
    '.wav',
    '.ogg',
    '.m4a',
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
def check_media_url(url:str):
    """
    Checks if the url is a media url.
    Returns True if the url is a media url, False otherwise.
    """
    for image_extension in IMAGE_EXTENSIONS:
        if image_extension in url:
            return True
    for video_extension in VIDEO_EXTENSIONS:
        if video_extension in url:
            return True
    for audio_extension in AUDIO_EXTENSIONS:
        if audio_extension in url:
            return True
    return False

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

def remove_blacklist_urls(list: list):
    for item in list:
        if isinstance(item, dict):
            url = item['url']
            for url_string in URL_STRINGS_TO_DROP:
                if url_string in url.strip().lower():
                    list.remove(item)
            title = item['title']
            for title_string in TITLES_TO_DROP:
                if title_string in title.strip().lower():
                    list.remove(item)
        elif isinstance(item, str):
            for url_string in URL_STRINGS_TO_DROP:
                if url_string in item.strip().lower():
                    list.remove(item)
    return list

def remove_irrelevant_areas(html_content:str, url:str):
    """
    Removes the irrelevant areas from the html content.
    Returns the html content with the irrelevant areas removed.
    """
    is_base_url = False
    for _, wiki_url in WICE_WIKI_VERSIONS.items():
        if wiki_url.strip('/') in url.strip('/'):
            is_base_url = True
            break
    if is_base_url:
        return html_content
    
    if html_content.startswith('<?xml'):
        return html_content
    if '.xml' in url:
        return html_content
    if '<?xml' in html_content:
        return html_content
    if check_media_url(url):
        return html_content
    soup = BeautifulSoup(html_content, "html.parser")
    mw_panel_div = soup.find("div", id="mw_panel")
    if mw_panel_div:
        mw_panel_div.decompose()
    mw_head_div = soup.find("div", id="mw_head")
    if mw_head_div:
        mw_head_div.decompose()
    # Remove the Contents/Index section from the html_content if present
    contents_index_div = soup.find("div", id="toc")
    if contents_index_div:
        contents_index_div.decompose()
    # Remove the <footer> tag from the html_content if present
    footer_tag = soup.find("footer")
    if footer_tag:
        footer_tag.decompose()
    return str(soup)

def get_version_number_from_url(url:str):
    url_split = url.split('/')
    wice_from_url = url_split[3]
    if wice_from_url.startswith('wice'):
        return wice_from_url.replace('wice', '').replace('.', '')
    return None

def add_to_complete_map(url:str, title:str, version_number:str):
    """
    Adds the url to the complete map for the given version number.
    Map is used to store all urls verified to exist.
    Map Structure: {'version_number': [{'url': url, 'title': title}]}
    """
    version_number = version_number.replace('.', '')
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
    version_number = version_number.replace('.', '')
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

def remove_invalid_urls_from_list(list:list):
    """
    Removes invalid urls from the list.
    Returns the list with invalid urls removed.
    """
    for item in list:
        if not useUrl_Checker(item):
            list.remove(item)
    return list

def remove_invalid_entries_from_list(list:list):
    """
    Removes invalid entries from the list.
    Returns the list with invalid entries removed.
    """
    for entry in list:
        url = entry['url']
        title = entry['title']
        if not useUrl_Checker(url) or not useTitle_Checker(title):
            list.remove(entry)
    return list

def renew_scraper_session():
    """
    Renews the scraper session.
    """
    global scraperSession
    scraperSession.close()
    scraperSession = requests.Session()
    scraperSession.headers.update(SCRAPER_HEADERS)
    bot_limit_reached = False
    request_bot_limit = 0

def check_url_exists(url:str):
    """
    Checks if the url exists by making a HEAD request.
    Returns True if the url exists, False otherwise.
    """
    response = scraperSession.head(url, timeout=10)
    if response.status_code == 200:
        if "Not Found" in response.text:
            if bot_limit_reached:
                renew_scraper_session()
            return " Not Found"
        return True
    if bot_limit_reached:
        renew_scraper_session()
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

def extract_hyperlinks_with_map(html_content, source_url:str, version_number:str):
    """
    Extracts all hyperlinks and their associated text from HTML content using the complete map.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    new_links = []
    unique_urls = [source_url]
    parsed_links = [source_url]

    # If urls already exist in complete map, load them first
    version_number = version_number.replace('.', '')
    if version_number in COMPLETE_MAP.keys():
        links = COMPLETE_MAP[version_number]
        for link in links:
            url = link['url'].strip()
            unique_urls.append(url)
            parsed_links.append(url)

    # Now check for any new URLs in the html page contents
    for anchor in soup.find_all('a', href=True):
        text = anchor.get_text(strip=True)
        url = resolve_relative_url(href=anchor['href'], current=source_url, base_url=source_url).strip()
        if useUrl_Checker(url) and useTitle_Checker(text) and (url not in unique_urls) and (url not in parsed_links):
            unique_urls.append(url)
            new_links.append(url)
            new_links = remove_duplicates_from_list(new_links)
            links.append({
                'title': text,
                'url': url
            })
            links = remove_invalid_entries_from_list(links)
            new_links = remove_invalid_urls_from_list(new_links)

    # Map all new HyperLinks
    for url in tqdm(new_links, desc='PROGRESS: Mapping new HyperLinks for version '+version_number):
        if url not in parsed_links:
            parsed_links.append(url)
            try:
                if check_media_url(url):
                    file_name = url.split('/')[-1]
                    # If the file name is a media file, add it to the complete map
                    if file_name not in COMPLETE_MAP[version_number]:
                        COMPLETE_MAP[version_number].append({
                            'url': url,
                            'title': file_name
                        })
                    continue
                parser = 'xml' if '.xml' in url else 'html.parser'
                html_content_temp = remove_irrelevant_areas(fetch_html_from_url(url), url)                   # Fetch the html content of the sub page
                content_stripped = html_content_temp.lstrip()
                if content_stripped.startswith('<?xml'):
                    parser = 'xml'
                if (len(content_stripped) > 100) and ('<?xml' in content_stripped):
                    parser = 'xml'
                else:
                    parser = 'html.parser'
                tempSoup = BeautifulSoup(html_content_temp, parser)     # Parse the html content of the sub page
                # Check for any new HyperLinks in the sub page  
                for anchor in tempSoup.find_all('a', href=True):
                    text = anchor.get_text(strip=True).strip()
                    temp_url = resolve_relative_url(href=anchor['href'], current=url, base_url=source_url).strip()
                    # If the url is valid, add it to the complete map
                    if version_number is not None:
                        add_to_complete_map(temp_url, text, version_number)
                    # If the url is valid, add it to the links list
                    if useUrl_Checker(temp_url) and useTitle_Checker(text) and (temp_url not in unique_urls) and (temp_url not in parsed_links) and (temp_url not in new_links):
                        unique_urls.append(temp_url)
                        new_links.append(temp_url)
                        new_links = remove_duplicates_from_list(new_links)
                        links.append({
                            'title': text,
                            'url': temp_url
                        })
                        links = remove_invalid_entries_from_list(links)
                        new_links = remove_invalid_urls_from_list(new_links)
            except Exception as e:
                if 'too many requests' in str(e).lower():
                    bot_limit_reached = True
                    # Remove duplicates from the links list
                    links = remove_duplicates_from_list_of_dicts(links)
                    # Replace the complete map with the new links
                    if version_number is not None:
                        COMPLETE_MAP[version_number] = links
                    return links
                print(f"ERROR: Fetching html content of sub page (URL: {url}): {e}")
                if url in new_links:
                    new_links.remove(url)
                    new_links = remove_duplicates_from_list(new_links)
                    links = remove_invalid_entries_from_list(links)
                    new_links = remove_invalid_urls_from_list(new_links)
    # Remove duplicates from the links list
    links = remove_duplicates_from_list_of_dicts(links)
    # Replace the complete map with the new links
    if version_number is not None:
        COMPLETE_MAP[version_number] = links
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
    response = scraperSession.get(url, timeout=10)
    response.raise_for_status()
    # If the response content does not include the bot limit, append it at the end
    global request_bot_limit
    response_text = response.text
    if "too many requests" not in response_text.lower():
        request_bot_limit += 1
    else:
        renew_scraper_session()

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
        for pre_card in tqdm(pre_cards, desc='PROGRESS: Extracting version numbers from software release history'):
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
    print('\nLOG: Unavailable versions: ', json.dumps(UNAVAILABLE_WICE_WIKI_VERSIONS, indent=4))
    print('\nLOG: Available versions: ', json.dumps(WICE_WIKI_VERSIONS, indent=4))
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

def _init_one_version(version):
    """Worker: fetch and extract hyperlinks for one version, write into COMPLETE_MAP."""
    url = WICE_WIKI_VERSIONS[version]
    print('LOG: Mapping Version: ', version)
    init_links = extract_hyperlinks_with_map(fetch_html_from_url(url), url, version)
    if len(init_links) > 0:
        COMPLETE_MAP[version.replace('.', '')] = init_links

def map_quick_start_hyperlinks():
    quick_start_versions = []
    for version, links in COMPLETE_MAP.items():
        for item in links:
            url = item.get('url', '')
            if 'index.php/Quick_Start' in url:
                quick_start_versions.append((version, url))
                continue

    for version, quick_start_url in quick_start_versions:
        print(f"\nLOG: Mapping Quick Start hyperlinks for version: {version}, url: {quick_start_url}")
        hyperlinks = extract_hyperlinks_with_map(fetch_html_from_url(quick_start_url), quick_start_url, version)
        # Avoid duplicating the initial entry for Quick Start (if already present)
        existing_urls = set(link['url'] for link in COMPLETE_MAP[version])
        new_links = [link for link in hyperlinks if link['url'] not in existing_urls]
        COMPLETE_MAP[version].extend(new_links)

def init():
    """
    Initializes the complete map by mapping all the versions and their hyperlinks.
    """
    init_start_time = time.time()
    get_version_map_full(v_type='software')
    valid_versions_count = len(WICE_WIKI_VERSIONS.keys())

    with ThreadPoolExecutor(max_workers=valid_versions_count) as executor:
        futures = [executor.submit(_init_one_version, version) for version in WICE_WIKI_VERSIONS.keys()]
        for f in as_completed(futures):
            f.result()  # wait for each; re-raise any exception

    # For each url in COMPLETE_MAP, if url has the sub-string 'index.php/Quick_Start', then map all hyperlinks within it
    map_quick_start_hyperlinks()

    # Remove blacklist urls from the complete map
    for key in COMPLETE_MAP.keys():
        COMPLETE_MAP[key] = remove_blacklist_urls(COMPLETE_MAP[key])
        
    print('LOG: After Initial Mapping: ')
    for key in COMPLETE_MAP.keys():
        print(f"\t{key}: {len(COMPLETE_MAP[key])}")

    init_end_time = time.time()
    init_execution_time = init_end_time - init_start_time
    minutes, seconds = divmod(init_execution_time, 60)
    print(f"LOG: Initial Mapping Execution Time: {int(minutes)} min {seconds:.2f} sec")

_iniy_lock = threading.Lock()
_initialized = False
def async_init():
    global _initialized
    with _iniy_lock:
        if not _initialized:
            init()
            _initialized = True


# start init in a separate thread so the function host can finish startup
threading.Thread(target=async_init, daemon=True).start()

@app.route(route='get_version_map_full',methods=['GET'])
def getVersionMapFull(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to fetch version map full.')

    version_maps = get_version_map_full(v_type='software')
    if version_maps:
        
        return func.HttpResponse(
            body=json.dumps(version_maps), 
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )
    else:
        return func.HttpResponse(
            body=json.dumps({'error': 'No version maps found'}), 
            status_code=404,
            headers={'Content-Type': 'application/json'}
        )   

@app.route(route="get_url_content", methods=["POST"])
def get_url_content(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to fetch URL content.')

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON in request body.", status_code=400)    
    if not data :
        return func.HttpResponse("No data provided in request body.", status_code=400)
    
    url = data.get('url')
    if not url:
        return func.HttpResponse("URL is required in the request body.", status_code=400)   
    

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
     
    print('\nLOG: Available Versions: ', COMPLETE_MAP.keys())
    print(f"LOG: Available URLs for {version_number}: {len(COMPLETE_MAP[version_number])}")

    try:
         html_content = fetch_html_from_url(url)
         html_content = remove_irrelevant_areas(html_content, url)
    except Exception as e:
                   return func.HttpResponse(f"Error fetching html content: {e}", status_code=500)
    try:
         text_content=html_to_text(html_content)

    except Exception as e:
                   return func.HttpResponse(f"Error converting html to text: {e}", status_code=500)
    try:
        hyperlinks = extract_hyperlinks_with_map(html_content, url,version_number)
          
    except Exception as e:
                   return func.HttpResponse(f"Error extracting hyperlinks: {e}", status_code=500)
    

    end_time = time.time()
    execution_time = end_time - start_time
    if len(hyperlinks) == 0 and version_number.replace('.', '') in COMPLETE_MAP.keys():
        hyperlinks = remove_blacklist_urls(COMPLETE_MAP[version_number.replace('.', '')])

    print('\n\nLOG: Duplicates removed by URL: '+str(duplicate_urls))
    print('LOG: Duplicates removed by Titles: '+str(duplicate_titles))
    print('LOG: Version number: ',version_number)
    print('LOG: Total SubUrls Found: ',len(hyperlinks))

    if text_content:
        response_body = {
             "success": True,
             "url": url,
            "contentOfPage": text_content,
            "hyperlinksFromPage": hyperlinks,
            "executionTime": execution_time
        }
        if bot_limit_reached:
            response_body['botLimitReached'] = bot_limit_reached
            response_body['requestBotLimit'] = request_bot_limit
        return func.HttpResponse(
            body=json.dumps(response_body), 
            status_code=200,
            mimetype="application/json")
    else:
        return func.HttpResponse("No content found at the provided URL.", status_code=404)  
    
  
# # Populate the version map when instance is started
# init()     