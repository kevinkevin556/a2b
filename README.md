# A2B (Arxiv to Bibliography)

#### Replace arxiv links by their corresponding bibliography in markdowns. Inspired by [Mu Li](https://www.youtube.com/watch?v=q1G0xZCqYxY&ab_channel=MuLi).


![demo](https://github.com/kevinkevin556/arxiv2bib/raw/main/demo.gif)


This repo provides a tool to replace arXiv links in markdown files with their corresponding bibliographic information. The script uses the Semantic Scholar API to retrieve information such as authors, title, journal, year, and citation count for a given arXiv paper.

**Start from version 1.0.4 , we support creating bibliography from DOI links.**

## Installation

To install `a2b`, make sure you have [pip installed](https://pip.pypa.io/en/stable/installation/) and run:

```Bash
>> pip install a2b
```

## Usage

The tool can be run from the command line. Either a link, a file or a directory can be taken as the argument.

### Generate markdown from a single arxiv link or DOI

For example:

```Bash
>> a2b --arxiv https://arxiv.org/abs/1912.08957

## __Optimization for deep learning: theory and algorithms.__ *Ruoyu Sun.* __ArXiv, 2019__ [(Arxiv)](https://arxiv.org/abs/1912.08957) 
## [(S2)](https://www.semanticscholar.org/paper/c23173e93f1db79a422e2af881a40afb96b8cb92) (Citations __114__)
```

Here you can use the link of pdf `https://arxiv.org/pdf/1912.08957.pdf`, instead of the link of arxiv page.

```Bash
>> a2b --doi https://doi.org/10.1007/BF00133570

## __Snakes: Active contour models.__ *M. Kass et al.* __International Journal of Computer Vision, 2004__ 
## [(Link)](https://doi.org/10.1007/BF00133570) [(S2)](https://www.semanticscholar.org/paper/9394a5d5adcb626128b6a42c8810b9505a3c6487)
## (Citations __15860__)
```

One can simply provide the DOI `10.1007/BF00133570` without adding the hyperlink prefix to generate bibilography from DOI.


### Replace arxiv links in a single markdown file

```Bash
>> a2b path/to/markdown.md
```

### Replace arxiv links in all markdown files within a directory 

Run the following command to replace all arxiv links found in the given directory and its subdirectories.

```Bash
>> a2b path/to/directory
```

To replace arxiv links in the markdown files **ONLY** within the directory (subdirectories excluded), use arguments `--no-recursive` or `-nr`:

```Bash
>> a2b -nr path/to/directory
```
