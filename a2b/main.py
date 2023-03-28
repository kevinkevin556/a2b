import os
import argparse
import pkg_resources
from .message import prompt
from .markdown import query_single_link, replace_links, replace_links_in_dir
from .notion import replace_links_in_db, get_database_id


def main():
    description = "Replace arxiv links in the markdown files by their corresponding bibliography."
    help_path = "path of a markdown or a directory containing markdowns."
    help_nr = "replace arxiv links in markdowns only under the given directory"
    help_version = "retrieve the version of the installed a2b library"
    help_arxiv = "generate markdown from a single arxiv link"
    help_doi = "generate markdown from a single doi"
    help_notion = "the Notion database id"
    help_key = "the Notion API key"

    version_info = pkg_resources.require("a2b")[0].version
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("path", help=help_path)
    parser.add_argument("-nr", "--no-recursive", dest="recursive", action="store_false", help=help_nr)
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version_info}", help=help_version)
    parser.add_argument("--arxiv", action="store_true", help=help_arxiv)
    parser.add_argument("--doi", action="store_true", help=help_doi)
    parser.add_argument("--notion", action="store_true", help=help_notion)
    parser.add_argument('--key', type=str, help=help_key)
    args = parser.parse_args()

    
    # Query a single arxiv or doi link
    if args.arxiv or args.doi:
        link = args.path
        query_single_link(link, arxiv=args.arxiv)
    
    # Search in Notion database
    elif args.notion:
        database_id = get_database_id(args.path)
        api_key = args.key or os.environ.get('NOTION_API_KEY')
        if not api_key:
            raise ValueError("Notion API key is missing. Please provide it as an argument or set it as an environment variable.")
        replace_links_in_db(database_id, api_key)
        prompt("[DONE]")
    
    # Search in markdown files
    elif os.path.isfile(args.path) and args.path.endswith(".md"):
        replace_links(args.path)
        prompt("[DONE]")

    # Search in all markdown files in a directory
    elif args.recursive:
        for dir, _, _ in os.walk(args.path):
            replace_links_in_dir(dir)
        prompt("[DONE]")
        
    # all markdown files in a directory (except subdirectories)
    else:
        replace_links_in_dir(args.path)
        prompt("[DONE]")


if __name__ == "__main__":
    main()