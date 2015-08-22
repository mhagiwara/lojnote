import unittest
import camxes
import lsp

class TestLojbanSemanticParser(unittest.TestCase):

    def testNumberSumtiInSentence(self):

        def semantic_parse_text(text):
            return lsp.semantic_parse(camxes.parse(text))

        def compare_places(sparse, *places):
            self.assertEqual(sparse['selbri'].lojban, places[0])
            for i in xrange(1, len(places)):
                if places[i] is None:
                    self.assertTrue(i not in sparse)
                else:
                    self.assertEqual(sparse[i].lojban, places[i])

        # test case - bare selbri
        sparse = semantic_parse_text("broda")
        compare_places(sparse, "broda", None, None, None, None, None)

        # test case - without x1
        sparse = semantic_parse_text("broda zo'e")
        compare_places(sparse, "broda", None, "zo'e")

        # test case - standard x1 to x4
        sparse = semantic_parse_text("mi tavla do zo'e zo'e")
        compare_places(sparse, "tavla", "mi", "do", "zo'e", "zo'e")

        # test case - standard x1 CMAVO and x2 sumti
        sparse = semantic_parse_text("mi klama le zarci")
        compare_places(sparse, "klama", "mi", "le zarci")

        # test case - standard x1 CMAVO and x2 sumti with CU
        sparse = semantic_parse_text("mi cu klama le zarci")
        compare_places(sparse, "klama", "mi", "le zarci")

        # test case - changing place by FA and filling subsequent places
        sparse = semantic_parse_text("mi klama fi la .atlantas. le dargu fe la bastn. le karce")
        compare_places(sparse, "klama", "mi", "la bastn", "la atlantas", "le dargu", "le karce")

        # test case muliple sumti before selbri
        sparse = semantic_parse_text("mi ti vecnu ta")
        compare_places(sparse, "vecnu", "mi", "ti", "ta")

        # test cases for SE
        sparse = semantic_parse_text("do se tavla mi ti")
        compare_places(sparse, "tavla", "mi", "do", "ti")

        sparse = semantic_parse_text("ti te tavla do mi")
        compare_places(sparse, "tavla", "mi", "do", "ti")

        # test cases for tanru
        sparse = semantic_parse_text("mi sutra klama la meris.")
        compare_places(sparse, "sutra klama", "mi", "la meris")

        # test cases for tanru with SE
        sparse = semantic_parse_text("mi sutra se klama la meris.")
        print sparse



if __name__ == '__main__':
    unittest.main()
