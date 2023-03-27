import toml
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

metadata = toml.load(open("pyproject.toml"))["tool"]["poetry"]

setuptools.setup(
    name=metadata["name"],
    version=metadata["version"],
    description=metadata["description"],
    long_description=long_description,
    long_description_content_type=metadata["long_description_content_type"],
    url=metadata["url"],
    author=metadata["author"],
    author_email=metadata["author_email"],
    license=metadata["license"],
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["a2b=a2b.main:main"]},
    zip_safe=False,
    keywords=metadata["keywords"],
    classifiers=metadata["classifiers"],
)
