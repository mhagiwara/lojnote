import unittest
from ldp import camxes


class TestLojbanDependencyParser(unittest.TestCase):

    def test_camxes(self):
        self.assertEquals([('KOhA', 'mi'), ('gismu', 'klama'), ('LE', 'le'), ('gismu', 'zarci')],
                          list(camxes.tag('mi klama le zarci')))


if __name__ == '__main__':
    unittest.main()
