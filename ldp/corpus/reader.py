"""Access methods for Lojban dependency corpus."""

from ldp import DefaultList, pad_tokens
from ldp import camxes


def parse_sent_str(sent_lines):
    words = DefaultList('')
    tags = DefaultList('')
    heads = [None]
    labels = [None]
    for line in sent_lines:
        fields = line.split()
        word, head = fields[1], fields[2]
        label = '' if len(fields) < 4 else fields[3]
        words.append(intern(word))
        heads.append(int(head) + 1 if head != '-1' else len(sent_lines) + 1)
        labels.append(label)

    sent = ' '.join(words)
    tagged_words = list(camxes.tag(sent))
    assert len(tagged_words) == len(words)
    tags = [tag for _, tag in tagged_words]

    pad_tokens(words)
    pad_tokens(tags)
    return words, tags, heads, labels


def read(io):
    """Read from a dependency corpus.

    Parameters:
        io: The IO object that we are reading the file from (stdin, file, etc.)

    Yields:
        Pairs (words, arcs) where:
            words: list of words
            arcs: set of DependencyArcs
    """
    sent_lines = []
    for line in io:
        line = line.strip()
        if line.startswith('#'):
            # comment line
            continue

        if not line:
            # sentence separator
            if sent_lines:
                yield parse_sent_str(sent_lines)
            sent_lines = []
        else:
            sent_lines.append(line)
    if sent_lines:
        yield parse_sent_str(sent_lines)


if __name__ == '__main__':
    import sys
    for sent in read(sys.stdin):
        print sent
