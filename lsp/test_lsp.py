import unittest
import camxes
import lsp

class TestLojbanSemanticParser(unittest.TestCase):

    def testNumberSumtiInSentence(self):
        # test case - without x1
        parse = camxes.parse("broda zo'e")
        lsp.semantic_parse(parse)
        selbri = parse.bridiTail3[0].BRIVLA[0]
        self.assertEqual((selbri, 2), parse.bridiTail3[0].CMAVO[0].place)

        # test case - standard x1 CMAVO and x2 sumti
        parse = camxes.parse("mi klama le zarci")
        lsp.semantic_parse(parse)
        selbri = parse.sentence[0].bridiTail3[0].BRIVLA[0]
        self.assertEqual((selbri, 1), parse.sentence[0].CMAVO[0].place)
        self.assertEqual((selbri, 2), parse.sentence[0].bridiTail3[0].sumti6[0].place)

        # test case - changing place by FA and filling subsequent places
        parse = camxes.parse("mi klama fi la .atlantas. le dargu fe la bastn. le karce")
        lsp.semantic_parse(parse)
        selbri = parse.sentence[0].bridiTail3[0].BRIVLA[0]
        self.assertEqual((selbri, 1), parse.sentence[0].CMAVO[0].place)
        self.assertEqual((selbri, 3), parse.sentence[0].bridiTail3[0].terms[0].term1[0].sumti6[0].place)
        self.assertEqual((selbri, 4), parse.sentence[0].bridiTail3[0].terms[0].sumti6[0].place)
        self.assertEqual((selbri, 2), parse.sentence[0].bridiTail3[0].terms[0].term1[1].sumti6[0].place)
        self.assertEqual((selbri, 5), parse.sentence[0].bridiTail3[0].terms[0].sumti6[1].place)

if __name__ == '__main__':
    unittest.main()
