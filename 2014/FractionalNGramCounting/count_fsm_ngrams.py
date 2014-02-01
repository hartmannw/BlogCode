#!/usr/bin/python

# Takes a lattice stored in OpenFST ascii format and counts the fractional
# ngrams.

import sys, string, re, codecs, argparse, copy

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser(usage=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Counts fractional ngrams in a FSM.')
    parser.add_argument("fsm", help="FSM Lattice to search.")
    parser.add_argument("--max_order", "-m", default=1, help='Set the ' + 
      'maximum order of ngrams.')
    parser.add_argument("--codec", "-c", default='utf-8', help='Codec used ' + 
            'for the lm file and the output.')
    parser.add_argument("--output", "-o", default=sys.stdout, help='Name of ' +
            'the file to write the FST to.')
    args = parser.parse_args()

    fout = codecs.getwriter(args.codec)(args.output)
    
    final_state = [] # Unknown until we read it from fsm.
    start_state = 0 # Assumes start state = 0
    fsm = {}
    ngram = {}
    with codecs.open(args.fsm, 'r', encoding=args.codec) as fin:
        for line in fin:
            line = line.strip()
            data = line.split()
            default_node = {}
            default_node["child"] = []
            default_node["parent"] = []
            default_node["score"] = 1
            if len(data) == 1: # Must be line giving final state
                final_state.append(int(data[0]))
            else: # Must be an arc definition.
                start_node = int(data[0])
                end_node = int(data[1])
                symbol = data[2]
                to_arc = {}
                from_arc = {}
                to_arc["to"] = end_node
                to_arc["label"] = symbol
                from_arc["to"] = start_node
                from_arc["label"] = symbol
                if start_node not in fsm:
                    fsm[start_node] = copy.deepcopy(default_node)
                if end_node not in fsm:
                    fsm[end_node] = copy.deepcopy(default_node)
                fsm[start_node]["child"].append(to_arc)
                fsm[end_node]["parent"].append(from_arc)

    occupancy_probability(fsm, final_state[0])
    count_ngrams(fsm, ngram, 3)

    for key in ngram:
        fout.write(str(ngram[key]) + " " + key + "\n")
    fout.close()
  

def occupancy_probability(fsm, state):
    if not hasattr(occupancy_probability, "dp"):
        occupancy_probability.dp = {}
    if state in occupancy_probability.dp:
        return occupancy_probability.dp[state]
    score = 0
    for parent in fsm[state]["parent"]:
        score = score + (
                occupancy_probability(fsm, parent["to"]) *
                (1.0 / len(fsm[parent["to"]]["child"])))
    if len(fsm[state]["parent"]) == 0:
        score = 1
    fsm[state]["score"] = score
    occupancy_probability.dp[state] = score
    return score

def count_ngrams(fsm, ngram, order):
    for state in fsm:
        ngrams_from_state(fsm, ngram, state, '', fsm[state]["score"], order)


def ngrams_from_state(fsm, ngram, state, history, cost, order):
    if len(history) > 0:
        ngram[history] = ngram.get(history, 0) + cost
    if order <= 0:
        return
    for child in fsm[state]["child"]:
        ngrams_from_state(fsm, ngram, child["to"], 
                (history + " " + child["label"]).strip(),
                cost * (1.0 / len(fsm[state]["child"])), order - 1)


if __name__ == "__main__":
    main()
