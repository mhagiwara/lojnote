
def semantic_parse(parse):
    for node in parse:
        if node.name == 'sentence':
            number_sumti_in_sentence(node)
        else:
            semantic_parse(node)

FA_TAGS = {
    'fa': 1,
    'fe': 2,
    'fi': 3,
    'fo': 4,
    'fu': 5
}


def number_sumti_in_sentence(parse):
    """Number sumti in a sentence"""

    assert parse.name == 'sentence'

    sentence_elements = []
    for node in parse:
        if node.name == 'bridiTail3':
            for subnode in node:
                if subnode.name == 'terms':
                    # put individual terms in sentence_elements
                    for subsubnode in subnode:
                        sentence_elements.append(subsubnode)
                else:
                    sentence_elements.append(subnode)
        else:
            sentence_elements.append(node)

    # find the selbri element
    selbri_cands = [node for node in sentence_elements if node.name in ['selbri3', 'BRIVLA']]
    selbri_node = selbri_cands[0] if len(selbri_cands) > 0 else None

    # now walk through sentence_elements
    sumti_counter = 1
    for node in sentence_elements:
        print node
        if node.name == 'sumti6':
            node.place = (selbri_node, sumti_counter)
            print "sumti6 - %s (%s, %s)" % (node.lojban, selbri_node.lojban, sumti_counter)
            # TODO: replace this with 'next unoccupied place'
            sumti_counter += 1
        elif node.name == 'term1':
            if node[0].name == 'CMAVO' and node[0][0].name == 'FA':
                sumti_counter = FA_TAGS[node[0][0][0]]
                node[1].place = (selbri_node, sumti_counter)
                print "term1 - %s (%s, %s)" % (node[1].lojban, selbri_node.lojban, sumti_counter)
                # TODO: replace this with 'next unoccupied place'
                sumti_counter += 1
            else:
                pass

        elif node.name in ['selbri3', 'BRIVLA'] and sumti_counter == 1:
            # TODO: replace this with 'next unoccupied place'
            sumti_counter += 1
        elif node.name == 'CMAVO':
            node.place = (selbri_node, sumti_counter)
            print "CMAVO - %s (%s, %s)" % (node.lojban, selbri_node.lojban, sumti_counter)
