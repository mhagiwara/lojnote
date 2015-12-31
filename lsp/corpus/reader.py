"""Access methods for Lojban dependency corpus."""

import re
from collections import namedtuple

# Type definition for a single word in a dependency tree.
# child_idx: 0-base sentence-internal index of child (the current word)
# child_suf: the surface string of child
# head_idx : index of head (the word this child depends on)
# arc_tyep:  type of dependency - list of string, e.g., ['PLACE', '1'], ['QUANTIFIER'], etc.
WordWithDependency = namedtuple('WordWithDependency',
                                ['child_idx', 'child_suf', 'head_idx', 'arc_type'])


def read(io):
    """Read from a dependency corpus.

    Parameters:
        io: The IO object that we are reading the file from (stdin, file, etc.)

    Returns:
        list of sentences, where a sentence is a list of WordWithDependency."""
    current_sent = []
    sentences = []
    for line in io:
        line = line.strip()
        if not line:
            # sentence separator
            if current_sent:
                sentences.append(current_sent)
            current_sent = []
        else:
            # valid line with a word
            fields = re.split(r'\s+', line)
            word = WordWithDependency(child_idx=int(fields[0]), child_suf=fields[1],
                                      head_idx=int(fields[2]), arc_type=fields[3:])
            current_sent.append(word)
    if current_sent:
        sentences.append(current_sent)

    return sentences


def write(io):
    """Write to a dependency corpus."""
    pass


if __name__ == '__main__':
    import sys
    corpus = read(sys.stdin)
    print corpus
