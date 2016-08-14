import unittest
from ldp import camxes, DependencyArc
from ldp.parser import decode, get_oracle_transition_func


class TestLojbanDependencyParser(unittest.TestCase):

    def test_camxes(self):
        self.assertEquals([('KOhA', 'mi'), ('gismu', 'klama'), ('LE', 'le'), ('gismu', 'zarci')],
                          list(camxes.tag('mi klama le zarci')))

    def test_parser(self):
        tagged_words = camxes.tag('mi klama le zarci')
        arcs = {
            DependencyArc(child=0, parent=1, label='PLACE_1'),
            DependencyArc(child=1, parent=-1, label='MAIN_BRIDI'),
            DependencyArc(child=2, parent=3, label='DESCRIPTOR'),
            DependencyArc(child=3, parent=1, label='PLACE_2')
        }

        next_transition = get_oracle_transition_func(arcs)
        print decode(sent, next_transition)

if __name__ == '__main__':
    unittest.main()
