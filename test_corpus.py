#!/usr/bin/python
# coding: utf-8

import pycantonese as pc # assuming pycantonese.py is in the same directory

##----------------------------------------------------------------------------##
## read corpus data

dataPath = 'data_sample' # the folder "data_sample" (which has data_sample.txt)
                         # is in the same directory as this script
currentCorpus = pc.read_corpus(dataPath)

##----------------------------------------------------------------------------##
## customized functions

def printListUTF8(stringlist):
    for word in stringlist:
        try:
            print unicode(word, encoding='utf-8')
        except:
            print repr(word)

def final_tone(corpus, what_final_tone):
    final = what_final_tone[: -1]
    tone = what_final_tone[-1]
    return pc.search_jp(corpus, [(final, 2), (tone, 3)], 'type')

##----------------------------------------------------------------------------##
## sample usage of PyCantonese

print '\nFind all words with a specific tone (e.g., tone 4):'
tone4 = pc.tone(currentCorpus, '4', 'type')
print 'There are %d matching words, e.g.:' % (len(tone4))
printListUTF8(tone4[: 5]) # 5 results

print '\nFind all words with a specific onset/initial (e.g., \'b\'):'
b = pc.onset(currentCorpus, 'b', 'type') # the function initial() is the same
print 'There are %d matching words, e.g.:' % (len(b))
printListUTF8(b[: 5]) # 5 results

print '\nFind all words with a specific nucleus (e.g., \'aa\'):'
aa = pc.nucleus(currentCorpus, 'aa', 'type')
print 'There are %d matching words, e.g.:' % (len(aa))
printListUTF8(aa[: 5]) # 5 results

print '\nFind all words with a specific coda (e.g., \'ng\'):'
ng = pc.coda(currentCorpus, 'ng', 'type')
print 'There are %d matching words, e.g.:' % (len(ng))
printListUTF8(ng[: 5]) # 5 results

print '\nFind all words with a specific final (e.g., \'aan\'):'
aan = pc.final(currentCorpus, 'aan', 'type')
print 'There are %d matching words, e.g.:' % (len(aan))
printListUTF8(aan[: 5]) # 5 results

print '\n*** using a customized function not from PyCantonese ***\n' + \
      'Find all words with a specific coda plus a tone (e.g., \'t\' and \'3\'):'
t3 = final_tone(currentCorpus, 't3')
print 'There are %d matching words, e.g.:' % (len(t3))
printListUTF8(t3[: 5]) # 5 results

print '\nFind all words with a specific character (e.g., \'我\'):'
ngo5 = pc.character(currentCorpus, '我', 'type')
print 'There are %d matching words, e.g.:' % (len(ngo5))
printListUTF8(ngo5[: 5]) # 5 results

print '\nFind all words with a specific character (e.g., \'我\'),'
print 'each instance with a range -- -2 characters and +3 characters:'
ngo5_range = pc.character_range(currentCorpus, '我', 2, 3)
print 'There are %d instances of \'我\', e.g.:' % (len(ngo5_range))
for i in range(3): # 3 results
    printListUTF8(ngo5_range[i])
    print
