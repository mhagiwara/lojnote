import sys
import tempfile

from pkg_resources import resource_filename
from subprocess import Popen, PIPE
from ldp import camxes
from ldp.corpus_reader import DepToken, read_conllx_corpus, sent2conllx

_jarfile = resource_filename(__name__, 'maltparser/maltparser-1.9.0.jar')


def text2conll(text):
    """Given a raw text, run camxes, tag words, and yield lines of CoNLL-X format corpus."""
    tagged_words = camxes.tag(text)
    sent = []
    for word, tag in tagged_words:
        token = DepToken(word=word, tag=tag, head=0, deprel='-')
        sent.append(token)

    return sent2conllx(sent)


def parse(text):
    """Run maltparser on text, and yield the parse result.

    Parameters:
        text: text (string) to parse.
    Yields:
        Sentences, where a sentence is a list of CONLLXToken.
    """
    if not text:
        return

    # Set up a temporary file, and write CoNLL-X format as an input corpus.
    temp = tempfile.NamedTemporaryFile()
    for line in text2conll(text):
        temp.write(line)
        temp.write('\n')
    temp.write('\n')
    temp.flush()

    # Run MaltParser
    args = ['-w', 'ldp/data', '-c', 'ldp-malt', '-i', temp.name, '-m', 'parse']
    malt_process = Popen(['java', '-jar', _jarfile] + args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    malt_process.stderr.read()

    # Close the temporary file (which deletes it) as soon as the process finishes running.
    temp.close()

    for sent in read_conllx_corpus(malt_process.stdout):
        yield sent


def main():
    for sent in parse("mi klama le zarci"):
        print sent


if __name__ == '__main__':
    main()
