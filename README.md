# A2B (Arxiv to Bibliography)

> Replace arXiv links (or doi links) by their corresponding bibliography in markdowns. Inspired by [Mu Li](https://www.youtube.com/watch?v=q1G0xZCqYxY&ab_channel=MuLi).


![demo](https://github.com/kevinkevin556/arxiv2bib/raw/main/demo.gif)


This repo provides a tool to replace arXiv/DOI links saved in 

* [markdown files](#markdown) or
* [Notion database](#notion-database)

with their corresponding bibliographic information, which intends to create a more convenient experience for users in needs of searching, collecting, and taking notes of literatures. The script uses the Semantic Scholar API to retrieve information such as authors, title, journal, year, and citation count for a given arXiv paper.


## Installation

To install `a2b`, make sure you have [pip installed](https://pip.pypa.io/en/stable/installation/) and run:

```Bash
>> pip install a2b
```

## Usage

The tool can be run from the command line, e.g. to check the installed version of `a2b`,

```Bash
>> a2b --version
```


![](https://img.icons8.com/ios/2x/markdown.png)

### Markdown

#### 1. Generate markdown from a single arXiv link or DOI

For example:

```Bash
>> a2b --arXiv https://arXiv.org/abs/1912.08957

## __Optimization for deep learning: theory and algorithms.__ *Ruoyu Sun.* __ArXiv, 2019__ [(Arxiv)](https://arXiv.org/abs/1912.08957) 
## [(S2)](https://www.semanticscholar.org/paper/c23173e93f1db79a422e2af881a40afb96b8cb92) (Citations __114__)
```

Here you can use the link of pdf `https://arXiv.org/pdf/1912.08957.pdf`, instead of the link of arXiv page.

```Bash
>> a2b --doi https://doi.org/10.1007/BF00133570

## __Snakes: Active contour models.__ *M. Kass et al.* __International Journal of Computer Vision, 2004__ 
## [(Link)](https://doi.org/10.1007/BF00133570) [(S2)](https://www.semanticscholar.org/paper/9394a5d5adcb626128b6a42c8810b9505a3c6487)
## (Citations __15860__)
```

One can simply provide the DOI `10.1007/BF00133570` without adding the hyperlink prefix to generate bibilography from DOI.

#### 2. Replace arXiv links in a single markdown file

```Bash
>> a2b path/to/markdown.md
```

#### 3. Replace arXiv links in all markdown files within a directory

Run the following command to replace all arXiv links found in the given directory and its subdirectories.

```Bash
>> a2b path/to/directory
```

To replace arXiv links in the markdown files **ONLY** within the directory (subdirectories excluded), use arguments `--no-recursive` or `-nr`:

```Bash
>> a2b -nr path/to/directory
```

![](https://img.icons8.com/color/2x/notion--v1.png)

###  Notion Database

To generate bibliography from links saved in a Notion database, follow the instructions below

1. Create a new [Notion integration](https://www.notion.so/my-integrations) and keep the Notion API key obtained from the integration
2. Go to the Notion database and 
    * [Connect the Notion database to the integration](https://developers.notion.com/docs/create-a-notion-integration#step-2-share-a-database-with-your-integration) you just created
    * Create these columns (with data type matched) in the Notion database
      * Title (title)
      * Author (rich_text)
      * Year (number)
      * Journal (rich_text)
      * Arxiv (url)
      * Link (url)
      * S2 (url)
      * Citations (number)
3. Paste Arxiv links or doi links in the column `Title` and run the following command to activate the conversion

```Bash
>> a2b --notion notion_database_id --key notion_api_key
# or
>> a2b --notion notion_database_url --key notion api_key
```

You can choose to save your Notion API key as a environment variable `NOTION_API_KEY`, and then you can simply run without manually providing the key in command:

```Bash
>> a2b --notion notion_database_id
# or
>> a2b --notion notion_database_url
```



## Changelog

* **Version 1.0.5**
  * Support Notion database
  * Fix version command
* **Version 1.0.4**
  * Support creating bibliography from DOI links
  * Support querying a single arXiv link from terminal
