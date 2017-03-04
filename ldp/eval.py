from ldp.corpus_reader import read_conllx_corpus
from collections import Counter


def evaluate_sent(ans_sent, sys_sent):
    """Compare the dependency head and relation labels between ans_sent and sys_sent,
    returns a dictionary containing evaluation statistics."""
    assert len(ans_sent) == len(sys_sent)
    assert len(ans_sent) > 0

    unlabeled_matches = 0
    labeled_matches = 0
    for ans_token, sys_token in zip(ans_sent, sys_sent):
        if ans_token.head == sys_token.head:
            unlabeled_matches += 1
            if ans_token.deprel == sys_token.deprel:
                labeled_matches += 1

    return {
        'num_tokens': len(ans_sent),
        'unlabeled_matches': unlabeled_matches,
        'labeled_matches': labeled_matches
    }


def evaluate(ans_corpus, sys_corpus):
    assert len(ans_corpus) == len(sys_corpus)
    assert len(ans_corpus) > 0

    stats_sum = Counter()
    for ans_sent, sys_sent in zip(ans_corpus, sys_corpus):
        stats = evaluate_sent(ans_sent, sys_sent)
        stats_sum.update(stats)

    assert stats_sum['num_tokens'] > 0
    las = 1. * stats_sum['labeled_matches'] / stats_sum['num_tokens']
    uas = 1. * stats_sum['unlabeled_matches'] / stats_sum['num_tokens']

    # Sanity check - this should always hold
    assert las <= uas

    return {
        'LAS': las,
        'UAS': uas
    }


def main(ans_filename, sys_filename):
    ans_corpus = list(read_conllx_corpus(open(ans_filename)))
    sys_corpus = list(read_conllx_corpus(open(sys_filename)))
    print evaluate(ans_corpus, sys_corpus)


if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
