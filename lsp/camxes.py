import re
from pkg_resources import resource_filename
from subprocess import Popen, PIPE
import ast

_jarfile = resource_filename(__name__, 'camxes.jar')

_process_pool = {}


class TreeNode(object):
    def __init__(self, children=None, parent=None, label=None, terminal=False):
        """Initialize a TreeNode.

        Parameters:
            children: list of children (TreeNode)
            parent: parent TreeNode if exists, None otherwise (i.e., root nde)
            label: String label of this node - nonterminal name (e.g., 'sentence') or
                terminal word (e.g., 'coi')
            terminal: True if this node is terminal (has no children)
        """
        self.children = children or []
        self.parent = parent
        self.label = label
        self.terminal = terminal

    @classmethod
    def create_from_array(cls, subtree):
        """Create a TreeNode instance from an array representation."""
        assert isinstance(subtree, list)
        if len(subtree) == 1:
            # terminal nodes (no children)
            return TreeNode(children=[], label=subtree[0], terminal=True)
        else:
            assert len(subtree) >= 2
            children = [cls.create_from_array(child_array)
                        for child_array in subtree[1:]]
            node = TreeNode(children=children, label=subtree[0], terminal=False)
            for child in children:
                child.parent = node

            return node

    def to_string(self, margin=80, indent=0):
        """Returns an S-expression like recursive string representation of this TreeNode."""
        s = ' ' * indent
        if self.terminal:
            return s + self.label
        else:
            children_reprs = [child.to_string(margin=margin, indent=indent+2)
                              for child in self.children]
            s += '(%s\n%s)' % (self.label, '\n'.join(children_reprs))
            s_flat = re.sub(r'\n +', ' ', s)
            if len(s_flat) < margin:
                # If the entire representation fits within a line, return a flat representation.
                return s_flat
            else:
                # Otherwise, return a multi-line representation.
                return s

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


def get_camxes_process(arg):
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


def run_camxes(arg, text):
    """Run the camxex.jar process, feed the input text, and get the raw output."""
    proc = get_camxes_process(arg)
    proc.stdin.write(text.encode('utf-8'))
    proc.stdin.write(b'\n')
    proc.stdin.flush()
    output = proc.stdout.readline()
    return output.decode('utf-8').rstrip('\n')


def normalize_array_tree(subtree):
    """Recursively normalize camxes's array representation to [label, child1, child2, ...] form."""
    if isinstance(subtree, list) and len(subtree) == 1:
        # terminal nodes
        return subtree
    if isinstance(subtree, list) and len(subtree) == 2:
        children = normalize_array_tree(subtree[1])
        if isinstance(children[0], str):
            return [subtree[0], children]
        else:
            return [subtree[0]] + children

    # Otherwise, the subtree is always in the
    # [child1-label, child1-subtree, child2-label, child2-subtree, ...] form.
    assert len(subtree) % 2 == 0
    normalized_children = []
    num_children = len(subtree) / 2
    for i in xrange(num_children):
        grandchildren = normalize_array_tree(subtree[i * 2 + 1])
        if isinstance(grandchildren[0], str):
            normalized_children.append([subtree[i * 2], grandchildren])
        else:
            normalized_children.append([subtree[i * 2]] + grandchildren)

    return normalized_children


def parse(text):
    """Given raw Lojban text, parse it and return the parse tree in the array representation."""
    raw_output = run_camxes('-e', text)
    raw_output = re.sub(r'(\w+)\(', '"\\1", [', raw_output)
    raw_output = raw_output.replace(')', ']')
    tree_array = ast.literal_eval('[' + raw_output.strip() + ']')
    tree_array_normed = normalize_array_tree(tree_array)
    return TreeNode.create_from_array(tree_array_normed)
