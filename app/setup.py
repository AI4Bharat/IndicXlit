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

# Read meta-data
about = {}
exec(open('ai4bharat/transliteration/__metadata.py').read(), about)

# This call to setup() does all the work
setup(
    name="ai4bharat-transliteration",
    version=about["__version__"],
    description="Indic-Xlit: Transliteration library for Indic Languages. Conversion of text from English to 21 languages of South Asia.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AI4Bharat/IndicXlit",
    project_urls={
        # 'Say Thanks': 'mailto:opensource@ai4bharat.org',
        'Our Research': 'https://ai4bharat.org/transliteration',
        'Demo Website': 'https://xlit.ai4bharat.org',
        'Report Issues': 'https://github.com/AI4Bharat/IndicXlit/issues',
        'Source Code': 'https://github.com/AI4Bharat/IndicXlit/tree/master/app',
    },
    author="AI4Bhārat",
    author_email="opensource@ai4bharat.org",
    # packages=["ai4bharat.transliteration"],
    packages=find_packages(exclude=("tests",)),
    # packages=find_packages(include=('ai4bharat.transliteration*')),
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries"
    ],
)
