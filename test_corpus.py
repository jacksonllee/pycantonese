import pycantonese as pc # assuming pycantonese.py is in the same directory

##----------------------------------------------------------------------------##
## read corpus data

dataPath = 'data_sample' # the folder "data_sample" (which has data_sample.txt)
                         # is in the same directory as this script
currentCorpus = pc.readCorpus(dataPath)

##----------------------------------------------------------------------------##
## customized functions

def printListUTF8(stringlist):
    for word in stringlist:
        try:
            print unicode(word, encoding='utf-8')
        except:
            pass

def final_tone(corpus, what_final_tone):
    final = what_final_tone[: -1]
    tone = what_final_tone[-1]
    return pc.search(corpus, [(final, 2), (tone, 3)], 'set')

##----------------------------------------------------------------------------##
## sample usage of PyCantonese

print '\nFind all words with a specific tone (e.g., tone 4):'
tone4 = pc.tone(currentCorpus, '4', 'set')
print 'There are %d matching words, e.g.:' % (len(tone4))
printListUTF8(tone4[: 10]) # 10 results

print '\nFind all words with a specific onset/initial (e.g., \'b\'):'
b = pc.onset(currentCorpus, 'b', 'set') # the function initial() is the same
print 'There are %d matching words, e.g.:' % (len(b))
printListUTF8(b[: 10]) # 10 results

print '\nFind all words with a specific nucleus (e.g., \'aa\'):'
aa = pc.nucleus(currentCorpus, 'aa', 'set')
print 'There are %d matching words, e.g.:' % (len(aa))
printListUTF8(aa[: 10]) # 10 results

print '\nFind all words with a specific coda (e.g., \'ng\'):'
ng = pc.coda(currentCorpus, 'ng', 'set')
print 'There are %d matching words, e.g.:' % (len(ng))
printListUTF8(ng[: 10]) # 10 results

print '\nFind all words with a specific final (e.g., \'aan\'):'
aan = pc.final(currentCorpus, 'aan', 'set')
print 'There are %d matching words, e.g.:' % (len(aan))
printListUTF8(aan[: 10]) # 10 results

print '\n*** using a customized function not from PyCantonese ***\n' + \
      'Find all words with a specific coda plus a tone (e.g., \'t\' and \'3\'):'
t3 = final_tone(currentCorpus, 't3')
print 'There are %d matching words, e.g.:' % (len(t3))
printListUTF8(t3[: 10]) # 10 results

