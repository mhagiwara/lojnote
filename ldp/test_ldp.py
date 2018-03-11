from ldp import camxes
from ldp import depparser
from ldp.corpus_reader import (DepToken, parse_dep_sent, read_dep_corpus,
                               CONLLXToken, parse_conllx_sent, read_conllx_corpus)
from ldp.eval import evaluate_sent, evaluate


def test_camxes():
    tagged_words = list(camxes.tag(""))
    assert tagged_words == []

    tagged_words = list(camxes.tag("ko'a broda"))
    assert tagged_words == [("ko'a", 'KOhA'), ('broda', 'gismu')]


def test_dep_corpus_reader():
    sent = parse_dep_sent(['1\tmi\t2\tP1', '2\tklama\t0\tROOT'])

    assert len(sent) == 2
    assert sent[0] == DepToken('mi', 'KOhA', 2, 'P1')
    assert sent[1] == DepToken('klama', 'gismu', 0, 'ROOT')

    lines = ["1	mi	2	P1",
             "2	klama	0	ROOT",
             "",
             "1	ko'a	2	P1",
             "2	broda	0	ROOT"]

    sents = list(read_dep_corpus(lines))
    assert len(sents) == 2
    assert len(sents[0]) == 2
    assert len(sents[1]) == 2
    assert sents[1][0] == DepToken("ko'a", 'KOhA', 2, 'P1')
    assert sents[1][1] == DepToken('broda', 'gismu', 0, 'ROOT')


def test_conllx_corpus_reader():
    sent_str = "1	mi	_	KOhA	KOhA	_	2	P1	_	_"
    sent = parse_conllx_sent([sent_str])
    assert len(sent) == 1
    token = CONLLXToken(form='mi', lemma='_', cpostag='KOhA', postag='KOhA', feats='_',
                        head=2, deprel='P1', phead='_', pdeprel='_')
    assert sent[0] == token

    lines = ["1	broda	_	gismu	gismu	_	0	ROOT	_	_",
             "",
             "1	brode	_	gismu	gismu	_	0	ROOT	_	_"]

    sents = list(read_conllx_corpus(lines))
    assert len(sents) == 2
    assert len(sents[0]) == 1
    assert len(sents[1]) == 1

    token = CONLLXToken(form='broda', lemma='_', cpostag='gismu', postag='gismu',
                        feats='_', head=0, deprel='ROOT', phead='_', pdeprel='_')
    assert sents[0][0] == token

    token = CONLLXToken(form='brode', lemma='_', cpostag='gismu', postag='gismu',
                        feats='_', head=0, deprel='ROOT', phead='_', pdeprel='_')
    assert sents[1][0] == token


def test_eval():
    ans_str = ["1	mi	_	KOhA	KOhA	_	2	P1	_	_",
               "2	broda	_	gismu	gismu	_	0	ROOT	_	_"]
    sys_str = ["1	mi	_	KOhA	KOhA	_	1	PX	_	_",
               "2	broda	_	gismu	gismu	_	0	ROOTX	_	_"]

    ans_sent = parse_conllx_sent(ans_str)
    sys_sent = parse_conllx_sent(sys_str)
    stats = evaluate_sent(ans_sent, sys_sent)
    assert stats['num_tokens'] == 2
    assert stats['unlabeled_matches'] == 1
    assert stats['labeled_matches'] == 0

    ans_corpus = list(read_conllx_corpus(ans_str))
    sys_corpus = list(read_conllx_corpus(sys_str))
    results = evaluate(ans_corpus, sys_corpus)
    assert results['UAS'] == 0.5
    assert results['LAS'] == 0.0


def test_depparse():
    parse = list(depparser.parse(""))
    assert [] == parse

    sent = list(depparser.parse("ko'a broda"))[0]
    assert 2 == len(sent)
    assert "ko'a" == sent[0].form
    assert "broda" == sent[1].form
