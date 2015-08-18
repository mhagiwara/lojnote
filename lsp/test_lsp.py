import unittest
import camxes
import lsp

class TestLojbanSemanticParser(unittest.TestCase):

    def testNumberSumtiInSentence(self):
        parse = camxes.parse('mi klama fi la .atlantas. le dargu fe la bastn. le karce')
        print parse
        lsp.semantic_parse(parse)
        selbri = parse.sentence[0].bridiTail3[0].BRIVLA[0]
        self.assertEqual((selbri, 1), parse.sentence[0].CMAVO[0].place)
        self.assertEqual((selbri, 2), parse.sentence[0].bridiTail3[0].terms[0].term1[1].sumti6[0].place)
        self.assertEqual((selbri, 3), parse.sentence[0].bridiTail3[0].terms[0].sumti6[1].place)
        self.assertEqual((selbri, 4), parse.sentence[0].bridiTail3[0].terms[0].term1[0].sumti6[0].place)
        self.assertEqual((selbri, 5), parse.sentence[0].bridiTail3[0].terms[0].sumti6[0].place)

if __name__ == '__main__':
    unittest.main()
