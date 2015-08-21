import unittest
import camxes
import lsp

class TestLojbanSemanticParser(unittest.TestCase):

    def testNumberSumtiInSentence(self):
        # test case - bare selbri
        parse = camxes.parse("broda")
        sparse = lsp.semantic_parse(parse)
        self.assertEqual(sparse['selbri'].lojban, "broda")

        # test case - without x1
        parse = camxes.parse("broda zo'e")
        sparse = lsp.semantic_parse(parse)
        self.assertEqual(sparse['selbri'].lojban, "broda")
        self.assertEqual(sparse[2].lojban, "zo'e")

        # test case - standard x1 to x4
        parse = camxes.parse("mi tavla do zo'e zo'e")
        sparse = lsp.semantic_parse(parse)
        self.assertEqual(sparse['selbri'].lojban, "tavla")
        self.assertEqual([sparse[i].lojban for i in [1, 2, 3, 4]], ["mi", "do", "zo'e", "zo'e"])

        # test case - standard x1 CMAVO and x2 sumti
        parse = camxes.parse("mi klama le zarci")
        sparse = lsp.semantic_parse(parse)
        selbri = parse.sentence[0].bridiTail3[0].BRIVLA[0]
        self.assertEqual(sparse['selbri'], selbri)
        self.assertEqual(sparse[1], parse.sentence[0].CMAVO[0])
        self.assertEqual(sparse[2], parse.sentence[0].bridiTail3[0].sumti6[0])

        # test case - standard
        parse = camxes.parse("mi cu klama le zarci")
        sparse = lsp.semantic_parse(parse)
        selbri = parse.sentence[0].bridiTail3[0].BRIVLA[0]
        self.assertEqual(sparse['selbri'], selbri)
        self.assertEqual(sparse[1], parse.sentence[0].CMAVO[0])
        self.assertEqual(sparse[2], parse.sentence[0].bridiTail3[0].sumti6[0])

        # test case - changing place by FA and filling subsequent places
        parse = camxes.parse("mi klama fi la .atlantas. le dargu fe la bastn. le karce")
        sparse = lsp.semantic_parse(parse)
        selbri = parse.sentence[0].bridiTail3[0].BRIVLA[0]
        self.assertEqual(sparse['selbri'], selbri)
        self.assertEqual(sparse[1], parse.sentence[0].CMAVO[0])
        self.assertEqual(sparse[3], parse.sentence[0].bridiTail3[0].terms[0].term1[0].sumti6[0])
        self.assertEqual(sparse[4], parse.sentence[0].bridiTail3[0].terms[0].sumti6[0])
        self.assertEqual(sparse[2], parse.sentence[0].bridiTail3[0].terms[0].term1[1].sumti6[0])
        self.assertEqual(sparse[5], parse.sentence[0].bridiTail3[0].terms[0].sumti6[1])

if __name__ == '__main__':
    unittest.main()
