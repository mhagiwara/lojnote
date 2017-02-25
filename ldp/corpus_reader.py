"""Access methods for Lojban dependency corpus.
When run independently, this converts TSV-style dependency corpus into
CoNLL-X style format."""

from ldp import camxes
from itertools import izip
from collections import namedtuple

DepToken = namedtuple('DepToken', ['word', 'tag', 'head', 'deprel'])
CONLLXToken = namedtuple('CONLLXToken', ['form', 'lemma', 'cpostag', 'postag', 'feats',
                                         'head', 'deprel', 'phead', 'pdeprel'])


def parse_dep_sent(sent_lines):
    """Given a list of lines for Lojban dependency corpus, convert them into a list of DepTokens.
    This method also runs camxes to obtain correct POS tags (selma'o).
    """

    words = []
    heads = []
    deprels = []
    for line in sent_lines:
        fields = line.split()
        assert len(fields) == 4
        _, word, head, deprel = fields
        words.append(word)
        heads.append(int(head))
        deprels.append(deprel)

    sent = ' '.join(words)
    tagged_words = list(camxes.tag(sent))
    assert len(tagged_words) == len(words)

    tokens = []
    for word, (_, tag), head, deprel in izip(words, tagged_words, heads, deprels):
        token = DepToken(word=word, tag=tag, head=head, deprel=deprel)
        tokens.append(token)

    return tokens


def parse_conllx_sent(sent_lines):
    """Given a list of lines from a CoNLL-X format corpus, convert them into a list of CONLLXTokens.
    """
    tokens = []
    for line in sent_lines:
        fields = line.split()
        assert len(fields) == 10
        _, form, lemma, cpostag, postag, feats, head, deprel, phead, pdeprel = fields
        token = CONLLXToken(form=form, lemma=lemma, cpostag=cpostag, postag=postag, feats=feats,
                            head=int(head), deprel=deprel, phead=phead, pdeprel=pdeprel)
        tokens.append(token)

    return tokens


def read_corpus(io, parse_sent_func):
    """Read from a dependency/CoNLL-X corpus.

    Parameters:
        io: The IO object that we are reading the file from (stdin, file, etc.)
        parse_sent_func: method that, given a list of sentence lines, returns a sentence object.

    Yields:
        Sentences, where one sentence is the return value of parse_sent_func.
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
                yield parse_sent_func(sent_lines)
            sent_lines = []
        else:
            sent_lines.append(line)
    if sent_lines:
        yield parse_sent_func(sent_lines)


def read_dep_corpus(io):
    for sent in read_corpus(io, parse_dep_sent):
        yield sent


def read_conllx_corpus(io):
    for sent in read_corpus(io, parse_conllx_sent):
        yield sent


def sent2conllx(sent):
    """Given a sentence tuple, yield lines of CoNLL-X format."""
    for i, token in enumerate(sent):
        token_tuple = (i+1, token.word, token.tag, token.tag, token.head, token.deprel)
        yield '%d\t%s\t_\t%s\t%s\t_\t%s\t%s\t_\t_' % token_tuple


def main():
    import sys
    for sent in read_dep_corpus(sys.stdin):
        for line in sent2conllx(sent):
            print line
        print


if __name__ == '__main__':
    main()
