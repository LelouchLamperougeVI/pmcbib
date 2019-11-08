import re
from Levenshtein import ratio, jaro
from pmcbib.logger import logger
from pmcbib.pmdb import search

dictionary = {
    'author': 'authors',
    'year': 'year',
    'journal': 'journal',
    'title': 'title',
}

class validator():
    def __init__(self, ops):
        self.tags = ops['tags']
        self.threshold = ops['threshold']
        self.logger = logger(ops)

    def check_tags(self, entry):
        missing = list()
        try:
            for tag in self.tags[entry['ENTRYTYPE']]:
                if tag not in entry.keys() : missing.append(tag)
        except KeyError:
            return True, missing, False

        crit = len(missing) == 0
        for tag in self.tags['all']:
            if tag not in entry.keys() : missing.append(tag)

        return crit, missing, True

    def parse_auth(self, s):
        auth = s.split(' and ')
        for i in range(len(auth)):
            temp = auth[i].split(', ')
            temp[0] = ''.join(re.findall(r"[ a-zA-Z]", temp[0]))
            temp[1] = ''.join(re.findall(r"\b[A-Z]", temp[1]))
            auth[i] = ' '.join(temp)
        return auth

    def cmp_auth(self, s1, s2):
        if len(s1) != len(s2): return False, False
        matching, sorted = True, True
        sim_mat = [[jaro(s1[y], s2[x]) for x in range(len(s2))] for y in range(len(s1))]
        for i in range(len(s2)):
            if max(sim_mat[i]) != sim_mat[i][i]: sorted = False
            if max(sim_mat[i]) < self.threshold['author']: matching = False
        return matching, sorted

    def run(self, entry):
        self.logger.create(entry['ID'])
        article = search(entry)
        crit, missing, support = self.check_tags(entry)
        if not support:
            self.logger.log('No support for ' + entry['ENTRYTYPE'] + '. Currently, only the following entry types are supported: ' + ', '.join(set(self.tags.keys()).symmetric_difference({'all'})), 2)
            self.logger.print()
            return
        if not crit:
            self.logger.log('missing critical tag(s): ' + ' '.join(missing), 3)
            self.logger.print()
            return
        if article is None:
            self.logger.log('article could not be found on PubMed', 2)
            self.logger.print()
            return
        if len(missing) > 0:
            self.logger.log('the following tags are missing: ' + ' '.join(missing), 1)
            self.logger.unindent()

        # compare authors list
        matching, sorted = self.cmp_auth(self.parse_auth(entry['author']), article.authors)
        if not matching:
            self.logger.log('authors mismatch:', 3)
            self.logger.log('PM:  ' + ' & '.join(article.authors), 3)
            self.logger.unindent()
            self.logger.log('bib: ' + ' & '.join(self.parse_auth(entry['author'])), 3)
            self.logger.unindent()
            self.logger.unindent()
        elif not sorted:
            self.logger.log('authors list misordered:', 3)
            self.logger.log('PM:  ' + ' & '.join(article.authors), 3)
            self.logger.unindent()
            self.logger.log('bib: ' + ' & '.join(self.parse_auth(entry['author'])), 3)
            self.logger.unindent()
            self.logger.unindent()

        # critical comparisons
        for tag in set(self.tags[entry['ENTRYTYPE']]).symmetric_difference({'author'}):
            if self.threshold[tag] > jaro(article.__dict__[dictionary[tag]].strip('~`!@#$%^&*()_-+=[]{}<>.,:;\\/?').lower(), entry[tag].strip('~`!@#$%^&*()_-+=[]{}<>.,:;\\/?').lower()):
                self.logger.log(tag + ' mismatch:', 3)
                self.logger.log('PM:  ' + article.__dict__[dictionary[tag]].strip('~`!@#$%^&*()_-+=[]{}<>.,:;\\/?'), 3)
                self.logger.unindent()
                self.logger.log('bib: ' + entry[tag].strip('~`!@#$%^&*()_-+=[]{}<>.,:;\\/?'), 3)
                self.logger.unindent()
                self.logger.unindent()

        self.logger.print()
