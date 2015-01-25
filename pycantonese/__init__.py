#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
PyCantonese: A Python module for working with Cantonese corpus data

Developer: Jackson L. Lee

http://pycantonese.github.io

'''

import os
from pkg_resources import resource_string

from nltk.corpus.reader.tagged import TaggedCorpusReader
from nltk.corpus.reader.api import CorpusReader

__version__ = '0.2.1'

#------------------------------------------------------------------------------#
# constants

ABSPATH = os.path.dirname(os.path.abspath(__file__))

ONSET = set(['b', 'd', 'g', 'gw', 'z', 'p', 't', 'k', 'kw', 'c', 'm', 'n',
             'ng', 'f', 'h', 's', 'l', 'w', 'j', ''])

NUCLEUS = set(['aa', 'a', 'i', 'yu', 'u', 'oe', 'e', 'eo', 'o', 'm', 'ng'])

CODA = set(['p', 't', 'k', 'm', 'n', 'ng', 'i', 'u', ''])

TONE = set(['1', '2', '3', '4', '5', '6'])

ONSET_IPA = {'b': 'p',
             'd': 't',
             'g': 'k',
             'gw': 'k\\super w ',
             'z': 'ts',
             'p': 'p\\super h ',
             't': 't\\super h ',
             'k': 'k\\super h ',
             'kw': 'k\\super w\\super h ',
             'c': 'ts\\super h ',
             'm': 'm',
             'n': 'n',
             'ng' :'N',
             'f': 'f',
             'h': 'h',
             's': 's',
             'l': 'l',
             'w': 'w',
             'j': 'j',
             '': '',
            }

FINAL_IPA = {'i': 'i',
             'ip': 'ip\\textcorner ',
             'it': 'it\\textcorner ',
             'ik': 'Ik\\textcorner ',
             'im': 'im',
             'in': 'in',
             'ing': 'IN',
             'iu': 'iu',
             'yu': 'y',
             'yut': 'yt\\textcorner ',
             'yun': 'yn',
             'u': 'u',
             'ut': 'ut\\textcorner ',
             'uk': 'Uk\\textcorner ',
             'un': 'un',
             'ung': 'UN',
             'ui': 'uY',
             'e': 'E',
             'ek': 'Ek\\textcorner ',
             'eng': 'EN',
             'ei': 'eI',
             'eot': '8t\\textcorner ',
             'eon': '8n',
             'eoi': '8Y',
             'oe': '\\oe ',
             'oek': '\\oe k\\textcorner ',
             'oeng': '\\oe N',
             'o': 'O',
             'ot': 'Ot\\textcorner ',
             'ok': 'Ok\\textcorner ',
             'on': 'On',
             'ong': 'ON',
             'oi': 'OY',
             'ou': 'ou',
             'ap': '5p\\textcorner ',
             'at': '5t\\textcorner ',
             'ak': '5k\\textcorner ',
             'am': '5m',
             'an': '5n',
             'ang': '5N',
             'ai': '5I',
             'au': '5u',
             'aa': 'a',
             'aap': 'ap\\textcorner ',
             'aat': 'at\\textcorner ',
             'aak': 'ak\\textcorner ',
             'aam': 'am',
             'aan': 'an',
             'aang': 'aN',
             'aai': 'aI',
             'aau': 'au',
             'm': '\\s{m}',
             'ng': '\\s{N}',
            }

TONE_IPA = {'1': '55',
            '2': '25',
            '3': '33',
            '4': '21',
            '5': '23',
            '6': '22',
           }

FINAL = set(FINAL_IPA.keys())

#------------------------------------------------------------------------------#
# error classes

class JyutpingError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


class SearchError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

#------------------------------------------------------------------------------#
# corpus reader class for all Cantonese corpora in general

class CantoneseCorpusReader():
    '''
    the basic corpus reader for Cantonese corpora
    modeled on TaggedCorpusReader from NLTK
    '''
    def __init__(self, root, fileids):
        self._root = root
        self._fileids = fileids

    def words(self):
        _words = TaggedCorpusReader(self._root, self._fileids).words()
        return [w for w in _words
                if not w.startswith('SP:')]

    def sents(self):
        _sents = TaggedCorpusReader(self._root, self._fileids).sents()
        return [sent[1:] for sent in _sents
                if len(sent) > 1]

    def tagged_words(self):
        _tagged_words = TaggedCorpusReader(self._root,
                                           self._fileids).tagged_words()
        return [(word, tag) for (word, tag) in _tagged_words
                if not word.startswith('SP:')]

    def tagged_sents(self):
        _tagged_sents = TaggedCorpusReader(self._root,
                                           self._fileids).tagged_sents()
        return [tagged_sent[1:] for tagged_sent in _tagged_sents
                if len(tagged_sent) > 1]

    def jyutpings(self):
        '''
        :return: the given file(s) as a list of jyutpings
        :rtype: list(str)
        '''
        return [word.split('_')[1] for word in self.words()
                if '_' in word]

    def characters(self):
        '''
        :return: the given file(s) as a list of characters
        :rtype: list(str)
        '''
        return [word.split('_')[0] for word in self.words()
                if '_' in word]

    def jyutpings_sents(self):
        return [[word.split('_')[1] for word in sent if '_' in word]
                for sent in self.sents()]

    def characters_sents(self):
        return [[word.split('_')[0] for word in sent if '_' in word]
                for sent in self.sents()]

    def characters_tagged_sents(self):
        return [[(word.split('_')[0], tag) for (word, tag) in tagged_sent
                  if '_' in word]
                for tagged_sent in self.tagged_sents()]

    def speaker_tagged_sents(self):
        '''
        return list(tuple(speaker, list(tuple(word, tag))))
        '''
        _tagged_sents = TaggedCorpusReader(self._root,
                                           self._fileids).tagged_sents()
        return [(tagged_sent[0][0][3:], tagged_sent[1:])
                for tagged_sent in _tagged_sents if len(tagged_sent) > 1]

    def readme(self):
        return resource_string(__name__, self._root + '/README')


def read_corpus(path):
    '''
    returns NLTK corpus object given data from path
    type(path) = str
    '''
    return CantoneseCorpusReader(path, os.listdir(path))


#------------------------------------------------------------------------------#
# corpus reader classes for built-in corpora

dir_hkcancor = 'data/luke'

class HKCANCOR_CorpusReader(CantoneseCorpusReader):
    '''
    a subclass of CantoneseCorpusReader
    specific for KK Luke's Hong Kong Cantonese Corpus (Luke and Wong 2015)
    '''
    def __init__(self):
        CantoneseCorpusReader.__init__(self, ABSPATH + '/data/luke', r'FC.*')
#        self._root = root # need this later?
#        self._fileids = fileids # need this later?
        self.speakerfile = resource_string(__name__,
                           dir_hkcancor + '/SPEAKERS').strip('\n').split('\n')
        self.fileinfofile = resource_string(__name__,
                           dir_hkcancor + '/FILE_INFO').strip('\n').split('\n')

    def speakers(self):
        '''
        return a dictionary
        '''
        speakerDict = dict()

        for line in self.speakerfile:
            line = line.strip('\n')
            speakerID, gender_age_origin = line.split()
            gender, age, origin = gender_age_origin.split('-')

            if gender not in ['F', 'M']:
                gender = None
            if not age.isdigit():
                age = None
            else:
                age = int(age)
            if origin == '?':
                origin == None

            speakerDict[speakerID] = {'file': speakerID[:-2],
                                      'gender': gender,
                                      'age': age,
                                      'origin': origin,
                                     }
        return speakerDict

    def files(self):
        '''
        return a dictionary
        '''
        fileDict = dict()

        for line in self.fileinfofile:
            line = line.strip('\n')
            fileID, tape_number, date_of_recording, speakerListAsStr = line.split()

            list_of_speakers = list()
            for speaker in speakerListAsStr:
                list_of_speakers.append(fileID + '-' + speaker)

            fileDict[fileID] = {'tape_number': tape_number,
                                'date_of_recording': date_of_recording,
                                'speakers': list_of_speakers,
                               }
        return fileDict

#    def speaker_filtered_tagged_sents(self, speakerlist):
#        return [tagged_sent
#                for (speaker, tagged_sent) in self.speaker_tagged_sents(self)
#                if speaker in speakerlist]

hkcancor = HKCANCOR_CorpusReader()


#------------------------------------------------------------------------------#
# jyutping parsing

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


def parse_final(what_final):
    try:
        for i in range(1, len(what_final)+1):
            possibleNucleus = what_final[: i]
            possibleCoda = what_final[i :]

            if (possibleNucleus in NUCLEUS) and (possibleCoda in CODA):
                return (possibleNucleus, possibleCoda)
    except:
        return None


def ipa(jpString):
    jpParsedList = jyutping(jpString)
    ipaList = list()

    for jpParsed in jpParsedList:
        _onset = jpParsed[0]
        _final = jpParsed[1] + jpParsed[2]
        _tone = jpParsed[3]
        ipa = ''
        ipa = ONSET_IPA[_onset] + FINAL_IPA[_final]
        ipa = '\\textipa{' + ipa.strip() + '}'  + TONE_IPA[_tone]
        ipaList.append(ipa)

    return ipaList


#------------------------------------------------------------------------------#
# search functions


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



def search(corpus, onset=None, nucleus=None, coda=None, tone=None,
           initial=None, final=None, jp=None,
           character=None,
           wordrangeleft=0, wordrangeright=0,
           sentrangeleft=0, sentrangeright=0,
           speakerlist=None):
    '''
    overall strategy: deal with jp (and all jp-related elements) first, and
                      then the character

    1. jp

    hierarchy of jp and associated search elements:
                      jp
                 /     |    \
      onset/initial  final  tone
                     /   \
                nucleus  coda

    lower search elements cannot be used together with dominating higher
    elements
    '''

    # check if ``corpus`` is really a corpus object
    if not (isinstance(corpus, CantoneseCorpusReader) or isinstance(corpus, CorpusReader)):
        raise SearchError('a corpus object is required')

    # check if search elements conflict with one another
    if (onset != initial) and onset and initial:
        raise SearchError('onset conflicts with initial')
    if initial:
        onset = initial
    if final and (nucleus or coda):
        raise SearchError('final cannot be used together with either nucleus or'
                          ' coda (or both)')
    if jp and (onset or final or nucleus or coda or tone):
        raise SearchError('jp cannot be used together with other Jyutping '
                          'elements')
    if not (type(wordrangeleft) == type(wordrangeright) == int):
        raise SearchError('both wordrangeleft and wordrangeright must be integers')
    if (wordrangeleft < 0) or (wordrangeright < 0):
        raise SearchError('both wordrangeleft and wordrangeright must be non-negative')

    # needs work here
#    if (wordrangeleft or wordrangeright) and \
#       (sentrangeleft or sentrangeright):
#        raise SearchError('word range and sent range cannot be used together')

    # set up characterSearch and jpSearch; check if jyutping search is valid
    characterSearch = False
    jpSearch = False
    if character:
        characterSearch = True
    if onset or nucleus or coda or tone or final or jp:
        jpSearch = True
    if (not characterSearch) and (not jpSearch):
        raise SearchError('no search element')
    if jpSearch:
        if jp:
            try:
                jpSearchList = jyutping(jp)
            except:
                raise SearchError('invalid jyutping -- %s' % (repr(jp)))
            if len(jpSearchList) > 1:
                raise SearchError('only jyutping for one character is allowed')
            else:
                jpSearchTuple = jpSearchList[0]
        else:
            jpCheckDict = { onset: ONSET,
                            nucleus: NUCLEUS,
                            coda: CODA,
                            tone: TONE,
                            final: FINAL,
                          }
            for what in jpCheckDict.keys():
                if not what: # if it is None
                    continue
                if what not in jpCheckDict[what]:
                    raise SearchError('invalid jyutping -- %s' % (repr(what)))
            if final:
                nucleus, coda = parse_final(final)
            del jpCheckDict
            jpSearchTuple = (onset, nucleus, coda, tone)

    _tagged_sents = corpus.tagged_sents()

    resultList = list()

    for tagged_sent in _tagged_sents:
        len_tagged_sent = len(tagged_sent)

        for (idx, (character_jpString, tag)) in enumerate(tagged_sent):

            if character_jpString.count('_') == 1:
                characterStr, jpString = character_jpString.split('_')
            else:
                continue

            # set ``start`` and ``end`` for slicing found results from sent
            start = idx - wordrangeleft
            if start < 0:
                start = 0
            end = idx + wordrangeright + 1
            if end > len_tagged_sent:
                end = len_tagged_sent

            # only character search without jyutping (the easiest case)
            if characterSearch and not jpSearch:
                if character in characterStr:
                    resultList.append(tagged_sent[start: end])
                continue

            # jyutping search, with or without character search as well
            try:
                jpStringParsedList = jyutping(jpString)
            except:
                continue

            potentialMatch = True

            for (_idx, jpStringParsed) in enumerate(jpStringParsedList, 1):
                # walk through the 4 elements of onset, nucleus, coda, tone
                for (idx_tuple, what) in enumerate(jpSearchTuple):
                    if what is None:
                        continue
                    if what != jpStringParsed[idx_tuple]:
                        potentialMatch = False
                        break
                if _idx < len(jpStringParsedList):
                    potentialMatch = True

            if potentialMatch and characterSearch:
                if character in characterStr:
                    resultList.append(tagged_sent[start: end])
            elif potentialMatch:
                resultList.append(tagged_sent[start: end])
    if wordrangeleft == wordrangeright == 0:
        return sum(resultList, [])
    else:
        return resultList

if __name__ == "__main__":
    import doctest
    doctest.testmod()
