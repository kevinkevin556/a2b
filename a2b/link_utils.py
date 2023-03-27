import re

def get_arxiv_id(arxiv_link):
    arxiv_id = re.search(r"\d{4}\.\d{4,5}", arxiv_link)
    if arxiv_id is not None:
        arxiv_id = arxiv_id.group()
    return arxiv_id


def get_doi(doi_link):
    doi = re.search(r"\b(10[.]\d{4,}(?:[.]\d+)*/(?:(?!['&\"<>])\S)+)\b", doi_link)
    if doi is not None:
        doi = doi.group(1)
    return doi