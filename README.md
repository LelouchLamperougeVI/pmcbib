# pmcbib

If you're anything like me, then you probably use a citation manager such as Mendeley or Zotero, and use the browser plugin to conveniently add citations to your library. Everything is _rainbows and unicorns_ until it's time for dissemination :scream:. Enter `pmcbib`, a friendly utility written in python that checks your .bib file against the PubMed database to find all the fudge-ups.

> Very pre-alpha release...

## Dependencies
* python 3.7
* metapub
* bibtexparser
* python-Levenshtein
* internet connection (duh!)

## Installation

`pip install git+https://github.com/LelouchLamperougeVI/pmcbib.git`

## Usage

```
pmcbib [-h] [-c config.json] [-r report.md] [-v] [-w L] file.bib

positional arguments:
  file.bib              ye olde bibtex file

optional arguments:
  -h, --help            show this help message and exit
  -c config.json, --config config.json
                        config file
  -r report.md, --report report.md
                        report outputted as a MarkDown file (default no
                        output)
  -v, --verbose         turn on verbose (overwrites -w)
  -w L, --warn L        minimum warning level to report on console
  ```
