import requests

def connect_to_s2(arxiv_id=None, doi=None):
    fields = ["year", "authors", "title", "journal", "venue", "citationCount"]
    if arxiv_id is not None:
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields={','.join(fields)}"
    elif doi is not None:
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields={','.join(fields)}"
    else:
        raise ValueError("Either arxiv_id or doi should be provided.")

    response = requests.get(api_url)
    if response.status_code != 200:
        if arxiv_id is not None:
            raise ConnectionError(f"Unable to find arxiv paper with id = {arxiv_id}")
        else:
            raise ConnectionError(f"Unable to find paper with DOI = {doi}")
    
    paper_data = response.json()
    return paper_data


def extract_metadata(paper_data):
    s2_id = paper_data["paperId"]
    title = paper_data["title"]
    if len(paper_data["authors"]) <= 2:
        authors = ", ".join([author["name"] for author in paper_data["authors"]])
    else:
        authors = paper_data["authors"][0]["name"] + " et al"
    if paper_data.get("journal") is not None:
        journal = paper_data["journal"].get("name")
        if journal is None:
            journal = paper_data["venue"]
    else:
        journal = "Working Paper"
    year = paper_data.get("year", "UNKNOWN-YEAR")
    citations = paper_data.get("citationCount")
    return s2_id, title, authors, journal, year, citations