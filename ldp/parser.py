
from ldp import DependencyArc


def decode(sent, next_transition):
    """Decode a sentence and returns a list of WordWithDependency.

    Parameters:
        sent: list of (selma'o, word) pairs.
        next_transition: a callable which, given the word indices of head and next element of stack,
                and set of arcs obtained so far, returns the next action (action, label), where
                action is one of {'shift', 'left-arc', 'right-arc'}.

    Returns:
        dep_sent: list of WordWithDependency.
    """
    queue = list(enumerate(sent))
    stack = []

    def _shift(queue, stack):
        print 'shift'
        i, _ = queue.pop(0)
        stack.append((i, set()))

    def _left_arc(_, stack, label):
        print 'left-arc'
        j, arcs_j = stack.pop()
        i, arcs_i = stack.pop()
        new_arcs = arcs_i | arcs_j | {DependencyArc(child=i, parent=j, label=label)}
        stack.append((j, new_arcs))

    def _right_arc(_, stack, label):
        print 'right-arc'
        j, arcs_j = stack.pop()
        i, arcs_i = stack.pop()
        new_arcs = arcs_i | arcs_j | {DependencyArc(child=j, parent=i, label=label)}
        stack.append((i, new_arcs))

    while queue or len(stack) != 1:
        print 'state: stack %s, queue %s' % (stack, queue)
        if len(stack) < 2:
            _shift(queue, stack)
        else:
            action, label = next_transition(stack[-1][0], stack[-2][0])
            if action == 'left-arc':
                _left_arc(queue, stack, label)
            elif action == 'right-arc':
                _right_arc(queue, stack, label)
            else:
                _shift(queue, stack)

    _, arcs = stack.pop()
    return arcs


def get_oracle_transition_func(arcs):
    """Given a set of dependency arcs,
    returns a function that returns the next oracle transition based on the current state."""

    idx_pair_to_labels = {}
    for arc in arcs:
        idx_pair_to_labels[(arc.parent, arc.child)] = arc.label

    def _get_oracle_transition(top_idx, next_idx):
        left_arc_label = idx_pair_to_labels.get((top_idx, next_idx))
        if left_arc_label:
            return ('left-arc', left_arc_label)
        else:
            right_arc_label = idx_pair_to_labels.get((next_idx, top_idx))
            if right_arc_label:
                return ('right-arc', right_arc_label)
            else:
                return ('shift', None)

    return _get_oracle_transition
