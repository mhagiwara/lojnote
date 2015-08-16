
def semantic_parse(parse):
    for node in parse:
        if node.name == 'sentence':
            number_sumti_in_sentence(node)
        else:
            semantic_parse(node)

FA_TAGS = {
    'FA': 1,
    'FE': 2,
    'FI': 3,
    'FO': 4,
    'FU': 5
}


def number_sumti_in_sentence(parse):
    """Number sumtis in a sentence"""

    assert parse.name == 'sentence'

    sentence_elements = []
    for node in parse:
        if node.name == 'bridiTail3':
            for subnode in node:
                if subnode.name == 'terms':
                    for subsubnode in subnode:
                        sentence_elements.append(subsubnode)
                else:
                    sentence_elements.append(subnode)
        else:
            sentence_elements.append(node)

    sumti_counter = 1
    print sentence_elements


if __name__ == '__main__':
    import camxes
    parse = camxes.parse('mi klama fi le zarci bai lo broda')
    print semantic_parse(parse)
