# pmcbib

If you're anything like me, then you probably use a citation manager such as Mendeley or Zotero, and use the browser plugin to conveniently add citations to your library. Everything is _rainbows and unicorns_ until it's time for dissemination :scream:. Enter `pmcbib`, a friendly utility written in python that checks your .bib file against the PubMed database to find all the fudge-ups.

> version 0.0.2.dev1 added support for aliasing and makes use of stdout/stderr (see example use case)

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
pmcbib [-h] [-c config.json] [-o] [-r report.md] [-v] [-w L] file.bib

positional arguments:
  file.bib              ye olde bibtex file

optional arguments:
  -h, --help            show this help message and exit
  -c config.json, --config config.json
                        config file
  -o, --output          output automatically corrected bibtex entries on
                        STDOUT
  -r report.md, --report report.md
                        report outputted as a MarkDown file (default no
                        output)
  -v, --verbose         turn on verbose (overwrites -w)
  -w L, --warn L        minimum warning level to report on console (STDERR)

  ```

  ## Examples
  ### Generate a report for a given bibtex file
  ```
  pmcbib -r report.md example.bib

  to suppress warning messages:
  pmcbib -r report.md -w 4 example.bib
  or
  pmcbib -r report.md example.bib 2> /dev/null
  ```

  ### Automatically correct bibtex file and save as separate file
  ``` pmcbib -o example.bib > corrected.bib ```

  __`pmcbib` will automatically try to fix identified issues. However, it is strongly recommended for the user to go over the report before committing to the output.__

  ### Use custom configuration file
  ``` pmcbib -c ~/.config/pmcbib/config.json example.bib ```
