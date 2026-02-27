import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
import json
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
    try:
         html_content = fetch_html_from_url(url)
         text_content = html_to_text(html_content)
         hyperlinks =   extract_hyperlinks(html_content)

         response_body = {
             "success": True,
             "url": url,
            "contentOfPage": text_content,
            "hyperlinksFromPage": hyperlinks
        }


         return  func.HttpResponse(
            body=json.dumps(response_body), 
            status_code=200,
            mimetype="application/json")
    
    except Exception as e:
        logging.error(f"Error fetching URL content: {e}")
        return func.HttpResponse(f"Error fetching URL content: {e}", status_code=500)   

def fetch_html_from_url(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def html_to_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def extract_hyperlinks(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return [a.get("href") for a in soup.find_all("a", href=True)]        