
def semantic_parse(parse):
    for node in parse:
        if node.name in ['sentence', 'bridiTail3', 'BRIVLA']:
            return parse_bridi(node)
        else:
            semantic_parse(node)

FA_TAGS = { 'fa': 1, 'fe': 2, 'fi': 3, 'fo': 4, 'fu': 5 }

SE_TAGS = { 'se': 2, 'te': 3, 've': 4, 'xe': 5 }


def next_available_place(places, current_place):
    current_place += 1
    while current_place in places:
        current_place += 1
    return current_place


def parse_bridi(parse):
    """Parse a bridi into a feature-value structure.

       parse: a camxes parse tree

       Returns a dict which corresponds to the feature-value structure of the bridi,
       which contains the following keys:
       1, 2, ...    : places
       'selbri'     : main selbri of the bridi
    """

    assert parse.name in ['sentence', 'bridiTail3', 'BRIVLA']

    print "Analyzing '%s'" % parse.lojban
    print parse

    # put sentence elements into an array
    sentence_elements = []
    if parse.name == 'BRIVLA':
        sentence_elements.append(parse)
    else:
        for node in parse:
            if (node.name == 'bridiTail3'
                    or node.name == 'terms'):   # for more than one sumti before selbri (cu)
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
    selbri_cands = [node for node in sentence_elements if node.name in ['selbri3', 'BRIVLA', 'tanruUnit2']]
    selbri_node = selbri_cands[0] if len(selbri_cands) > 0 else None

    # now walk through sentence_elements and fill features
    places = dict()     # a dict from place to sumti
    current_place = 0
    for node in sentence_elements:
        if node.name == 'sumti6':
            current_place = next_available_place(places, current_place)
            places[current_place] = node
            print "\tsumti6: %s -> (%s, %s)" % (node.lojban, selbri_node.lojban, current_place)
        elif node.name == 'term1':
            if node[0].name == 'CMAVO' and node[0][0].name == 'FA':
                current_place = FA_TAGS[node[0][0][0]]
                places[current_place] = node[1]
                print "\tterm1: %s -> (%s, %s)" % (node[1].lojban, selbri_node.lojban, current_place)

        elif node.name in ['selbri3', 'BRIVLA'] and current_place == 0:
            current_place = next_available_place(places, current_place)

        elif node.name == 'CMAVO' and node[0].name != 'CU':
            current_place = next_available_place(places, current_place)
            places[current_place] = node
            print "\tCMAVO: %s -> (%s, %s)" % (node.lojban, selbri_node.lojban, current_place)
        else:
            print "\t%s: %s - no place" % (node.name, node.lojban)

    # deal with SE and swap places
    if (selbri_node.name == 'tanruUnit2'
        and selbri_node[0].name == 'CMAVO'
        and selbri_node[0][0].name == 'SE'):
        swap_place = SE_TAGS[selbri_node[0][0][0]]
        places[1], places[swap_place] = places[swap_place], places[1]
        selbri_node = selbri_node[1]

    if (selbri_node[-1].name == 'tanruUnit2'
        and selbri_node[-1][0].name == 'CMAVO'
        and selbri_node[-1][0][0].name == 'SE'):
        swap_place = SE_TAGS[selbri_node[-1][0][0][0]]
        places[1], places[swap_place] = places[swap_place], places[1]
        # selbri_node[-1] = selbri_node[-1][1]  TODO: create a new selbri node without SE

    # put selbri
    places['selbri'] = selbri_node

    return places
