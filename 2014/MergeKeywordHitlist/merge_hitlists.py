#!/usr/bin/python

# Takes a set of hitlists and merges them depending on the options.

import sys
import string
import re
import codecs
import argparse
import math
from operator import itemgetter
import datetime

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(usage=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Merge a set of hit list files into a single hit list.')
    parser.add_argument("kwlist", nargs='+', help="List of keyword hit lists")
    parser.add_argument("--prune", "-b", default=0.0, type=float, 
            help='Only hits >= prune are printed.')
    parser.add_argument("--codec", "-c", default='utf-8', help='Codec used for ' +
            'the lm file and the output.')
    parser.add_argument("--keywords", "-k", help='List of keywords ' +
            'to consider. Useful to merge only certain keywords. Default is all' +
            ' keywords.')
    parser.add_argument("--merge", "-m", default="max", 
            choices=["min", "max", "mean", "rank", "majority", "gmean", "fast"], 
            help='Sets the method for merging hits from multiple hit lists.\n' +
                 'Note that the unscored option is important because it sets ' +
                 'whether a missing item in a hit list is just treated as ' +
                 'missing, or as a score of 0.\n' +
                 'min - minimum score in all hitlists.\n' + 
                 'max - maximum score in all hitlists.\n' + 
                 'mean - average score in all hitlists.\n' +
                 'rank - takes the score from the first hitlist that has a ' + 
                 'score for that hit.\n')
    parser.add_argument("--output", "-o", default='-', help='Name of the' +
            ' file to write the merged hitlist.')
    parser.add_argument("--threshold", "-t", default=0.5, type=float, 
            help="Minimum score for a hit to be considered a keyword.")
    parser.add_argument("--unscored", "-u", action='store_true', 
            help="Treat all hits not in the hitlist as having a score of 0.")
  
    args = parser.parse_args()
    max_overlap = 0.01
    
    kwlist = []
    for idx, kw in enumerate(args.kwlist):
        kwlist.append(ParseKWList(kw, idx, args))
  
    keywords = []
    if args.keywords:
        # Load list of keywords from file.
        with codecs.open(args.keywords, mode='r', encoding=args.codec) as fin:
            for line in fin:
                keywords.append(line.strip())
    else:
        for kw in kwlist:
            for key in kw:
                keywords.append(key)
    keywords = sorted(set(keywords))

    # Merge all of the hit lists into a single list.
    hitlist = {}
    for key in keywords:
        hitlist[key] = []
        for kw in kwlist:
            for hit in kw.get(key, []):
                hitlist[key].append(hit)
        if args.merge == "fast":
            hitlist[key] = UpdateScore(hitlist[key],args)
        else:
            hitlist[key] = UpdateScore(CompactKWHits(hitlist[key], max_overlap),args)
   
    # Write merged hitlist.
    if args.output == "-":
        fout = codecs.getwriter(args.codec)(sys.stdout)
    else:
        fout = codecs.open(args.output, mode='w', encoding=args.codec)
    fout.write('<kwslist system_id="" language="" kwlist_filename="">\n')
    for k in sorted(hitlist.keys()):
        fout.write('  <detected_kwlist search_time="1" kwid="' + 
                k + '" oov_count="0">\n' )
        hitlist[k] = sorted(hitlist[k], key=itemgetter("score"), reverse=True)
        for x in hitlist.get(k, []):
            if x["score"] >= args.prune:
                WriteKWHit(fout, x)
        fout.write("  </detected_kwlist>\n")
    fout.write('</kwslist>\n')
    fout.close()

def UpdateScore(hitlist, args):
    for i,hit in enumerate(hitlist):
        if args.unscored: # Add score of 0 for any missing scores in score_set.
            for idx, val in enumerate(args.kwlist):
                hit["score_set"][idx] = hit["score_set"].get(idx, 0.0)
        if args.merge == "min":
            hitlist[i]["score"] = min(hit["score_set"].values())
        elif args.merge == "max" or args.merge == "fast":
            hitlist[i]["score"] = max(hit["score_set"].values())
        elif args.merge == "mean":
            hitlist[i]["score"] = float( sum(hit["score_set"].values()) / 
                len(hit["score_set"]) )
        elif args.merge == "gmean":
            hitlist[i]["score"] = float(math.exp( 
                sum( [math.log(x) / len(hit["score_set"]) for x in hit["score_set"].values()])))
        elif args.merge == "rank":
            hitlist[i]["score"] = hit["score_set"][min(hit["score_set"].keys())]
        if hitlist[i]["score"] >= args.threshold:
            hitlist[i]["decision"] = "YES"
        else:
            hitlist[i]["decision"] = "NO"
    return hitlist

def DoesOverlap(a, b, max_overlap):
    if a["file"] != b["file"]:
        return False
    if a["channel"] != b["channel"]:
        return False

    starta = a["tbeg"]
    startb = b["tbeg"]
    enda = starta + a["dur"]
    endb = startb + b["dur"]
    overlap = min([enda, endb]) - max([starta, startb])
    length = min([ a["dur"], b["dur"] ])
    overlap = overlap / length
    if overlap > max_overlap:
        return True
    return False

def CompactKWHits(hits, max_overlap):
    ret = []
    hits = sorted(hits, key=itemgetter('file', 'channel', 'tbeg'))
    for a in hits:
        if len(ret) > 0:
            b = ret[-1]
            if DoesOverlap(a, b, max_overlap):
                for k, val in a["score_set"].iteritems(): # Should only be 1.
                    if val > max(b["score_set"].values()):
                        b["tbeg"] = a["tbeg"]
                        b["dur"] = a["dur"]
                    b["score_set"][k] = max([val, b["score_set"].get(k,0)])
            else:
                ret.append(a)
        else:
            ret.append(a)
    return ret

def ParseKWList(kwlist, idx, args):
    ret = {}
    kw = ""
    with codecs.open(kwlist, mode='r', encoding=args.codec) as fin:
        for line in fin:
            if "<detected_kwlist" in line:
                kw = re.search('kwid=\"([0-9A-Z\-\.]+)\"', line).group(1)
                ret[ kw ] = []
            elif "<kw " in line:
                ret[kw].append(ParseKWHit(line, idx))
            elif "</detected_kwlist>" in line:
                kw = ""
    return ret

def ParseKWHit(line, idx):
    ret = {}
    ret["line"] = line
    if not re.search('score=\"([0-9\.e\-\+inf]+)\"', line):
        print line
    ret["score"] = float(re.search('score=\"([0-9\.e\-\+inf]+)\"', line).group(1))
    if ret["score"] > 1:
        ret["score"] = 1
    elif ret["score"] < 0:
        ret["score"] = 0
    ret["tbeg"] = float(re.search('tbeg=\"([0-9\.]+)\"', line).group(1))
    ret["dur"] = float(re.search('dur=\"([0-9\.]+)\"', line).group(1))
    ret["channel"] = re.search('channel=\"([0-9\.]+)\"', line).group(1)
    ret["file"] = re.search('file=\"([^\".]+)\"', line).group(1)
    ret["decision"] = re.search('decision=\"([^\".]+)\"', line).group(1)
    ret["score_set"] = {}
    ret["score_set"][idx] = ret["score"]

    return ret

def WriteKWHit(fout, hit):
    fout.write("    <kw tbeg=\"" + str(hit["tbeg"]) + "\"")
    fout.write(" dur=\"" + str(hit["dur"]) + "\"")
    fout.write(" file=\"" + hit["file"] + "\"")
    fout.write(" score=\"" + str(hit["score"]) + "\"")
    fout.write(" channel=\"" + hit["channel"] + "\"")
    fout.write(" decision=\"" + hit["decision"] + "\"")
    fout.write(" />\n")

if __name__ == "__main__":
    main()
