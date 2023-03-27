import os
from .s2 import connect_to_s2, extract_metadata
from .message import prompt, get_update_message
from .link_utils import get_arxiv_id, get_doi


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


def query_single_link(link, arxiv=False):
    if arxiv:
        arxiv_id = get_arxiv_id(link)
        paper_data = connect_to_s2(arxiv_id=arxiv_id)
        s2_id, title, authors, journal, year, citations = extract_metadata(paper_data)
        markdown = generate_markdown(s2_id, title, authors, journal, year, citations, arxiv_id=arxiv_id)
        print(markdown)
    else:
        doi = get_doi(link)
        paper_data = connect_to_s2(doi=doi)
        s2_id, title, authors, journal, year, citations = extract_metadata(paper_data)
        markdown = generate_markdown(s2_id, title, authors, journal, year, citations, doi=doi)
        print(markdown)


def replace_links(file_path):
    # Find links/id of arxiv or doi from a markdown file
    arxiv_links = find_arxiv_links(file_path)
    doi_links = find_doi_links(file_path)

    # Show file path if any link is found
    if len(arxiv_links + doi_links) > 0:
        prompt(f"[In {file_path}]")
    
    # Read contents from the markdown and replace links with their metadata
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
        markdown = generate_markdown(s2_id, title, authors, journal, year, citations, arxiv_id, doi)
        content = content.replace(link, markdown)
        print(get_update_message(link, title, journal, year))
    
    # Write the file with the modified content
    with open(file_path, "w", encoding='UTF-8') as f:
        f.write(content)


def replace_links_in_dir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if file_path.endswith(".md"):
            replace_links(file_path)