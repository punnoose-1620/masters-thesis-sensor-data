"""
Requirements to get authentication access for SharePoint :
1. Register a new application in Organization's Microsoft Entra ID
2. Internal admin must grant permission Sites.Selected
Above access only grants permission to certain directories.

Required Authentication Parameters :
- Tenant ID
- Client ID
- Client Secret (or Certificate)
"""

# auth.py
import os
import msal
import requests
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("SHAREPOINT_TENANT_ID")
CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET")

# TODO: Populate with actual values
HOSTNAME = "yourcompany.sharepoint.com"
SITENAME = "KnowledgeBase"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]  # Required for app-only tokens

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# Basic Authentication to get access token
def get_access_token():
    """
    Gets the access token for the SharePoint API.
    Returns (Response):
        The access token for the SharePoint API.
    """
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in result:
        raise Exception(f"Token acquisition failed: {result.get('error_description')}")

    return result["access_token"]

# Resolve Sharepoint Site and Library IDs
def get_site_id(hostname, site_name):
    """
    Gets the site ID for the given hostname and site name.
    Arguments:
        hostname (str): The hostname of the site.
        site_name (str): The name of the site.
    Returns (Response):
        The site ID for the given hostname and site name.
    """
    token = get_access_token()
    url = f"{GRAPH_BASE}/sites/{hostname}:/sites/{site_name}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

# Get Document Libraries in a given location in the GRAPH_BASE
def get_site_drives(site_id):
    """
    Gets the document libraries in a given location in the GRAPH_BASE.
    Arguments:
        site_id (str): The ID of the site.
    Returns (Response):
        The document libraries in a given location in the GRAPH_BASE.
    """
    token = get_access_token()
    url = f"{GRAPH_BASE}/sites/{site_id}/drives"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

# List the Files inside a Given drive in the GRAPH_BASE
def list_drive_root_items(drive_id):
    """
    Lists the files inside a given drive in the GRAPH_BASE.
    Arguments:
        drive_id (str): The ID of the drive.
    Returns (Response):
        The files inside a given drive in the GRAPH_BASE.
    """
    token = get_access_token()
    url = f"{GRAPH_BASE}/drives/{drive_id}/root/children"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

# Recursively lists all file items in a drive (or under a folder).
def list_all_drive_files(drive_id, folder_item_id="root"):
    """
    Recursively lists all file items in a drive (or under a folder).
    Arguments:
        drive_id (str): The ID of the drive.
        folder_item_id (str): The folder item ID, or "root" for drive root.
    Returns (Response):
        A flat list of all file items (folders are walked, not included as items).
    """
    token = get_access_token()
    if folder_item_id == "root":
        url = f"{GRAPH_BASE}/drives/{drive_id}/root/children"
    else:
        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{folder_item_id}/children"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json()["value"]
    files = []
    for item in items:
        if "folder" in item:
            files.extend(list_all_drive_files(drive_id, item["id"]))
        else:
            files.append(item)
    return files

# Gets a single drive item (file or folder) by id.
def get_drive_item(drive_id, item_id):
    """
    Gets a single drive item (file or folder) by id.
    Arguments:
        drive_id (str): The ID of the drive.
        item_id (str): The ID of the item.
    Returns (Response):
        The drive item metadata (name, size, id, etc.).
    """
    token = get_access_token()
    url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Gets the raw content (bytes) of a drive item (file).
def get_drive_item_content(drive_id, item_id):
    """
    Gets the raw content (bytes) of a drive item (file).
    Arguments:
        drive_id (str): The ID of the drive.
        item_id (str): The ID of the file item.
    Returns (Response):
        The file content as bytes.
    """
    token = get_access_token()
    url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/content"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content

# Flow to use for endpoint : 
# 1. Resolve site
# site_id = get_site_id(HOSTNAME, SITENAME)

# 2. Get libraries
# drives = get_site_drives(site_id)
# target_drive = [d for d in drives if d["name"] == "Documents"][0]

# 3. List files in the library
# items = list_drive_root_items(target_drive["id"])
