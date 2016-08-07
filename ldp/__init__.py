
from collections import namedtuple

# Type definition for a single word in a dependency tree.
# Fields:
#   child: 0-base sentence-internal index of child (the current word)
#   parent : index of parent (the word this child depends on)
#   label:  label of dependency arc - e.g., 'PLACE1', 'DESCRIPTOR', etc.
DependencyArc = namedtuple('DependencyArc',
                           ['child', 'parent', 'label'])
