from setuptools import setup

setup(
    name='arxiv2bib',
    version='1.0.0',
    description='Replace arxiv links by their corresponding bibliography.',
    url='https://github.com/kevinkevin556/arxiv2bib',
    author='Zhen-Lun Hong',
    author_email='kevink556@gmail.com',
    license='MIT',
    packages=["arxiv2bib"],
    entry_points={"console_scripts":[
        "a2b=arxiv2bib.arxiv2bib:main",
        "arxiv2bib=arxiv2bib.arxiv2bib:main"
    ]},
    zip_safe=False
)