import requests

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

COMPLMETE_MAP = {}

# Function to remove duplicates from list
def remove_duplicates(list:list):
    unique_urls = []
    # Map unique urls in the list
    for item in list:
        if type(item) == dict:
            url = item['url']
            if url not in unique_urls:
                unique_urls.append(url)
            else:
                list.remove(item)
        else:
            if item not in unique_urls:
                unique_urls.append(item)
            else:
                list.remove(item)
    return list

# Function to remove entries comparing url with URL_STRINGS_TO_DROP, URLS_TO_DROP, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS and AUDIO_EXTENSIONS
def remove_entries_by_url(list:list):
    for item in list:
        if type(item) == dict:
            url = item['url'].strip().lower()
            for pattern in URL_STRINGS_TO_DROP:
                if pattern in url:
                    list.remove(item)
            for pattern in URLs_TO_DROP:
                if pattern in url:
                    list.remove(item)
            for pattern in IMAGE_EXTENSIONS:
                if url.endswith(pattern):
                    list.remove(item)
            for pattern in VIDEO_EXTENSIONS:
                if url.endswith(pattern):
                    list.remove(item)
            for pattern in AUDIO_EXTENSIONS:
                if url.endswith(pattern):
                    list.remove(item)
        else:
            for pattern in URL_STRINGS_TO_DROP:
                if pattern in item.strip().lower():
                    list.remove(item)
            for pattern in URLs_TO_DROP:
                if pattern in item.strip().lower():
                    list.remove(item)
            for pattern in IMAGE_EXTENSIONS:
                if item.strip().lower().endswith(pattern):
                    list.remove(item)
            for pattern in VIDEO_EXTENSIONS:
                if item.strip().lower().endswith(pattern):
                    list.remove(item)
            for pattern in AUDIO_EXTENSIONS:
                if item.strip().lower().endswith(pattern):
                    list.remove(item)
    return list

# Function to remove entries comparing title with TITLES_TO_DROP, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS and AUDIO_EXTENSIONS
def remove_entries_by_title(list:list):
    for item in list:
        if type(item) == dict:
            title = item['title'].strip().lower()
            for pattern in TITLES_TO_DROP:
                if pattern in title:
                    list.remove(item)
        else:
            for pattern in TITLES_TO_DROP:
                if pattern in item.strip().lower():
                    list.remove(item)
    return list

# Function to get html content from url using scraperSession

# Function to convert html/xml content to text

# Function to get all hyperlinks in html content

# Function to save map to json file

# Main Function

# Main Call