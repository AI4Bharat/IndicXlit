import pathlib
from setuptools import setup, find_packages
import pkg_resources

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

with pathlib.Path('dependencies.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

# This call to setup() does all the work
setup(
    name="ai4bharat-transliteration",
    version="1.0.0",
    description="Deep Transliteration for Indic Languages",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AI4Bharat/IndicXlit",
    author="AI4Bharat",
    author_email="opensource@ai4bharat.org",
    packages=["ai4bharat.transliteration"],
    # packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries"
    ],
)
