#------------------------------------------------------------------------------#
# corpus reader class for all Cantonese corpora in general

import os
from pycantonese import ABSPATH

try:
    from nltk.corpus.reader.tagged import TaggedCorpusReader
except ImportError:
    sys.exit("Error in importing NLTK library readers")

class CantoneseCorpusReader():
    '''
    the basic corpus reader for Cantonese corpora
    modeled on TaggedCorpusReader from NLTK
    '''
    def __init__(self, root, fileids):
        self.root = root
        self.fileids = fileids

    def words(self):
        _words = TaggedCorpusReader(self.root, self.fileids).words()
        return (w for w in _words
                if not w.startswith('SP:'))

    def sents(self):
        _sents = TaggedCorpusReader(self.root, self.fileids).sents()
        return (sent[1:] for sent in _sents
                if len(sent) > 1)

    def tagged_words(self):
        _tagged_words = TaggedCorpusReader(self.root,
                                           self.fileids).tagged_words()
        return ((word, tag) for (word, tag) in _tagged_words
                if not word.startswith('SP:'))

    def tagged_sents(self):
        _tagged_sents = TaggedCorpusReader(self.root,
                                           self.fileids).tagged_sents()
        return (tagged_sent[1:] for tagged_sent in _tagged_sents
                if len(tagged_sent) > 1)

    def jyutpings(self):
        '''
        :return: the given file(s) as a list of jyutpings
        :rtype: list(str)
        '''
        return (word.split('_')[1] for word in self.words()
                if '_' in word)

    def characters(self):
        '''
        :return: the given file(s) as a list of characters
        :rtype: list(str)
        '''
        return (word.split('_')[0] for word in self.words()
                if '_' in word)

    def jyutpings_sents(self):
        return ((word.split('_')[1] for word in sent if '_' in word)
                for sent in self.sents())

    def characters_sents(self):
        return ((word.split('_')[0] for word in sent if '_' in word)
                for sent in self.sents())

    def characters_tagged_sents(self):
        return (((word.split('_')[0], tag) for (word, tag) in tagged_sent
                  if '_' in word)
                for tagged_sent in self.tagged_sents())

    def jyutpings_tagged_sents(self):
        return (((word.split('_')[1], tag) for (word, tag) in tagged_sent
                  if '_' in word)
                for tagged_sent in self.tagged_sents())

    def number_of_words(self):
        return len(list(self.words()))

    def number_of_characters(self):
        count_ = 0
        for characters_in_word in self.characters():
            count_ += len(characters_in_word)
        return count_

    def readme(self):
        return open(os.path.join(self.root, "README")).read()


#------------------------------------------------------------------------------#
# corpus reader classes for built-in corpora

dir_hkcancor = ["data", "hkcancor"]

class HKCanCor(CantoneseCorpusReader):
    '''
    a subclass of CorpusReader
    specific for KK Luke's Hong Kong Cantonese Corpus (Luke and Wong 2015)
    '''
    def __init__(self):
        DIR = os.path.join(ABSPATH, *dir_hkcancor)
        CantoneseCorpusReader.__init__(self, DIR, r'FC.*')

        self.speakerfile = open(os.path.join(DIR, "SPEAKERS"))
        self.fileinfofile = open(os.path.join(DIR, "FILE_INFO"))

    def speakers(self):
        '''
        returns a dictionary of key=speakerID, value={file, gender, age, origin}
        '''
        speakerDict = dict()

        for line in self.speakerfile:
            line = line.strip()
            if not line:
                continue

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
        returns a dictionary of
        key=fileID, value={tape_number, date_of_recording, speakers}
        '''
        fileDict = dict()

        for line in self.fileinfofile:
            line = line.strip()
            if not line:
                continue

            fileID, tape_number, date_of_recording, speakerListAsStr = line.split()

            list_of_speakers = list()
            for speaker in speakerListAsStr:
                list_of_speakers.append(fileID + '-' + speaker)

            fileDict[fileID] = {'tape_number': tape_number,
                                'date_of_recording': date_of_recording,
                                'speakers': list_of_speakers,
                               }
        return fileDict

hkcancor = HKCanCor()

