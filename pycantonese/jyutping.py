# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2017 PyCantonese Project
# Author: Jackson Lee <jacksonlunlee@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

import unicodedata

from pycantonese.util import (endswithoneof, startswithoneof)

ONSET = {'b', 'd', 'g', 'gw', 'z', 'p', 't', 'k', 'kw', 'c', 'm', 'n',
         'ng', 'f', 'h', 's', 'l', 'w', 'j', ''}

NUCLEUS = {'aa', 'a', 'i', 'yu', 'u', 'oe', 'e', 'eo', 'o', 'm', 'ng'}

CODA = {'p', 't', 'k', 'm', 'n', 'ng', 'i', 'u', ''}

TONE = {'1', '2', '3', '4', '5', '6'}

ONSET_TIPA = {'b': 'p',
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
              'ng': 'N',
              'f': 'f',
              'h': 'h',
              's': 's',
              'l': 'l',
              'w': 'w',
              'j': 'j',
              '': '',
              }

FINAL_TIPA = {'i': 'i',
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

TONE_TIPA = {'1': '55',
             '2': '25',
             '3': '33',
             '4': '21',
             '5': '23',
             '6': '22',
             }

FINAL = set(FINAL_TIPA.keys())

ONSET_YALE = {'b': 'b',
              'd': 'd',
              'g': 'g',
              'gw': 'gw',
              'z': 'j',
              'p': 'p',
              't': 't',
              'k': 'k',
              'kw': 'k',
              'c': 'ch',
              'm': 'm',
              'n': 'n',
              'ng': 'ng',
              'f': 'f',
              'h': 'h',
              's': 's',
              'l': 'l',
              'w': 'w',
              'j': 'y',
              '': '',
              }

NUCLEUS_YALE = {'aa': 'aa',
                'a': 'a',
                'i': 'i',
                'yu': 'yu',
                'u': 'u',
                'oe': 'eu',
                'e': 'e',
                'eo': 'eu',
                'o': 'o',
                'm': 'm',
                'ng': 'ng',
                }

CODA_YALE = {'p': 'p',
             't': 't',
             'k': 'k',
             'm': 'm',
             'n': 'n',
             'ng': 'ng',
             'i': 'i',
             'u': 'u',
             '': '',
             }


# ----------------------------------------------------------------------------#
# parse_jyutping parsing


def parse_jyutping(jp_str):
    """
    Parse *jp_str* as a string of Cantonese Jyutping romanization for one or
    multiple characters
    and return a list of 4-tuples, each as (onset, nucleus, coda, tone)
    """
    # check jp_str as a valid argument string
    if type(jp_str) is not str:
        raise ValueError('argument needs to be a string -- ' + repr(jp_str))
    jp_str = jp_str.lower()

    # parse jp_str as multiple jp strings
    jp_list = list()
    jp_current = ''
    for c in jp_str:
        jp_current = jp_current + c
        if c.isdigit():
            jp_list.append(jp_current)
            jp_current = ''

    if not jp_str[-1].isdigit():
        raise ValueError('tone error -- ' + repr(jp_str[-1]))

    jp_parsed_list = list()

    for jp in jp_list:

        if len(jp) < 2:
            raise ValueError('jyutping string has fewer than '
                             '2 characters -- ' + repr(jp))

        tone = jp[-1]
        cvc = jp[:-1]

        # tone
        if tone not in TONE:
            raise ValueError('tone error -- ' + repr(jp))

        # coda
        if not (cvc[-1] in 'ieaouptkmng'):
            raise ValueError('coda error -- ' + repr(jp))

        if cvc in ['m', 'n', 'ng', 'i', 'e', 'aa', 'o', 'u']:
            jp_parsed_list.append(('', cvc, '', tone))
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
            raise ValueError('nucleus error -- ' + repr(jp))

        onset = cv

        if onset not in ONSET:
            raise ValueError('onset error -- ' + repr(jp))

        jp_parsed_list.append((onset, nucleus, coda, tone))

    return jp_parsed_list


def parse_final(final):
    """
    Parse *final* as (nucleus, coda).
    """
    for i in range(1, len(final) + 1):
        possible_nucleus = final[: i]
        possible_coda = final[i:]

        if (possible_nucleus in NUCLEUS) and (possible_coda in CODA):
            return possible_nucleus, possible_coda
    return None


def jyutping2tipa(jp_str):
    """
    Convert *jp_str* to a list of LaTeX TIPA strings.
    """
    jp_parsed_list = parse_jyutping(jp_str)
    tipa_list = list()

    for jp_parsed in jp_parsed_list:
        onset = jp_parsed[0]
        final = jp_parsed[1] + jp_parsed[2]
        tone = jp_parsed[3]
        tipa = ONSET_TIPA[onset] + FINAL_TIPA[final]
        tipa = tipa.strip() + TONE_TIPA[tone]
        tipa_list.append(tipa)

    return tipa_list


def jyutping2yale(jp_str, as_list=False):
    """
    Convert *jp_str* to Yale.

    :param as_list: If True (default: False), return a list of Yale strings
        for individual syllables.
    """
    jp_parsed_list = parse_jyutping(jp_str)
    yale_list = list()

    for jp_parsed in jp_parsed_list:
        onset = ONSET_YALE[jp_parsed[0]]
        nucleus = NUCLEUS_YALE[jp_parsed[1]]
        coda = CODA_YALE[jp_parsed[2]]
        tone = jp_parsed[3]  # still in parse_jyutping

        # jyutping2yale system uses "h" to mark the three low tones
        if tone in {"4", "5", "6"}:
            low_tone_h = "h"
        else:
            low_tone_h = ""

        # in jyutping2yale, long "aa" vowel with no coda is denoted by "a"
        if nucleus == "aa" and coda == "":
            nucleus = "a"

        # when nucleus is "yu"...
        # 1. disallow "yyu" (when onset is "y")
        # 2. change nucleus "yu" into "u" -- this is a hack for adding tone
        #       diacritic, since we don't want "y" to bear the diacritic
        if nucleus == "yu":
            if onset == "y":
                onset = ""
            nucleus = "u"

        # when nucleus is "ng"
        # the tone diacritic has to be on "g" but not "n"
        # now we pretend that the nucleus is "g", and will prepend the "n" back
        # at the end
        if nucleus == 'ng':
            nucleus = 'g'

        # add the jyutping2yale tone diacritic to the first nucleus letter
        # parse_jyutping tone 1      --> add macron
        # parse_jyutping tone 2 or 5 --> add acute
        # parse_jyutping tone 4      --> add grave
        # parse_jyutping tone 3 or 6 --> (no diacritic)
        # If the accented letter doesn't exist in unicode, use the combining
        # accent instead.

        letter = nucleus[0]  # nucleus 1st letter
        unicode_letter_name = unicodedata.name(letter)
        if tone == "1":
            try:
                letter_with_diacritic = unicodedata.lookup(
                    unicode_letter_name + " WITH MACRON")
            except KeyError:
                letter_with_diacritic = letter + "\u0304"
        elif tone in {"2", "5"}:
            try:
                letter_with_diacritic = unicodedata.lookup(
                    unicode_letter_name + " WITH ACUTE")
            except KeyError:
                letter_with_diacritic = letter + "\u0301"
        elif tone == "4":
            try:
                letter_with_diacritic = unicodedata.lookup(
                    unicode_letter_name + " WITH GRAVE")
            except KeyError:
                letter_with_diacritic = letter + "\u0300"
        else:
            # either tone 3 or tone 6
            letter_with_diacritic = letter
        nucleus = letter_with_diacritic + nucleus[1:]

        # add back "y" if the nucleus is "yu"
        # ("y" was taken away for convenience in adding tone diacritic)
        if jp_parsed[1] == "yu":
            nucleus = "y" + nucleus

        # add back "n" if the nucleus is "ng"
        # ('n' was taken away so that tone diacritic is on "g" but not "n")
        if jp_parsed[1] == 'ng':
            nucleus = 'n' + nucleus

        # parse_jyutping final "eu" should be jyutping2yale "ew" (not "eu")
        if coda == "u" and nucleus == "e":
            coda = "w"

        # save the resultant jyutping2yale
        if coda in {"i", "u", "w"} and tone in {"4", "5", "6"}:
            yale = onset + nucleus + coda + low_tone_h
        else:
            yale = onset + nucleus + low_tone_h + coda
        yale_list.append(yale)

    if as_list:
        return yale_list

    # Output yale_list as a string
    # Check if there's potential ambiguity when Yale strings are concatenated

    # Ambiguity case 1:
    #   1st syllable coda is one of the "ambiguous_consonants"
    #   and 2nd syllable starts with a vowel *letter*

    # Ambiguity case 2:
    #   1st syllable has no coda and 2nd syllable starts with one of the
    #   "ambiguous_consonants"
    #   e.g., hei3hau6 'climate' --> heihauh
    #   (middle "h" for tone in 1st syllable or being onset of 2nd syllable?)

    if len(yale_list) == 1:
        return yale_list[0]

    ambiguous_consonants = {'h', 'p', 't', 'k', 'm', 'n', 'ng'}
    vowel_letters = {'a', 'e', 'i', 'o', 'u',
                     'á', 'é', 'í', 'ó', 'ú',
                     'à', 'è', 'ì', 'ò', 'ù',
                     'ā', 'ē', 'ī', 'ō', 'ū'}

    output_str = ''

    for i in range(len(yale_list) - 1):
        yale1 = yale_list[i]
        yale2 = yale_list[i+1]

        ambiguous = False

        # test case 1:
        if endswithoneof(yale1, ambiguous_consonants) and \
                startswithoneof(yale2, vowel_letters):
            ambiguous = True

        # test case 2:
        if not ambiguous and \
                not endswithoneof(yale1, ambiguous_consonants) and \
                startswithoneof(yale2, ambiguous_consonants):
            ambiguous = True

        output_str += yale1

        if ambiguous:
            output_str += '\''

    output_str += yale_list[-1]

    return output_str
