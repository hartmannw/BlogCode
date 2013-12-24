#!/usr/bin/python

# Converts a list of words into an FST that accepts a characters that correspond
# to a sequence of words in the list. 

import sys, string, re, codecs

def main():
  wordlist = sys.argv[1]

  have_unklist = False
  if len(sys.argv) > 2:
    unklist = sys.argv[2]
    have_unklist = True

  fout = codecs.getwriter("utf-8")(sys.stdout)
  index = 1

  with codecs.open(wordlist, 'r', encoding='utf-8') as fin:
    for line in fin:
      line = line.strip()
      if re.match('^\<.*\>$', line):
        fout.write("0 0 " + line + " " + line + "\n")
      else:
        path = []
        previous = 0
        for i in range(len(line[:-1])):
          if line[i+1] == "@":
            path.append(line[i] + line[i+1])
          elif line[i] != "@":
            path.append(line[i])
        if line[-1] != "@":
          path.append(line[-1])
        #[ path.append(x) for x in list(line) ]
        for x in path[:-1]:
          fout.write(str(previous) + " " + str(index) + " " + x + " <eps>\n")
          previous = index
          index = index + 1
        fout.write(str(previous) + " 0 " + path[-1] + " " + line + "\n")
  
  if have_unklist:
    with codecs.open(unklist, 'r', encoding='utf-8') as fin:
      for line in fin:
        line = line.strip()
        fout.write("0 0 " + line + " " + "<UNK>\n")

  fout.write("0\n")
  fout.close()

if __name__ == "__main__":
    main()
