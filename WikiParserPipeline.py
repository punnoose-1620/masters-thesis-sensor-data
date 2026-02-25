import re
import json
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

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
    'wireguard.com',
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
    if url.strip() == '':
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
    response = session.get(url, timeout=1)
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
    return version_numbers

# Function to get context of an anchor tag
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

# Function to get all immediate hyperlinks in html content. Reset fetchCount for every URL
def get_all_hyperlinks(ref_url:str, version:str, session:requests.Session=None):
    # if ref_url.endswith('/Quick_Start'):
    #     print('\nLOG: Getting all hyperlinks for Quick Start url: ', ref_url)
    global fetchCount
    fetchCount = 0
    unique_urls = []
    html_content = get_html_content(ref_url, session)
    text_content = html_to_text(html_content)
    parser = 'html.parser'
    if text_content.lstrip().startswith('<?xml') or ('<?xml' in text_content.lstrip()):
        parser = 'xml'
    soup = BeautifulSoup(html_content, parser)
    for anchor in soup.find_all('a', href=True):
        context = get_context(anchor)
        url = resolve_relative_url(anchor['href'], ref_url, VALID_VERSION_HOME_PAGES[version])
        valid_flag = False
        # Check if URL is valid and new
        if (url is not None) and (url.strip() != ''):
            valid_flag = True
        if url in [item['url'].strip() for item in unique_urls]:
            continue
        if already_mapped(url):
            continue
        if not valid_flag:
            continue
        # If URL is valid and new, add it to unique_urls
        if check_url_availability(url, session):
            unique_urls.append({
                'url': url,
                'title': context
            })
    return unique_urls

# Function to save map to json file
def save_json_to_file(content, file_path):
    """
    Saves the given content to a JSON file.

    Args:
        content (dict or list): The JSON-serializable content to write.
        file_path (str): Destination path for the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

# Function to get the latest version number
def get_latest_version():
    version_numbers = VALID_VERSION_HOME_PAGES.keys()
    max_version = 0.0
    for version in version_numbers:
        if float(version) > float(max_version):
            max_version = version
    return max_version

# Function to entirely map a given version
def _map_one_version(version: str):
    """Runs in a thread; maps a single version and writes to COMPLETE_MAP[version]."""
    urls_found = 0
    session = requests.Session()
    session.headers.update(SCRAPER_HEADERS)
    unique_entries = []
    url = VALID_VERSION_HOME_PAGES[version]
    unique_entries = get_all_hyperlinks(url, version, session)
    urls_found += len(unique_entries)
    unique_entries = remove_duplicates(unique_entries)
    unique_entries = remove_entries_by_url(unique_entries)
    unique_entries = remove_entries_by_title(unique_entries)
    COMPLETE_MAP[version] = unique_entries
    last_entry = unique_entries[-1]
    pbar = tqdm(
        unique_entries, 
        desc=f'PROGRESS: Mapping subpages for {version}.... ', 
        unit=' urls'
        )
    for entry in pbar:
        if entry==last_entry:
            pbar.set_description(f'PROGRESS: Mapping Quick Start flow for {version}.... ')
        url = entry['url']
        new_entries = get_all_hyperlinks(url, version, session)
        new_entries = remove_duplicates(new_entries)
        new_entries = remove_entries_by_url(new_entries)
        new_entries = remove_entries_by_title(new_entries)
        unique_entries.extend(new_entries)
    COMPLETE_MAP[version].extend(unique_entries)
    COMPLETE_MAP[version] = remove_duplicates(COMPLETE_MAP[version])
    COMPLETE_MAP[version] = remove_entries_by_url(COMPLETE_MAP[version])
    COMPLETE_MAP[version] = remove_entries_by_title(COMPLETE_MAP[version])
    session.close()
    return version, urls_found

# Main Function
def main():
    total_urls_found = 0
    valid_versions = get_available_version_numbers()
    start_time = time.time()
    latest_version = get_latest_version()

    print(f"LOG: Mapping Latest Version: {latest_version}")
    _map_one_version(latest_version)

    # print(f"LOG: Mapping {len(valid_versions)} versions: {valid_versions}")
    # print(f"LOG: {len(valid_versions)} Threads will be started, one for each version.")
    # # One thread per version (you have at most ~4 versions)
    # with ThreadPoolExecutor(max_workers=len(valid_versions)) as executor:
    #     results = list(executor.map(_map_one_version, valid_versions))
    #     for version, urls_found in results:
    #         total_urls_found += urls_found
    
    end_time = time.time()
    execution_time = end_time - start_time
    minutes, seconds = divmod(execution_time, 60)
    print(f"LOG: Total Mapping Execution Time: {int(minutes)}m {seconds:.2f}s")

    total_pages = 0
    print(f"Map Statistics:")
    for version in COMPLETE_MAP.keys():
        COMPLETE_MAP[version] = remove_duplicates(COMPLETE_MAP[version])
        COMPLETE_MAP[version] = remove_entries_by_url(COMPLETE_MAP[version])
        COMPLETE_MAP[version] = remove_entries_by_title(COMPLETE_MAP[version])
        total_pages += len(COMPLETE_MAP[version])
        print(f"\t{version}: {len(COMPLETE_MAP[version])}")
    print(f"Total Viable Pages Isolated: {total_pages}")
    print(f"Total URLs Found: {total_urls_found}")
    print(f"LOG: Latest Version: {latest_version}")
    save_json_to_file(COMPLETE_MAP, TARGET_FILE)

# Main Call
main()