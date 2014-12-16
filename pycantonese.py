#!/usr/bin/python
# coding: utf-8

'''

Developer: Jackson L. Lee
In collaboration with Litong Chen and Tsz-Him Tsui
for testing and compiling datasets

'''

import os
import nltk

ONSET = set(['b', 'd', 'g', 'gw', 'z', 'p', 't', 'k', 'kw', 'c', 'm', 'n',
             'ng', 'f', 'h', 's', 'l', 'w', 'j', ''])

NUCLEUS = set(['aa', 'a', 'i', 'yu', 'u', 'oe', 'e', 'eo', 'o', 'm', 'ng'])

CODA = set(['p', 't', 'k', 'm', 'n', 'ng', 'i', 'u', ''])

TONE = set(['1', '2', '3', '4', '5', '6'])

class JyutpingError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

def jyutping(jpString):
    """
    parses jpString as a list of Cantonese romanization jyutping strings and
    outputs a list of 4-tuples, each as (onset, nucleus, coda, tone)

    """

    ## check jpString as a valid argument string
    if type(jpString) is not str:
        raise JyutpingError('argument needs to be a string -- ' + repr(jp))
    jpString = jpString.lower()

    ## parse jpString as multiple jp strings
    jpList = list()
    jpCurrent = ''
    for c in jpString:
        jpCurrent = jpCurrent + c
        if c.isdigit():
            jpList.append(jpCurrent)
            jpCurrent = ''

    if not jpString[-1].isdigit():
        raise JyutpingError('tone error -- ' + repr(jp))

    jpParsedList = list()

    for jp in jpList:

        if len(jp) < 2:
            raise JyutpingError('argument string needs to contain '
                                'at least 2 characters -- ' + repr(jp))

        ## tone
        if (not jp[-1].isdigit()) or (jp[-1] not in TONE):
            raise JyutpingError('tone error -- ' + repr(jp))

        tone = jp[-1]
        cvc = jp[:-1]

        ## coda
        if not (cvc[-1] in 'ieaouptkmng'):
            raise JyutpingError('coda error -- ' + repr(jp))

        if cvc in ['m', 'ng', 'i', 'e', 'aa', 'o', 'u']:
            jpParsedList.append(('', cvc, '', tone))
            continue
        elif cvc[-2:] == 'ng':
            coda = 'ng'
            cv = cvc[:-2]
        elif (cvc[-1] in 'ptkmn') or \
             ((cvc[-1] == 'i') and (cvc[-2] in 'eaou')) or \
             ((cvc[-1] == 'u') and (cvc[-2] in 'ieao')):
            coda = cvc[-1]
            cv = cvc[:-1]
        else:
            coda = ''
            cv = cvc

        # nucleus, and then onset
        nucleus = ''

        while cv[-1] in 'ieaouy':
            nucleus = cv[-1] + nucleus
            cv = cv[:-1]
            if not cv:
                break

        if not nucleus:
            raise JyutpingError('nucleus error -- ' + repr(jp))

        onset = cv



        if onset not in ONSET:
            raise JyutpingError('onset error -- ' + repr(jp))

        jpParsedList.append((onset, nucleus, coda, tone))

    return jpParsedList


class CantoneseWord_withPOS():
    def __init__(self, inputWord):
        characterPlusJyutping, slash, self.pos_string = inputWord.split('/')
        self.characters, self.jp_string = characterPlusJyutping.split('_')
        self.msg = msg

    def char(self):
        return self.characters

    def jp(self):
        return self.jp_string

    def pos(self):
        return self.pos_string


def read_corpus(path):
    '''
    returns NLTK corpus object given data from path
    type(path) = str
    '''
    from nltk.corpus.reader.tagged import TaggedCorpusReader as corpusreader
    return corpusreader(path, os.listdir(path))

def all_characters():
    return

def all_jyutping():
    return

def character(corpus, what_character, output='token'):
    resultList = list()

    for character_jpString in corpus.words():

        if character_jpString.count('_') == 1:
            character, jpString = character_jpString.split('_')

            if what_character in character:
                resultList.append(character_jpString)

    if output == 'type':
        return list(set(resultList))
    else:
        return resultList

def search_jp(corpus, whatPositionList, output='token'):
    resultList = list()

    for character_jpString in corpus.words():

        if character_jpString.count('_') == 1:
            character, jpString = character_jpString.split('_')

            try:
                jpList = jyutping(jpString)
            except:
                continue

            for jp in jpList:
                checkList = [0] * len(whatPositionList)

                for (e, (what, position)) in enumerate(whatPositionList):

                    if jp[position] == what:
                        checkList[e] = 1

                if all(checkList):
                    resultList.append(character_jpString)
                    break

    if output == 'type':
        return list(set(resultList))
    else:
        return resultList

def onset(corpus, what_onset, output='token'):
    if what_onset in ONSET:
        return search_jp(corpus, [(what_onset, 0)], output)
    else:
        raise JyutpingError('onset error -- ' + repr(what_onset))

def initial(corpus, what_onset, output='token'):
    if what_onset in ONSET:
        return onset(corpus, what_onset, output)
    else:
        raise JyutpingError('onset error -- ' + repr(what_onset))

def nucleus(corpus, what_nucleus, output='token'):
    if what_nucleus in NUCLEUS:
        return search_jp(corpus, [(what_nucleus, 1)], output)
    else:
        raise JyutpingError('nucleus error -- ' + repr(what_nucleus))

def coda(corpus, what_coda, output='token'):
    if what_coda in CODA:
        return search_jp(corpus, [(what_coda, 2)], output)
    else:
        raise JyutpingError('coda error -- ' + repr(what_coda))

def tone(corpus, what_tone, output='token'):
    if what_tone in TONE:
        return search_jp(corpus, [(what_tone, 3)], output)
    else:
        raise JyutpingError('tone error -- ' + repr(what_tone))

def final(corpus, what_final, output='token'):
    if (type(what_final) is not str) and (len(what_final) < 1):
        raise JyutpingError('final error -- ' + repr(what_final))
    validFinal = False

    for i in range(1, len(what_final)+1):
        possibleNucleus = what_final[: i]
        possibleCoda = what_final[i :]

        if (possibleNucleus in NUCLEUS) and (possibleCoda in CODA):
            validFinal = True
            what_nucleus = possibleNucleus
            what_coda = possibleCoda
            break

    if validFinal:
        return search_jp(corpus, [(what_nucleus, 1), (what_coda, 2)], output)
    else:
        raise JyutpingError('final error -- ' + repr(what_final))

def character_range(corpus, what_character, before, after):
    resultList = list()

    wordList = corpus.words()
    wordListLen = len(wordList)

    for (idx, character_jpString) in enumerate(wordList):

        if character_jpString.count('_') == 1:
            character, jpString = character_jpString.split('_')

            if what_character in character:

                if before < idx:
                    start = idx - before
                else:
                    start = 0

                if (after + idx) > wordListLen:
                    end = wordListLen
                else:
                    end = after + idx + 1

                resultList.append(wordList[start: end])

    return resultList

if __name__ == "__main__":
    import doctest
    doctest.testmod()
