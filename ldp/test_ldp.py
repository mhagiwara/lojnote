import unittest
from ldp import camxes
from ldp import depparser
from ldp.corpus_reader import (DepToken, parse_dep_sent, read_dep_corpus,
                               CONLLXToken, parse_conllx_sent, read_conllx_corpus)
from ldp.eval import evaluate_sent, evaluate


class LDPTestCases(unittest.TestCase):

    def test_camxes(self):
        tagged_words = list(camxes.tag(""))
        self.assertEquals([], tagged_words)

        tagged_words = list(camxes.tag("ko'a broda"))
        self.assertEquals([("ko'a", 'KOhA'), ('broda', 'gismu')], tagged_words)

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

    def test_eval(self):
        ans_str = ["1	mi	_	KOhA	KOhA	_	2	P1	_	_",
                   "2	broda	_	gismu	gismu	_	0	ROOT	_	_"]
        sys_str = ["1	mi	_	KOhA	KOhA	_	1	PX	_	_",
                   "2	broda	_	gismu	gismu	_	0	ROOTX	_	_"]

        ans_sent = parse_conllx_sent(ans_str)
        sys_sent = parse_conllx_sent(sys_str)
        stats = evaluate_sent(ans_sent, sys_sent)
        self.assertEquals(2, stats['num_tokens'])
        self.assertEquals(1, stats['unlabeled_matches'])
        self.assertEquals(0, stats['labeled_matches'])

        ans_corpus = list(read_conllx_corpus(ans_str))
        sys_corpus = list(read_conllx_corpus(sys_str))
        results = evaluate(ans_corpus, sys_corpus)
        self.assertAlmostEquals(0.5, results['UAS'])
        self.assertAlmostEquals(0.0, results['LAS'])

    def test_depparse(self):
        parse = list(depparser.parse(""))
        self.assertEqual([], parse)

        sent = list(depparser.parse("ko'a broda"))[0]
        self.assertEqual(2, len(sent))
        self.assertEqual("ko'a", sent[0].form)
        self.assertEqual("broda", sent[1].form)


if __name__ == '__main__':
    unittest.main()
