#!/usr/bin/python

# Takes an ARPA formatted LM (such as one produced by SRILM) and transforms it
# into the FST format used by OpenFst. In order to be used in OpenFST it needs
# to be subsequently compiled using fstcompile.
#
# ISSUES:
# Currently only supports trigram LMs.

import sys, string, re, codecs, math, argparse

def main():
  # Parse command line arguments
  parser = argparse.ArgumentParser(usage=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter,
      description='Convert an ARPA formatted language model to a text file ' +
          'representation of an FST. The FST can be subsequently compiled ' + 
          'using the OpenFST fstcompile command.')
  parser.add_argument("lm", help="ARPA Formatted Language Model")
  parser.add_argument("--start_symbol", "-s", default='<s>', help='Set the ' +
      'symbol representing the start of a sentence.')
  parser.add_argument("--end_symbol", "-e", default='</s>', help='Set the ' + 
      'symbol representing the end of a sentence.')
  parser.add_argument("--backoff", "-b", default='once', 
      choices=['once'', twice' ], help='Backoff is not handled directly. Once' +
      ' refers to always allowing backoff from trigram to unigram. Twice ' +
      'refers to only allowing backoff to bigram, potentially counting the ' +
      'the backoff twice.')
  parser.add_argument("--codec", "-c", default='utf-8', help='Codec used for ' +
      'the lm file and the output.')
  parser.add_argument("--output", "-o", default=sys.stdout, help='Name of the' +
      ' file to write the FST to.')
  args = parser.parse_args()

  fout = codecs.getwriter(args.codec)(args.output)

  words = {}

  # We have four special states: initial state, start_symbol state, null backoff
  # state, and end_symbol state. Only a single arc exists between initial state
  # and start symbol state. Can only get to the null backoff state after passing
  # through the start_symbol state

  words[args.start_symbol] = 1
  words[args.end_symbol] = 2
  words['@@RESERVED_FOR_NULL_STATE@@'] = 3
  null_state = 3
  index = 4

  # Add dummy arc from initial state to state_symbol state. Forces OpenFST to 
  # recognize the correct initial state.
  fout.write("0 1 " + args.start_symbol + " " + args.start_symbol + " 1000000\n")

  current_ngram = 0

  with codecs.open(args.lm, 'r', encoding=args.codec) as fin:
    for line in fin:
      line = line.strip()
      data = line.split()
      if line == '\\1-grams:':
        current_ngram = 1
      elif line == '\\2-grams:':
        current_ngram = 2
      elif line == '\\3-grams:':
        current_ngram = 3
      elif line == '\\4-grams:':
        current_ngram = 4
      if current_ngram > 0 and len(data) > 1 and is_float(data[0]):
        score = str(-float(data[0]))
        if current_ngram == 1: # Unigram entry with backoff
          if data[1] not in words:
            words[ data[1] ] = index
            index = index + 1

          # Set the correct destination for the transition.
          if len(data) > 2:
            backoff = str(-float(data[2]))
            dest = str(words[data[1]])
            fout.write(str(words[data[1]]) + " " + str(null_state) +  " <eps> <eps> " + backoff + "\n")
          elif data[1] == args.end_symbol:
            dest = str(words[data[1]])
          else:
            dest = str(null_state)

          # Add the unigram transition.
          if data[1] == args.start_symbol:
            fout.write("0 " + dest + " " + data[1] + " " + data[1] + " " + score + "\n")
          else:
            fout.write(str(null_state) + " " + dest + " " + data[1] + " " + data[1] + " " + score + "\n")
        elif current_ngram == 2: # Bigram entry
          # All unigrams should already have been seen.
          if data[1] not in words or data[2] not in words:
            system.exit("Bigram contains previously unseen unigram.\n" + line)
          if data[1] + " " + data[2] not in words:
            words[ data[1] + " " + data[2] ] = index
            index = index + 1
          
          # Set the correct destination for the transition.
          if len(data) > 3:
            backoff = str(-float(data[3]))
            dest = str(words[data[1] + " " + data[2]])
            fout.write(str(words[data[1] + " " + data[2]]) + " " + str(words[data[2]]) +  " <eps> <eps> " + backoff + "\n")
            if args.backoff == 'once':
              fout.write(str(words[data[1] + " " + data[2]]) + " " + str(null_state) +  " <eps> <eps> " + backoff + "\n")
          else:
            dest = str(words[data[2]])
          fout.write(str(words[data[1]]) + " " + dest + " " + data[2] + " " + data[2] + " " + score + "\n")
        elif current_ngram == 3: # Trigram entry
          # All unigrams and bigrams should have already been seen.
          if data[1] not in words or data[2] not in words or data[3] not in words:
            system.exit("Trigram contains previously unseen unigram.\n" + line)
          if data[1] + " " + data[2] not in words or data[2] + " " + data[3] not in words:
            system.exit("Trigram contains previously unseen biigram.\n" + line)
          fout.write(str(words[ data[1] + " " + data[2] ]) + " " + str(words[ data[2] + " " + data[3] ]) + " " + data[3] + " " + data[3] + " " + score + "\n")

  fout.write(str(words["</s>"]) + "\n")
  fout.close()

def is_float(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

if __name__ == "__main__":
    main()
