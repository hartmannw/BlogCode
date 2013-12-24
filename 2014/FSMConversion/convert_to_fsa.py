#!/usr/bin/python

# Converts a sequence of strings separated by white space into an OpenFST format
# FSA. If the text contains multiple lines, they FSA is expanded such that each 
# line begins at the same start state and then independently follows a path to a
# final state.

import sys, string, re, codecs, argparse

def main():

  # Parse command line arguments
  parser = argparse.ArgumentParser(usage=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter,
      description='Converts a set of sentences into a single FSA that can be ' +
          'read by OpenFST.')
  parser.add_argument("sequences", help="Set of sentences, one per line.")
  parser.add_argument("--start_symbol", "-s", default='<s>', help='Set the ' +
      'symbol representing the start of a sentence.')
  parser.add_argument("--end_symbol", "-e", default='</s>', help='Set the ' + 
      'symbol representing the end of a sentence.')
  parser.add_argument("--codec", "-c", default='utf-8', help='Codec used for ' +
      'the lm file and the output.')
  parser.add_argument("--output", "-o", default=sys.stdout, help='Name of the' +
      ' file to write the FST to.')
  args = parser.parse_args()

  fout = codecs.getwriter(args.codec)(args.output)

  index = 1
  previous = 0
  final_state = []

  with codecs.open(args.sequences, 'r', encoding=args.codec) as fin:
    for line in fin:
      line = line.strip()
      data = line.split()
      fout.write("0 " + str(index) + " " + args.start_symbol + "\n")
      previous = index
      index = index + 1
      for word in data:
        fout.write(str(previous) + " " + str(index) + " " + word + "\n")
        previous = index
        index = index + 1
      fout.write(str(previous) + " " + str(index) + " " + args.end_symbol + "\n")
      final_state.append(index)
      index = index + 1
  
  for state in final_state:
    fout.write(str(state) + "\n")


if __name__ == "__main__":
    main()
