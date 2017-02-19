"""Access methods for Lojban dependency corpus.
When run independently, this converts TSV-style dependency corpus into
CoNLL-X style format."""

from ldp import camxes
from itertools import izip


def parse_sent_str(sent_lines):
    """Given a list of lines for Lojban dependency corpus, convert them into a tuple of:
        words: list of words
        tags: list of POS tags
        heads: list of head indices
        rels: list of dependency labels

    This method also runs camxes to obtain correct POS tags (selma'o).
    """
    words = []
    tags = []
    heads = []
    rels = []
    for line in sent_lines:
        fields = line.split()
        assert len(fields) == 4
        _, word, head, deprel = fields
        words.append(word)
        heads.append(head)
        rels.append(deprel)

    sent = ' '.join(words)
    tagged_words = list(camxes.tag(sent))
    assert len(tagged_words) == len(words)
    tags = [tag for _, tag in tagged_words]

    return words, tags, heads, rels


def read(io):
    """Read from a dependency corpus.

    Parameters:
        io: The IO object that we are reading the file from (stdin, file, etc.)

    Yields:
        Tuples (words, tags, heads, rels) where:
            words: list of words
            tags: list of POS tags
            heads: list of head indices
            rels: list of dependency labels
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


def sent2conllx(sent):
    """Given a sentence tuple, yield lines of CoNLL-X format."""
    words, tags, heads, rels = sent
    for i, (word, tag, head, rel) in enumerate(izip(words, tags, heads, rels)):
        yield '%d\t%s\t_\t%s\t%s\t_\t%s\t%s\t_\t_' % (i+1, word, tag, tag, head, rel)


def main():
    import sys
    for sent in read(sys.stdin):
        for line in sent2conllx(sent):
            print line
        print


if __name__ == '__main__':
    main()
