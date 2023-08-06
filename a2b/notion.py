
import requests
import re
from .s2 import connect_to_s2, extract_metadata
from .message import red, yellow, prompt, get_update_message
from .link_utils import get_arxiv_id, get_doi



def get_database_id(text):
    uuid_len = 32
    if len(text) == uuid_len:
        database_id = text
    else:
        prog = re.compile(f"[a-zA-Z0-9]{{{uuid_len}}}(?=\?v)")
        match = prog.search(text)
        database_id = match.group(0) if match else None
    return database_id


def get_database_name(database_id, notion_api_key):
    endpoint = 'https://api.notion.com/v1'
    notion_headers = {
        'Notion-Version': '2021-08-16',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {notion_api_key}'
    }
    response = requests.get(
        f'{endpoint}/databases/{database_id}',
        headers=notion_headers
    )
    if response.status_code != 200:
        status = red(str(response.status_code))
        error_msg = yellow(response.json()['message'])
        raise ConnectionError(f"Status {status} - {error_msg}")
    return response.json()['title'][0]['plain_text']


def generate_page_data(s2_id, title, author, journal, year, citations, arxiv_id=None, doi=None):
    metadata = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Author": {"rich_text": [{"text": {"content": author+"."}}]},
        "Journal": {"rich_text": [{"text": {"content": journal}}]},
        "Year": {"number": year},
        "Citations": {"number": citations},
        "S2": {"url": f"https://www.semanticscholar.org/paper/{s2_id}"}
    }
    if arxiv_id is not None:
        metadata['Arxiv'] = {"url": f"https://arxiv.org/abs/{arxiv_id}"}
    if doi is not None:
        metadata['Link'] = {"url": f"https://doi.org/{doi}"}
    return {'properties': metadata}


def update_page(page_id, notion_api_key, page_data):
    endpoint = f"https://api.notion.com/v1/pages/{page_id}"
    notion_headers = {
        'Notion-Version': '2021-08-16',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {notion_api_key}'
    }
    response = requests.patch(endpoint, headers=notion_headers, json=page_data)
    return response


def replace_links_in_db(database_id, notion_api_key, start_cursor=None):
    # Define the Notion API endpoint
    endpoint = 'https://api.notion.com/v1'
    notion_headers = {
        'Notion-Version': '2021-08-16',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {notion_api_key}'
    }

    # Show database name
    if start_cursor is None:
        db_name = get_database_name(database_id, notion_api_key)
        prompt(f"[In Notion database: {db_name}]")
        response = requests.post(
            f'{endpoint}/databases/{database_id}/query',
            headers=notion_headers
        )
    else:
    # Make the API call to retrieve the database contents
        response = requests.post(
            f'{endpoint}/databases/{database_id}/query',
            headers=notion_headers,
            json={"start_cursor": start_cursor}
        )

    # Extract the database contents and replace links with metadata
    for page in response.json()['results']:

        page_id = page.get("id")
        paper_title = page.get("properties").get(
            "Title").get("title")[0].get("plain_text")
        arxiv_id = get_arxiv_id(paper_title)
        doi = get_doi(paper_title)


        if doi:
            paper_data = connect_to_s2(doi=doi)
        elif arxiv_id:
            paper_data = connect_to_s2(arxiv_id=arxiv_id)
        else:
            paper_data = None

        if paper_data:
            s2_id, title, authors, journal, year, citations = extract_metadata(
                paper_data)
            page_data = generate_page_data(
                s2_id, title, authors, journal, year, citations, arxiv_id, doi)
            page_resp = update_page(page_id, notion_api_key, page_data)
            if page_resp.status_code == 200:
                print(get_update_message(paper_title, title, journal, year))
            else:
                status = red(str(page_resp.status_code))
                error_msg = yellow(page_resp.json()['message'])
                raise ConnectionError(f"Status {status} - {error_msg}")

    # Retrieve more contents from the database if there is any
    if response.json()['has_more']:
        replace_links_in_db(database_id, notion_api_key,
                            response.json()["next_cursor"])
