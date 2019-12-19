from datetime import datetime
import sys

severity = {
0: u"\u001b[0m",
1: u"\u001b[36m",
2: u"\u001b[33m",
3: u"\u001b[31m",
}

class logger():
    def __init__(self, ops):
        self.lvl = int(ops['lvl'])
        self.report = ops['report']
        self.lst = list()

    def create(self, post='noname'):
        self.current = dict({post: [0, 0]})
        self.lst.append(self.current)
        self.ind = 1 # indentation level

    def unindent(self):
        self.ind = max([self.ind - 1, 1])

    def log(self, msg, lvl=0):
        self.current.update({msg: [lvl, self.ind]})
        self.ind += 1

    def how_severe(self, d=None): # get max severity level for the given dictionary
        if d is None:
            d = self.current
        maxS = 0
        for lvl,_ in d.values(): maxS = max([maxS, lvl])
        return maxS

    def print(self): # print the current entry
        maxS = self.how_severe()
        if maxS >= self.lvl:
            for s,(lvl, ind) in self.current.items():
                tabs = ''.join(['\t' for t in range(ind)])
                print(severity[lvl] + tabs + s + severity[0], file=sys.stderr)

    def _dump(self, lvl):
        for i in range(len(self.lst)):
            if self.how_severe(self.lst[i]) == lvl:
                for s,(lvl, ind) in self.lst[i].items():
                    if ind == 0:
                        self.f.write('1. ' + s + '\n')
                        continue
                    tabs = ''.join(['\t' for t in range(ind)])
                    self.f.write(tabs + '* ' + s + '\n')

    def dump(self):
        if self.report is not None:
            self.f = open(self.report, 'w')
            self.f.write('# PMCBIB Report\n')
            self.f.write('The following report was generated using pmcbib\n\n')
            self.f.write('created on: ' + datetime.now().strftime('%A, %B %-d, %Y %H:%M:%S') + '\n\n')

            self.f.write('## Critical\n')
            self.f.write('The following entries are critically compromised:\n')
            self._dump(3)
            self.f.write('\n')

            self.f.write('## Medium\n')
            self.f.write('The following entries might have some issues:\n')
            self._dump(2)
            self.f.write('\n')

            self.f.write('## Low\n')
            self.f.write('The following entries have some minor issues:\n')
            self._dump(1)
            self.f.write('\n')
            self.f.close()
