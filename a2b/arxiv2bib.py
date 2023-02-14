import os
import argparse
import requests
from requests.exceptions import ConnectionError

def extract_metadata(arxiv_id):
    fields = ["year", "authors", "title", "journal", "venue", "citationCount"]
    api_url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields={','.join(fields)}"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise ConnectionError

    paper_data = response.json()
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

    return title, authors, journal, year, citations

def find_arxiv_links(file_path):
    arxiv_links = []
    with open(file_path, "r", encoding='UTF-8') as f:
        for content in iter(f):
            arxiv_links += [link for link in content.split(" ") if link.startswith("https://arxiv.org/abs/")]
    return arxiv_links

def generate_markdown(title, authors, journal, year, arxiv_link, citations):
    markdown = f"**{title}.** "
    markdown += f"*{authors}.* "
    markdown += f"**{journal}, {str(year)}** "
    markdown += f"[(Arxiv)]({arxiv_link}) "
    markdown += f"(Citations **{str(citations)}**)\n"
    return markdown


def replace_arxiv_links(file_path):
    arxiv_links = find_arxiv_links(file_path)
    if len(arxiv_links) > 0:
        print("\033[92m" + f"[In {file_path}]" + "\033[0m")
    with open(file_path, "r", encoding='UTF-8') as f:
        content = f.read()
    for arxiv_link in arxiv_links:
        arxiv_id = arxiv_link.split("/")[-1].rstrip()
        title, authors, journal, year, citations = extract_metadata(arxiv_id)
        print(get_update_message(arxiv_id, title, journal, year))
        markdown = generate_markdown(title, authors, journal, year, arxiv_link, citations)
        content = content.replace(arxiv_link, markdown)
    with open(file_path, "w", encoding='UTF-8') as f:
        f.write(content)

def get_update_message(arxiv_id, title, journal, year):
    msg = "\033[92m"+ " * " + "\033[0m"
    msg += f"https://arxiv.org/abs/{arxiv_id} = "
    msg += "\033[93m"+ f"{title}. " + "\033[0m"
    msg += f"{journal}, "
    msg += "\033[91m"+ f"{year} " + "\033[0m"
    return msg


def replace_links_in_dir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if file_path.endswith(".md"):
            replace_arxiv_links(file_path)


def main():
    description = "Replace arxiv links in the markdown files by their corresponding bibliography."
    help_path = "path of a markdown or a directory containing markdowns."
    help_nr = "replace arxiv links in markdowns only under the given directory"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("path", help=help_path)
    parser.add_argument("-nr", "--no-recursive", dest="recursive", action="store_false", help=help_nr)
    args = parser.parse_args()

    if os.path.isfile(args.path):
        if args.path.endswith(".md"):
            replace_arxiv_links(args.path)
    elif args.recursive:
        for dir, _, _ in os.walk(args.path):
            replace_links_in_dir(dir)
    else:
        replace_links_in_dir(args.path)

    print("\033[92m" + "[Done]" + "\033[0m")


if __name__ == "__main__":
    main()
