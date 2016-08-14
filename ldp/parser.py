"""A simple implementation of a greedy transition-based parser. Released under BSD license.
The majority of code here is taken from https://spacy.io/blog/parsing-english-in-python
"""
from os import path
import os
import sys
from collections import defaultdict
import random
import time
import pickle

from ldp import DefaultList, pad_tokens
from ldp.corpus.reader import read
from ldp import camxes

SHIFT = 0
RIGHT = 1
LEFT = 2
MOVES = (SHIFT, RIGHT, LEFT)
START = ['-START-', '-START2-']
END = ['-END-', '-END2-']


class Parse(object):
    def __init__(self, n):
        self.n = n
        self.heads = [None] * (n-1)
        self.labels = [None] * (n-1)
        self.lefts = []
        self.rights = []
        for _ in xrange(n + 1):
            self.lefts.append(DefaultList(0))
            self.rights.append(DefaultList(0))

    def add(self, head, child, label=None):
        self.heads[child] = head
        self.labels[child] = label
        if child < head:
            self.lefts[head].append(child)
        else:
            self.rights[head].append(child)


class Parser(object):
    def __init__(self):
        self.model = Perceptron(MOVES)

    def parse(self, words, tags):
        n = len(words)
        i = 2
        stack = [1]
        parse = Parse(n)
        while stack or (i+1) < n:
            features = extract_features(words, tags, i, n, stack, parse)
            scores = self.model.score(features)
            valid_moves = get_valid_moves(i, n, len(stack))
            guess = max(valid_moves, key=lambda move: scores[move])
            i = transition(guess, i, stack, parse)
        return tags, parse.heads

    def train_one(self, words, tags, gold_heads):
        n = len(words)
        i = 2
        stack = [1]
        parse = Parse(n)
        while stack or (i + 1) < n:
            features = extract_features(words, tags, i, n, stack, parse)
            scores = self.model.score(features)
            valid_moves = get_valid_moves(i, n, len(stack))
            gold_moves = get_gold_moves(i, n, stack, parse.heads, gold_heads)
            guess = max(valid_moves, key=lambda move: scores[move])
            assert gold_moves
            best = max(gold_moves, key=lambda move: scores[move])
            self.model.update(best, guess, features)
            i = transition(guess, i, stack, parse)
        return len([i for i in xrange(n-1) if parse.heads[i] == gold_heads[i]])


def transition(move, i, stack, parse):
    if move == SHIFT:
        stack.append(i)
        return i + 1
    elif move == RIGHT:
        parse.add(stack[-2], stack.pop())
        return i
    elif move == LEFT:
        parse.add(i, stack.pop())
        return i
    assert move in MOVES


def get_valid_moves(i, n, stack_depth):
    moves = []
    if (i+1) < n:
        moves.append(SHIFT)
    if stack_depth >= 2:
        moves.append(RIGHT)
    if stack_depth >= 1:
        moves.append(LEFT)
    return moves


def get_gold_moves(n0, n, stack, heads, gold):
    def deps_between(target, others, gold):
        for word in others:
            if gold[word] == target or gold[target] == word:
                return True
        return False

    valid = get_valid_moves(n0, n, len(stack))
    if not stack or (SHIFT in valid and gold[n0] == stack[-1]):
        return [SHIFT]
    if gold[stack[-1]] == n0:
        return [LEFT]
    costly = set([m for m in MOVES if m not in valid])
    # If the word behind s0 is its gold head, Left is incorrect
    if len(stack) >= 2 and gold[stack[-1]] == stack[-2]:
        costly.add(LEFT)
    # If there are any dependencies between n0 and the stack,
    # pushing n0 will lose them.
    if SHIFT not in costly and deps_between(n0, stack, gold):
        costly.add(SHIFT)
    # If there are any dependencies between s0 and the buffer, popping
    # s0 will lose them.
    if deps_between(stack[-1], range(n0+1, n-1), gold):
        costly.add(LEFT)
        costly.add(RIGHT)
    return [m for m in MOVES if m not in costly]


def extract_features(words, tags, n0, n, stack, parse):
    def get_stack_context(depth, stack, data):
        if depth >= 3:
            return data[stack[-1]], data[stack[-2]], data[stack[-3]]
        elif depth >= 2:
            return data[stack[-1]], data[stack[-2]], ''
        elif depth == 1:
            return data[stack[-1]], '', ''
        else:
            return '', '', ''

    def get_buffer_context(i, n, data):
        if i + 1 >= n:
            return data[i], '', ''
        elif i + 2 >= n:
            return data[i], data[i + 1], ''
        else:
            return data[i], data[i + 1], data[i + 2]

    def get_parse_context(word, deps, data):
        if word == -1:
            return 0, '', ''
        deps = deps[word]
        valency = len(deps)
        if not valency:
            return 0, '', ''
        elif valency == 1:
            return 1, data[deps[-1]], ''
        else:
            return valency, data[deps[-1]], data[deps[-2]]

    features = {}
    # Set up the context pieces --- the word (W) and tag (T) of:
    # S0-2: Top three words on the stack
    # N0-2: First three words of the buffer
    # n0b1, n0b2: Two leftmost children of the first word of the buffer
    # s0b1, s0b2: Two leftmost children of the top word of the stack
    # s0f1, s0f2: Two rightmost children of the top word of the stack

    depth = len(stack)
    s0 = stack[-1] if depth else -1

    Ws0, Ws1, Ws2 = get_stack_context(depth, stack, words)
    Ts0, Ts1, Ts2 = get_stack_context(depth, stack, tags)

    Wn0, Wn1, Wn2 = get_buffer_context(n0, n, words)
    Tn0, Tn1, Tn2 = get_buffer_context(n0, n, tags)

    Vn0b, Wn0b1, Wn0b2 = get_parse_context(n0, parse.lefts, words)
    Vn0b, Tn0b1, Tn0b2 = get_parse_context(n0, parse.lefts, tags)

    Vn0f, Wn0f1, Wn0f2 = get_parse_context(n0, parse.rights, words)
    _, Tn0f1, Tn0f2 = get_parse_context(n0, parse.rights, tags)

    Vs0b, Ws0b1, Ws0b2 = get_parse_context(s0, parse.lefts, words)
    _, Ts0b1, Ts0b2 = get_parse_context(s0, parse.lefts, tags)

    Vs0f, Ws0f1, Ws0f2 = get_parse_context(s0, parse.rights, words)
    _, Ts0f1, Ts0f2 = get_parse_context(s0, parse.rights, tags)

    # Cap numeric features at 5?
    # String-distance
    Ds0n0 = min((n0 - s0, 5)) if s0 != 0 else 0

    features['bias'] = 1
    # Add word and tag unigrams
    for w in (Wn0, Wn1, Wn2, Ws0, Ws1, Ws2, Wn0b1, Wn0b2, Ws0b1, Ws0b2, Ws0f1, Ws0f2):
        if w:
            features['w=%s' % w] = 1
    for t in (Tn0, Tn1, Tn2, Ts0, Ts1, Ts2, Tn0b1, Tn0b2, Ts0b1, Ts0b2, Ts0f1, Ts0f2):
        if t:
            features['t=%s' % t] = 1

    # Add word/tag pairs
    for i, (w, t) in enumerate(((Wn0, Tn0), (Wn1, Tn1), (Wn2, Tn2), (Ws0, Ts0))):
        if w or t:
            features['%d w=%s, t=%s' % (i, w, t)] = 1

    # Add some bigrams
    features['s0w=%s,  n0w=%s' % (Ws0, Wn0)] = 1
    features['wn0tn0-ws0 %s/%s %s' % (Wn0, Tn0, Ws0)] = 1
    features['wn0tn0-ts0 %s/%s %s' % (Wn0, Tn0, Ts0)] = 1
    features['ws0ts0-wn0 %s/%s %s' % (Ws0, Ts0, Wn0)] = 1
    features['ws0-ts0 tn0 %s/%s %s' % (Ws0, Ts0, Tn0)] = 1
    features['wt-wt %s/%s %s/%s' % (Ws0, Ts0, Wn0, Tn0)] = 1
    features['tt s0=%s n0=%s' % (Ts0, Tn0)] = 1
    features['tt n0=%s n1=%s' % (Tn0, Tn1)] = 1

    # Add some tag trigrams
    trigrams = ((Tn0, Tn1, Tn2), (Ts0, Tn0, Tn1), (Ts0, Ts1, Tn0),
                (Ts0, Ts0f1, Tn0), (Ts0, Ts0f1, Tn0), (Ts0, Tn0, Tn0b1),
                (Ts0, Ts0b1, Ts0b2), (Ts0, Ts0f1, Ts0f2), (Tn0, Tn0b1, Tn0b2),
                (Ts0, Ts1, Ts1))
    for i, (t1, t2, t3) in enumerate(trigrams):
        if t1 or t2 or t3:
            features['ttt-%d %s %s %s' % (i, t1, t2, t3)] = 1

    # Add some valency and distance features
    vw = ((Ws0, Vs0f), (Ws0, Vs0b), (Wn0, Vn0b))
    vt = ((Ts0, Vs0f), (Ts0, Vs0b), (Tn0, Vn0b))
    d = ((Ws0, Ds0n0), (Wn0, Ds0n0), (Ts0, Ds0n0), (Tn0, Ds0n0),
         ('t' + Tn0+Ts0, Ds0n0), ('w' + Wn0+Ws0, Ds0n0))
    for i, (w_t, v_d) in enumerate(vw + vt + d):
        if w_t or v_d:
            features['val/d-%d %s %d' % (i, w_t, v_d)] = 1
    return features


class Perceptron(object):
    def __init__(self, classes=None):
        # Each feature gets its own weight vector, so weights is a dict-of-arrays
        self.classes = classes
        self.weights = {}
        # The accumulated values, for the averaging. These will be keyed by
        # feature/clas tuples
        self._totals = defaultdict(int)
        # The last time the feature was changed, for the averaging. Also
        # keyed by feature/clas tuples
        # (tstamps is short for timestamps)
        self._tstamps = defaultdict(int)
        # Number of instances seen
        self.i = 0

    def predict(self, features):
        '''Dot-product the features and current weights and return the best class.'''
        scores = self.score(features)
        # Do a secondary alphabetic sort, for stability
        return max(self.classes, key=lambda clas: (scores[clas], clas))

    def score(self, features):
        all_weights = self.weights
        scores = dict((clas, 0) for clas in self.classes)
        for feat, value in features.items():
            if value == 0:
                continue
            if feat not in all_weights:
                continue
            weights = all_weights[feat]
            for clas, weight in weights.items():
                scores[clas] += value * weight
        return scores

    def update(self, truth, guess, features):
        def upd_feat(c, f, w, v):
            param = (f, c)
            self._totals[param] += (self.i - self._tstamps[param]) * w
            self._tstamps[param] = self.i
            self.weights[f][c] = w + v

        self.i += 1
        if truth == guess:
            return None
        for f in features:
            weights = self.weights.setdefault(f, {})
            upd_feat(truth, f, weights.get(truth, 0.0), 1.0)
            upd_feat(guess, f, weights.get(guess, 0.0), -1.0)

    def average_weights(self):
        for feat, weights in self.weights.items():
            new_feat_weights = {}
            for clas, weight in weights.items():
                param = (feat, clas)
                total = self._totals[param]
                total += (self.i - self._tstamps[param]) * weight
                averaged = round(total / float(self.i), 3)
                if averaged:
                    new_feat_weights[clas] = averaged
            self.weights[feat] = new_feat_weights

    def save(self, path):
        print "Saving model to %s" % path
        pickle.dump(self.weights, open(path, 'w'))

    def load(self, path):
        self.weights = pickle.load(open(path))


def train(train_io, model_file):
    nr_iter = 15
    parser = Parser()
    sentences = list(read(train_io))

    for itn in xrange(nr_iter):
        corr = 0
        total = 0
        random.shuffle(sentences)
        for words, tags, gold_parse, gold_label in sentences:
            corr += parser.train_one(words, tags, gold_parse)
            total += len(words)
        print itn, '%.3f' % (float(corr) / float(total))
    print 'Averaging weights'
    parser.model.average_weights()
    parser.model.save(model_file)


def test(sentences_io, model_file):

    parser = Parser()
    parser.model.load(model_file)
    for sentence in sentences_io:
        tagged_words = list(camxes.tag(sentence))
        words = [word for word, _ in tagged_words]
        tags = [tag for _, tag in tagged_words]
        pad_tokens(words)
        pad_tokens(tags)
        print tagged_words
        print parser.parse(words, tags)


if __name__ == '__main__':
    if sys.argv[1] == 'train':
        train(open(sys.argv[2]), sys.argv[3])

    elif sys.argv[1] == 'test':
        test(sys.stdin, sys.argv[2])
