
def semantic_parse(parse):
    for node in parse:
        if node.name in ['sentence', 'bridiTail3']:
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


def next_available_place(places, current_place):
    current_place += 1
    while current_place in places:
        current_place += 1
    return current_place


def number_sumti_in_sentence(parse):
    """Number sumti in a sentence"""

    assert parse.name in ['sentence', 'bridiTail3']

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

    # now walk through sentence_elements and fill places
    places = dict()     # a dict from place to sumti
    current_place = 0
    for node in sentence_elements:
        print node
        if node.name == 'sumti6':
            current_place = next_available_place(places, current_place)
            places[current_place] = node
            print "sumti6 - %s (%s, %s)" % (node.lojban, selbri_node.lojban, current_place)
        elif node.name == 'term1':
            if node[0].name == 'CMAVO' and node[0][0].name == 'FA':
                current_place = FA_TAGS[node[0][0][0]]
                places[current_place] = node[1]
                print "term1 - %s (%s, %s)" % (node[1].lojban, selbri_node.lojban, current_place)

        elif node.name in ['selbri3', 'BRIVLA'] and current_place == 0:
            current_place = next_available_place(places, current_place)
        elif node.name == 'CMAVO':
            current_place = next_available_place(places, current_place)
            places[current_place] = node
            print "CMAVO - %s (%s, %s)" % (node.lojban, selbri_node.lojban, current_place)

    # TODO - deal with SE here

    # assign place infomation to each sumti/CMAVO
    for place, node in places.iteritems():
        node.place = (selbri_node, place)
