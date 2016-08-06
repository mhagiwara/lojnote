"""Access methods for Lojban dependency corpus."""

import re
from lsp import WordWithDependency


def read(io):
    """Read from a dependency corpus.

    Parameters:
        io: The IO object that we are reading the file from (stdin, file, etc.)

    Yields:
        sentences, where a sentence is a list of WordWithDependency.
    """
    current_sent = []
    for line in io:
        line = line.strip()
        if line.startswith('#'):
            # comment line
            continue

        if not line:
            # sentence separator
            if current_sent:
                yield current_sent
            current_sent = []
        else:
            # valid line with a word
            fields = re.split(r'\s+', line)
            word = WordWithDependency(child_idx=int(fields[0]), child_suf=fields[1],
                                      head_idx=int(fields[2]), arc_type=fields[3:])
            current_sent.append(word)
    if current_sent:
        yield current_sent


def write(io):
    """Write to a dependency corpus."""
    pass


if __name__ == '__main__':
    import sys
    for sent in read(sys.stdin):
        print sent
