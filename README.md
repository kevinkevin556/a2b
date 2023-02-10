# A2B (Arxiv to Bibliography)

#### Replace arxiv links by their corresponding bibliography in markdowns. Inspired by [Mu Li](https://www.youtube.com/watch?v=q1G0xZCqYxY&ab_channel=MuLi).


![demo](https://github.com/kevinkevin556/arxiv2bib/raw/main/demo.gif)


This repo provides a tool to replace arXiv links in markdown files with their corresponding bibliographic information. The script uses the Semantic Scholar API to retrieve information such as authors, title, journal, year, and citation count for a given arXiv paper.

## Installation

To install `a2b`, make sure you have [pip installed](https://pip.pypa.io/en/stable/installation/) and run:

```Bash
pip install a2b
```

## Usage

The tool can be run from the command line by passing the file path or directory path as an argument.

### Replace arxiv links in a single markdown file

```Bash
a2b path/to/markdown.md
```

### Replace arxiv links in all markdown files within a directory 

Run the following command to replace all arxiv links found in the given directory and its subdirectories.

```Bash
a2b path/to/directory
```

To replace arxiv links in the markdown files **ONLY** within the directory (not recursively), use arguments `--no-recursive` or `-nr`:

```Bash
a2b -nr path/to/directory
```
