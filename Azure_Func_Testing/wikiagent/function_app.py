import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import json
from tqdm import tqdm
import re
from urllib.parse import urljoin
import threading
import warnings
import subprocess
# Ignore XML Parsed as HTML Warning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)





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

TARGET_FILE = "WikiParserPipeline.json"
fetchCount = 0

RELEASE_HISTORIES = 'https://wice-sysdoc.alkit.se/index.php/WICE_WCU_Software_Revision_History'
WIKI_BASE_URL = "https://wiki.alkit.se/<VERSION_NUMBER>/index.php/Main_Page"

URLs_TO_INCLUDE = ['wiki.alkit.se', 'sysdoc.alkit.se', 'alkit.se/wice', 'wice.alkit.se']

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
    'wireguard',
    'solarwinds',
    'comparitech',
    'vpm.'
    'vanish',
    'openelec',
    'freak',
    'project.org',
    'torrent',
    'opennicproject',
    'threatpost',
    'boum.org',
    'spideroak',
    'surfshark',
    'azure.com',
    'securelist',
    'eicar',
    'vembu',
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

# version: home_url
VALID_VERSION_HOME_PAGES = {}

# version: [{url, title}]
COMPLETE_MAP = {}

# Function to double check and avoid invalid url patterns
def avoid_url_check(url:str):
    url = url.strip()
    if url == '':
        return True
    for pattern in URL_STRINGS_TO_DROP:
        if pattern in url:
            return True
    for pattern in URLs_TO_DROP:
        if pattern in url:
            return True
    for pattern in IMAGE_EXTENSIONS:
        if url.endswith(pattern):
            return True
    for pattern in VIDEO_EXTENSIONS:
        if url.endswith(pattern):
            return True
    for pattern in AUDIO_EXTENSIONS:
        if url.endswith(pattern):
            return True
    for url_to_include in URLs_TO_INCLUDE:
        if url_to_include in url:
            return False
    return False

# Function to check if URL is already mapped in any version
def already_mapped(url:str):
    list_of_mappings = COMPLETE_MAP.values()                # list_of_mappings: [[{url, title} for v1],[{url, title} for v2]], 
    for mapping in list_of_mappings:                        # For mappings list of each version
        for entry in mapping:                               # For each entry in that mappings list
            url_ref = entry.get('url', '')
            if url.strip()==url_ref.strip():
                return True
    return False

def add_to_map(url:str, title:str, version:str):
    if version not in COMPLETE_MAP.keys():
        COMPLETE_MAP[version] = [{
            'title': title,
            'url': url
        }]
    else:
        COMPLETE_MAP[version].append({
            'title': title,
            'url': url
        })

# Resolve Relative Urls and ignore fragment-only / empty links
def resolve_relative_url(href:str, current:str, base_url:str=None):
    # If the href is a fragment (sub-section) of the page, like '#SectionName', return empty
    if href.strip().startswith('#'):
        return ''
    if re.search(r'[A-Za-z0-9_]+:[A-Za-z0-9_]+', href):
        return ''
    if href.startswith(("http://", "https://", "mailto:", "tel:")):
        return href
    if href.startswith("/"):
        return urljoin(current, href)
    return urljoin(base_url, href)

# Remove Navigation Bars from all non-home pages
def remove_navigation_bars(html_content:str):
    soup = BeautifulSoup(html_content, 'html.parser')
    mw_panel_div = soup.find("div", id="mw_panel")
    if mw_panel_div:
        mw_panel_div.decompose()
    mw_head_div = soup.find("div", id="mw_head")
    if mw_head_div:
        mw_head_div.decompose()
    contents_index_div = soup.find("div", id="toc")
    if contents_index_div:
        contents_index_div.decompose()
    contents_index_div = soup.find("div", role="toc")
    if contents_index_div:
        contents_index_div.decompose()
    footer_tag = soup.find("footer")
    if footer_tag:
        footer_tag.decompose()
    return str(soup)

# Isolate body content from html content
def isolate_body_content(html_content:str):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_tag = soup.find("body")
    if body_tag:
        return str(body_tag)
    return html_content

# Function to remove duplicates from list
def remove_duplicates(list:list):
    unique_urls = []
    # Map unique urls in the list
    for item in list:
        if type(item) == dict:
            url = item['url']
            if url not in unique_urls:
                unique_urls.append(url)
            else:                           # For every url encountered that's already been mapped to unique_urls, remove entry
                list.remove(item)
        else:
            if item not in unique_urls:
                unique_urls.append(item)
            else:                           # For every url encountered that's already been mapped to unique_urls, remove entry
                list.remove(item)
    return list

# Function to remove entries comparing url with URL_STRINGS_TO_DROP, URLS_TO_DROP, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS and AUDIO_EXTENSIONS
def remove_entries_by_url(list:list):
    for item in list:
        if type(item) == dict:
            url = item['url'].strip().lower()
            for pattern in URL_STRINGS_TO_DROP:
                if (pattern in url) and (item in list):
                    list.remove(item)
            for pattern in URLs_TO_DROP:
                if (pattern in url) and (item in list):
                    list.remove(item)
            for pattern in IMAGE_EXTENSIONS:
                if (url.endswith(pattern)) and (item in list):
                    list.remove(item)
            for pattern in VIDEO_EXTENSIONS:
                if (url.endswith(pattern)) and (item in list):
                    list.remove(item)
            for pattern in AUDIO_EXTENSIONS:
                if (url.endswith(pattern)) and (item in list):
                    list.remove(item)
        else:
            for pattern in URL_STRINGS_TO_DROP:
                if (pattern in item.strip().lower()) and (item in list):
                    list.remove(item)
            for pattern in URLs_TO_DROP:
                if (pattern in item.strip().lower()) and (item in list):
                    list.remove(item)
            for pattern in IMAGE_EXTENSIONS:
                if (item.strip().lower().endswith(pattern)) and (item in list):
                    list.remove(item)
            for pattern in VIDEO_EXTENSIONS:
                if (item.strip().lower().endswith(pattern)) and (item in list):
                    list.remove(item)
            for pattern in AUDIO_EXTENSIONS:
                if (item.strip().lower().endswith(pattern)) and (item in list):
                    list.remove(item)
    return list

# Function to remove entries comparing title with TITLES_TO_DROP, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS and AUDIO_EXTENSIONS
def remove_entries_by_title(list:list):
    for item in list:
        if type(item) == dict:
            title = item['title'].strip().lower()
            for pattern in TITLES_TO_DROP:
                if (pattern in title) and (item in list):
                    list.remove(item)
        else:
            for pattern in TITLES_TO_DROP:
                if (pattern in item.strip().lower()) and (item in list):
                    list.remove(item)
    return list

# Function to get html content from url using scraperSession
def get_html_content(url:str, session:requests.Session=None):
    if session is None:
        session = scraperSession
    global fetchCount
    # If 3 calls have already failed, return empty
    if fetchCount>3:
        print(f"\nERROR: Retry Limit Exceeded for Url [{url}]....")
        fetchCount = 0
        return None
    fetchCount = fetchCount+1
    try:
        response = session.get(url, timeout=2)
        response.raise_for_status()
        # If Request Saturation Reached, wait 3 seconds, renew Session, and retry
        if "too many requests" in response.text.lower():
            print(f"ERROR: Request Saturated at Url [{url}]....\n\tWaiting for 3 seconds before retrying....\n")
            time.sleep(3)
            session.close()
            session = requests.Session()
            session.headers.update(SCRAPER_HEADERS)
            return get_html_content(url, session)
        return response.text
    except Exception as e:
        print(f"\nERROR: Fetching HTML Content:{e} for URL: \n{url}")
        return None

# Function to convert html/xml content to text
def xml_to_text(content):
    soup = BeautifulSoup(content, 'xml')
    return soup.get_text(separator='\n', strip=True)

def html_to_text(content):
    if content.lstrip().startswith('<?xml') or ('<?xml' in content.lstrip()):
        return xml_to_text(content)
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text(separator='\n', strip=True)

# Function to check URL availability using Head Request
def check_url_availability(url:str, session:requests.Session=None):
    if session is None:
        session = scraperSession
    try:
        if avoid_url_check(url):
            return False
        response = session.head(url, timeout=2)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"\nERROR: {e} for URL: \n{url}")
        return False

# Function to get all valid version numbers from software release history
def get_available_version_numbers(session:requests.Session=None):
    version_numbers = []
    release_history_html = get_html_content(RELEASE_HISTORIES, session)
    if release_history_html is None:
        return version_numbers
    soup = BeautifulSoup(release_history_html, 'html.parser')
    pre_cards = soup.find_all('pre')
    print(' ')
    # Isolate All Version Numbers
    for card in tqdm(pre_cards, desc='PROGRESS: Extracting version numbers from software release history'):
        version_match = re.search(r'Version\s*([\d\.]+)', card.text)
        if version_match:
            version_number = version_match.group(1)
            version_number = '.'.join(version_number.split('.')[:2])
            version_numbers.append(version_number)
    # Remove Duplicates
    version_numbers = remove_duplicates(version_numbers)
    # Check Validity for each version number
    for version in version_numbers:
        version_number = 'wice'+version.replace('.', '')
        version_home = WIKI_BASE_URL.replace('<VERSION_NUMBER>', version_number)
        if check_url_availability(version_home, session):
            COMPLETE_MAP[version] = [{
                'title': 'Home Page',
                'url': version_home
            }]
            VALID_VERSION_HOME_PAGES[version]= version_home
        else:
            version_numbers.remove(version)
    print(f"LOG: Available versions : {version_numbers}")
    return version_numbers

# Function to get context(related text/title) of an anchor tag
def get_context(anchor:BeautifulSoup):
    anchor_text = anchor.get_text(strip=True)
    parent_text = ''
    if anchor.parent and hasattr(anchor.parent, 'get_text'):
        parent_text = anchor.parent.get_text(" ", strip=True)
    context = ''
    if parent_text and anchor_text:
        idx = parent_text.find(anchor_text)
        if idx != -1:
            window = 60  # character window either side
            start = max(0, idx - window)
            end = min(len(parent_text), idx + len(anchor_text) + window)
            context = parent_text[start:end]
    return context.strip()

# Function to get the latest valid version number
def get_latest_version():
    version_numbers = VALID_VERSION_HOME_PAGES.keys()
    max_version = 0.0
    for version in version_numbers:
        if float(version) > float(max_version):
            max_version = version
    return max_version

# Function to map immediate hyperlinks from html content
def extract_immediate_hyperlinks(html_content:str, url:str, version:str):
    soup = BeautifulSoup(html_content, 'html.parser')
    hyperlinks = []
    for anchor in soup.find_all('a', href=True):
        text = anchor.get_text(strip=True)
        url = resolve_relative_url(anchor['href'], url, url).strip()
        includeFlag = False
        for url_to_include in URLs_TO_INCLUDE:
            if url_to_include in url:
                includeFlag = True
        if not includeFlag:
            continue
        if (url is None) or (url.strip() == ''):
            continue
        if avoid_url_check(url):
            continue
        if already_mapped(url):
            hyperlinks.append({
                'title': text,
                'url': url
            })
            continue
        if check_url_availability(url):
            hyperlinks.append({
                'title': text,
                'url': url
            })
            add_to_map(url, text, version)
    return hyperlinks

def init():
    start_time = time.time()
    valid_versions = get_available_version_numbers()
    latest_version = get_latest_version()

    end_time = time.time()
    execution_time = end_time - start_time
    minutes, seconds = divmod(execution_time, 60)
    print(f"LOG: Total Mapping Execution Time: {int(minutes)}m {seconds:.2f}s")
    return latest_version


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


# endpoints

@app.route(route="", methods=['GET'])
def index(req: func.HttpRequest) -> func.HttpResponse:
    """
    Index Page for the API
    Returns:
        message: str
        current_commit: str
    """
    last_commit_message = None
    latest_version = None
    last_commit_message = "Unable to retrieve commit message"
    try:
        latest_version = init()
        result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], 
                                capture_output=True,
                                  text=True)
        last_commit_message = result.stdout.strip()
    except Exception as e:
        last_commit_message = f"Unable to retrieve commit message: {e}"

   
    # if 'Unable to retrieve commit message' in last_commit_message:
    #     return func.HttpResponse(f"Welcome to the WICE Wiki API. This API is used to resolve version numbers, urls and get contents from the WICE Wiki Pages.", status_code=200)

    response_body = {
        "message": f"Welcome to the WICE Wiki API. This API is used to resolve version numbers, urls and get contents from the WICE Wiki Pages.",
        "latest_version": latest_version,       
        "last_commit_message": last_commit_message
    }  
    
    return func.HttpResponse(
        body=json.dumps(response_body),     
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )







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