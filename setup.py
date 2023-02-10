from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name='arxiv2bib',
    version='1.0.0',
    description='Replace arxiv links by their corresponding bibliography.',
    long_description=long_description,
    url='https://github.com/kevinkevin556/arxiv2bib',
    author='Zhen-Lun Hong',
    author_email='kevink556@gmail.com',
    license='MIT',
    packages=["arxiv2bib"],
    entry_points={"console_scripts":[
        "a2b=arxiv2bib.arxiv2bib:main",
        "arxiv2bib=arxiv2bib.arxiv2bib:main"
    ]},
    zip_safe=False,
    keywords=['arxiv', "biblography"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License"
    ]
)