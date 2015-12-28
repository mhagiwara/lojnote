import re
import simplejson as json
from pkg_resources import resource_filename
from subprocess import Popen, PIPE
import ast

_jarfile = resource_filename(__name__, 'camxes.jar')

_process_pool = {}

def get_process(arg):
    """Get the camxes.jar process (create a new one in the pool if necessary)"""
    if (arg not in _process_pool or
        _process_pool[arg].poll() is not None):

        _process_pool[arg] = Popen(['java', '-jar', _jarfile, arg],
                                   stdout=PIPE, stdin=PIPE)
        num_args = len(arg) - 1    # number of arguments given (minus the first '-')
        for _ in xrange(num_args):
            # Consume camxes.jar's initial header lines (as many as there are options)
            _process_pool[arg].stdout.readline()

    return _process_pool[arg]


def get_result(arg, text):
    """Run the camxex.jar process, feed the input text, and get the raw output."""
    proc = get_process(arg)
    proc.stdin.write(text.encode('utf-8'))
    proc.stdin.write(b'\n')
    proc.stdin.flush()
    output = proc.stdout.readline()
    return output.decode('utf-8').rstrip('\n')


def parse(text):
    """Given raw Lojban text, parse it and return the parse tree."""
    raw_output = get_result('-e', text)
    raw_output = re.sub(r'(\w+)\(', '"\\1", [', raw_output)
    raw_output = raw_output.replace(')', ']')
    print raw_output
    return ast.literal_eval('[' + raw_output.strip() + ']')


def normalize_parse(subtree):
    """Recursively normalize camxes.jar's output to [label, child1, child2, ...] form."""
    if type(subtree) == list and len(subtree) == 1:
        # terminal nodes
        return subtree
    if type(subtree) == list and len(subtree) == 2:
        children = normalize_parse(subtree[1])
        if type(children[0]) == str:
            return [subtree[0], children]
        else:
            return [subtree[0]] + children

    # Otherwise, the subtree is always in the
    # [child1-label, child1-subtree, child2-label, child2-subtree, ...] form.
    assert len(subtree) % 2 == 0
    normalized_children = []
    num_children = len(subtree) / 2
    for i in xrange(num_children):
        grandchildren = normalize_parse(subtree[i * 2 + 1])
        if type(grandchildren[0]) == str:
            normalized_children.append([subtree[i * 2], grandchildren])
        else:
            normalized_children.append([subtree[i * 2]] + grandchildren)

    return normalized_children
