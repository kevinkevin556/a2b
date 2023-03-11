import os
import argparse
import requests
from requests.exceptions import ConnectionError
import pkg_resources
from .color_str import green, yellow, red


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


def find_arxiv_links(file_path):
    arxiv_links = []
    with open(file_path, "r", encoding='UTF-8') as f:
        for content in iter(f):
            for link in content.split(" "):
                arxiv_links += [link.rstrip()] if link.startswith("https://arxiv.org/") else []
    return arxiv_links


def find_doi_links(file_path):
    doi_links = []
    with open(file_path, "r", encoding='UTF-8') as f:
        for content in iter(f):
            for link in content.split(" "):
                if link.startswith("10.") or link.startswith("https://doi.org/10."):
                    doi_links += [link.rstrip()]  
    return doi_links


def generate_markdown(s2_id, title, authors, journal, year, citations, arxiv_id=None, doi=None):
    markdown = f"__{title}.__ "
    markdown += f"*{authors}.* "
    markdown += f"__{journal}, {str(year)}__ "
    if arxiv_id is not None:
        markdown += f"[(Arxiv)]({'https://arxiv.org/abs/'+str(arxiv_id)}) "
    if doi is not None:
        markdown += f"[(Link)]({'https://doi.org/'+str(doi)}) "
    markdown += f"[(S2)]({'https://www.semanticscholar.org/paper/'+str(s2_id)}) "
    markdown += f"(Citations __{str(citations)}__)"
    return markdown


def get_arxiv_id(arxiv_link):
    if arxiv_link.startswith("https://arxiv.org/abs/"):
        arxiv_id = arxiv_link.split("/")[-1]
    if arxiv_link.startswith("https://arxiv.org/pdf/"):
        arxiv_id = arxiv_link.split("/")[-1].rstrip()[:-4]
    return arxiv_id


def get_doi(doi_link):
    if doi_link.startswith("10."):
        return doi_link
    if doi_link.startswith("https://doi.org/10."):
        return doi_link[len("https://doi.org/"):]


def replace_links(file_path):
    arxiv_links = find_arxiv_links(file_path)
    doi_links = find_doi_links(file_path)
    if len(arxiv_links + doi_links) > 0:
        print(green(f"[In {file_path}]"))
    with open(file_path, "r", encoding='UTF-8') as f:
        content = f.read()
    for i, link in enumerate(arxiv_links+doi_links):
        if i < len(arxiv_links):
            arxiv_id, doi = get_arxiv_id(link), None
            paper_data = connect_to_s2(arxiv_id=arxiv_id)
        else:
            arxiv_id, doi = None, get_doi(link)
            paper_data = connect_to_s2(doi=doi)
        s2_id, title, authors, journal, year, citations = extract_metadata(paper_data)
        print(get_update_message(link, title, journal, year))
        markdown = generate_markdown(s2_id, title, authors, journal, year, citations, arxiv_id, doi)
        content = content.replace(link, markdown)
    with open(file_path, "w", encoding='UTF-8') as f:
        f.write(content)



def get_update_message(link, title, journal, year):
    return f" {green('*')} {link} = {yellow(title)+'.'} {journal}, {red(str(year))} "



def replace_links_in_dir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if file_path.endswith(".md"):
            replace_links(file_path)


def main():
    description = "Replace arxiv links in the markdown files by their corresponding bibliography."
    help_path = "path of a markdown or a directory containing markdowns."
    help_nr = "replace arxiv links in markdowns only under the given directory"
    help_version = "retrieve the version of the installed a2b library"
    help_arxiv = "generate markdown from a single arxiv link"
    help_doi = "generate markdown from a single doi"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("path", help=help_path)
    parser.add_argument("-nr", "--no-recursive", dest="recursive", action="store_false", help=help_nr)
    parser.add_argument("-v", "--version", dest="version", action="store_true", help=help_version)
    parser.add_argument("--arxiv", action="store_true", help=help_arxiv)
    parser.add_argument("--doi", action="store_true", help=help_doi)
    args = parser.parse_args()

    if args.version:
        print("a2b", pkg_resources.require("a2b")[0].version)
    elif args.arxiv:
        arxiv_id = get_arxiv_id(args.path)
        paper_data = connect_to_s2(arxiv_id=arxiv_id)
        s2_id, title, authors, journal, year, citations = extract_metadata(paper_data)
        markdown = generate_markdown(s2_id, title, authors, journal, year, citations, arxiv_id=arxiv_id)
        print(markdown)
    elif args.doi:
        doi = get_doi(args.path)
        paper_data = connect_to_s2(doi=doi)
        s2_id, title, authors, journal, year, citations = extract_metadata(paper_data)
        markdown = generate_markdown(s2_id, title, authors, journal, year, citations, doi=doi)
        print(markdown)
    else:
        if os.path.isfile(args.path):
            if args.path.endswith(".md"):
                replace_links(args.path)
        elif args.recursive:
            for dir, _, _ in os.walk(args.path):
                replace_links_in_dir(dir)
        else:
            replace_links_in_dir(args.path)
        print(green("[Done]"))


if __name__ == "__main__":
    main()
