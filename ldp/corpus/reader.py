"""Access methods for Lojban dependency corpus."""

import re
from ldp import DependencyArc


def read(io):
    """Read from a dependency corpus.

    Parameters:
        io: The IO object that we are reading the file from (stdin, file, etc.)

    Yields:
        Pairs (words, arcs) where:
            words: list of words
            arcs: set of DependencyArcs
    """
    words = []
    arcs = set()
    for line in io:
        line = line.strip()
        if line.startswith('#'):
            # comment line
            continue

        if not line:
            # sentence separator
            if words:
                yield (words, arcs)
            words = []
            arcs = set()
        else:
            # valid line with a word
            fields = re.split(r'\s+', line)
            arc = DependencyArc(child=int(fields[0]), parent=int(fields[2]),
                                label=fields[3] if len(fields) == 4 else '*')
            words.append(fields[1])
            arcs.add(arc)

    if words:
        yield (words, arcs)


def write(io):
    """Write to a dependency corpus."""
    pass


if __name__ == '__main__':
    import sys
    for sent in read(sys.stdin):
        print sent
