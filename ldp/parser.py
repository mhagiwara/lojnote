from pkg_resources import resource_filename
from subprocess import Popen, PIPE
from ldp.corpus_reader import read_conllx_corpus

_jarfile = resource_filename(__name__, 'maltparser/maltparser-1.9.0.jar')


def parse(text):
    """Run maltparser on text, and yield the parse result.

    Parameters:
        text: text (string) to parse.
    Yields:
        Sentences, where a sentence is a list of CONLLXToken.
    """
    args = ['-w', 'ldp', '-c', 'ldp-malt', '-i', 'ldp/test.conllx', '-m', 'parse']
    malt_process = Popen(['java', '-jar', _jarfile] + args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    for sent in read_conllx_corpus(malt_process.stdout):
        yield sent


def main():
    for sent in parse(""):
        print sent


if __name__ == '__main__':
    main()
