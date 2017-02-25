import unittest
from ldp.corpus_reader import (DepToken, parse_dep_sent, read_dep_corpus,
                               CONLLXToken, parse_conllx_sent, read_conllx_corpus)


class LDPTestCases(unittest.TestCase):

    def test_dep_corpus_reader(self):
        sent = parse_dep_sent(['1\tmi\t2\tP1', '2\tklama\t0\tROOT'])

        self.assertEquals(2, len(sent))
        self.assertEquals(DepToken('mi', 'KOhA', 2, 'P1'), sent[0])
        self.assertEquals(DepToken('klama', 'gismu', 0, 'ROOT'), sent[1])

        lines = """
1\tmi\t2\tP1
2\tklama\t0\tROOT

1\tko'a\t2\tP1
2\tbroda\t0\tROOT
        """
        sents = list(read_dep_corpus(lines.splitlines()))
        self.assertEquals(2, len(sents))
        self.assertEquals(2, len(sents[0]))
        self.assertEquals(2, len(sents[1]))
        self.assertEquals(DepToken("ko'a", 'KOhA', 2, 'P1'), sents[1][0])
        self.assertEquals(DepToken('broda', 'gismu', 0, 'ROOT'), sents[1][1])

    def test_conllx_corpus_reader(self):
        sent_str = "1	mi	_	KOhA	KOhA	_	2	P1	_	_"
        sent = parse_conllx_sent([sent_str])
        self.assertEquals(1, len(sent))
        token = CONLLXToken(form='mi', lemma='_', cpostag='KOhA', postag='KOhA', feats='_',
                            head=2, deprel='P1', phead='_', pdeprel='_')
        self.assertEquals(token, sent[0])

        lines = """
1	broda	_	gismu	gismu	_	0	ROOT	_	_

1	brode	_	gismu	gismu	_	0	ROOT	_	_
"""
        sents = list(read_conllx_corpus(lines.splitlines()))
        self.assertEquals(2, len(sents))
        self.assertEquals(1, len(sents[0]))
        self.assertEquals(1, len(sents[1]))
        self.assertEquals(CONLLXToken(form='broda', lemma='_', cpostag='gismu', postag='gismu',
                          feats='_', head=0, deprel='ROOT', phead='_', pdeprel='_'),
                          sents[0][0])
        self.assertEquals(CONLLXToken(form='brode', lemma='_', cpostag='gismu', postag='gismu',
                          feats='_', head=0, deprel='ROOT', phead='_', pdeprel='_'),
                          sents[1][0])


if __name__ == '__main__':
    unittest.main()
