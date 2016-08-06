
from collections import namedtuple
# Type definition for a single word in a dependency tree.
# child_idx: 0-base sentence-internal index of child (the current word)
# child_suf: the surface string of child
# head_idx : index of head (the word this child depends on)
# arc_tyep:  type of dependency - list of string, e.g., ['PLACE', '1'], ['QUANTIFIER'], etc.
WordWithDependency = namedtuple('WordWithDependency',
                                ['child_idx', 'child_suf', 'head_idx', 'arc_type'])
