from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name='a2b',
    version='1.0.2',
    description='Replace arxiv links in markdowns by their corresponding bibliography.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kevinkevin556/arxiv2bib',
    author='Zhen-Lun Hong',
    author_email='kevink556@gmail.com',
    license='MIT',
    packages=["a2b"],
    entry_points={"console_scripts":[
        "a2b=a2b.arxiv2bib:main",
    ]},
    zip_safe=False,
    keywords=['arxiv', "biblography", "markdown"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License"
    ]
)