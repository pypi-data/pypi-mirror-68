"""Setup file. The package can be installed for development by running

pip install -e .

or similar where . is replaced by the path to package root
"""
import pathlib

from setuptools import find_packages, setup

README_FILE_PATH = pathlib.Path(__file__).parent / "README.md"
with open(README_FILE_PATH) as f:
    README = f.read()

s = setup(  # pylint: disable=invalid-name
    name="awesome-panel",
    version="20200511.1",
    license="MIT",
    description="""This package supports the Awesome Panel Project and
    provides highly experimental features!""",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/MarcSkovMadsen/awesome-panel",
    author="Marc Skov Madsen",
    author_email="marc.skov.madsen@gmail.com",
    # package_data={"awesome_panel": ["py.typed"]},
    include_package_data=True,
    packages=find_packages(include=["awesome_panel", "awesome_panel.*"]),
    install_requires=["panel"],
    python_requires=">= 3.7",
    zip_safe=False,
)
