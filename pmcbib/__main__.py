import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from pmcbib.validate import validator
import argparse
from json import load
from pkg_resources import resource_stream

def main():
    parser = argparse.ArgumentParser(description='pmcbib - Python utility for validating bibtex files against PubMed database')
    parser.add_argument('-c', '--config', metavar='config.json', default=None, help='config file')
    parser.add_argument('-o', '--output', action='store_true', help='output automatically corrected bibtex entries on STDOUT')
    parser.add_argument('-r', '--report', metavar='report.md', default=None, help='report outputted as a MarkDown file (default no output)')
    parser.add_argument('-v', '--verbose', action='store_true', help='turn on verbose (overwrites -w)')
    parser.add_argument('-w', '--warn', default=2, metavar='L', help='minimum warning level to report on console (STDERR)')
    parser.add_argument('bibfile', metavar='file.bib', help="ye olde bibtex file")

    args = parser.parse_args()

    if args.config is not None:
        with open(args.config) as cfg_file: cfg = load(cfg_file)
    else:
        cfg = load(resource_stream('pmcbib', 'data/config.json'))

    if args.verbose:
        cfg.update({'lvl': 0})
    else:
        cfg.update({'lvl': args.warn})
    cfg.update({'report': args.report})
    validate = validator(cfg)

    with open(args.bibfile) as bib_file:
        bibdb = bibtexparser.load(bib_file)

    corrected = BibDatabase()
    for entry in bibdb.entries:
        centry = validate.run(entry)
        if args.output:
            corrected.entries = [centry]
            print(bibtexparser.dumps(corrected))

    validate.logger.dump()

if __name__ == "__main__":
    main()
