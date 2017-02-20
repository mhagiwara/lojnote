import unittest
from ldp.corpus_reader import DepToken, parse_dep_sent, read_dep_corpus


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


if __name__ == '__main__':
    unittest.main()
