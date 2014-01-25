# -*- coding: utf-8 -*-
"""RE pattern objects for detecting and splitting Pinyin.

Splitting pinyin into syllables is not as simple as looking for the maximum
length matches using valid syllables. Instead, lookahead/lookbehind assertions
must be used to validate possible matches. For syllables, the rough approach
used is:
    * Get the longest valid syllable.
    * If it ends in a consonant make sure it's not followed directly by a
        vowel (a hyphen or apostrophe doesn't count).
    * If the above didn't match, repeat for the next longest valid match.

Lookahead/lookbehind assertions are used to ensure that hyphens and
apostrophes are only included in words if used correctly. This helps to weed
out non-Pinyin strings.

"""

from __future__ import unicode_literals
from string import whitespace


vowels = (
    'aɑeiouüvAEIOUÜV'
    'āɑ̄ēīōūǖĀĒĪŌŪǕ'
    'áɑ́éíóúǘÁÉÍÓÚǗ'
    'ǎɑ̌ěǐǒǔǚǍĚǏǑǓǙ'
    'àɑ̀èìòùǜÀÈÌÒÙǛ'
)
consonants = 'bpmfdtnlgkhjqxzcsrzcswyBPMFDTNLGKHJQXZCSRZCSWY'
marks = "·012345:-'"
non_stops = """"#$%&'()*+,-/:;<=>@[\]^_`{|}~"""
stops = '.!?'
printable = vowels + consonants + marks[:-3] + whitespace + stops + non_stops

_a = 'a\u0101\u00E0\u00E1\u01CE'
_e = 'e\u0113\u00E9\u011B\u00E8'
_i = 'i\u012B\u00ED\u01D0\u00EC'
_o = 'o\u014D\u00F3\u01D2\u00F2'
_u = 'u\u016B\u00FA\u01D4\u00F9'
_v = 'v\u00FC\u01D6\u01D8\u01DA\u01DC'

# This is the end-of-syllable-consonant lookahead assertion.
_consonant_end = '(?![%(a)s%(e)s%(i)s%(o)s%(u)s%(v)s]|u:)' % {
    'a': _a, 'e': _e, 'i': _i, 'o': _o, 'u': _u, 'v': _v
}

syl = syllable = (
    '(?:\u00B7|\u2027)?'
    '(?:'
    '(?:(?:[zcs]h|[gkh])u[%(a)s]ng%(consonant_end)s)|'
    '(?:[jqx]i[%(o)s]ng%(consonant_end)s)|'
    '(?:[nljqx]i[%(a)s]ng%(consonant_end)s)|'
    '(?:(?:[zcs]h?|[dtnlgkhrjqxy])u[%(a)s]n%(consonant_end)s)|'
    '(?:(?:[zcs]h|[gkh])u[%(a)s]i)|'
    '(?:(?:[zc]h?|[rdtnlgkhsy])[%(o)s]ng%(consonant_end)s)|'
    '(?:(?:[zcs]h?|[rbpmfdtnlgkhw])?[%(e)s]ng%(consonant_end)s)|'
    '(?:(?:[zcs]h?|[rbpmfdtnlgkhwy])?[%(a)s]ng%(consonant_end)s)|'
    '(?:[bpmdtnljqxy][%(i)s]ng%(consonant_end)s)|'
    '(?:[bpmdtnljqx]i[%(a)s]n%(consonant_end)s)|'
    '(?:[bpmdtnljqx]i[%(a)s]o)|'
    '(?:[nl](?:v|u:|\u00FC)[%(e)s])|'
    '(?:[nl](?:[%(v)s]|u:))|'
    '(?:[jqxy]u[%(e)s])|'
    '(?:[bpmnljqxy][%(i)s]n%(consonant_end)s)|'
    '(?:[mdnljqx]i[%(u)s])|'
    '(?:[bpmdtnljqx]i[%(e)s])|'
    '(?:[dljqx]i[%(a)s])|'
    '(?:(?:[zcs]h?|[rdtnlgkhxqjy])[%(u)s]n%(consonant_end)s)|'
    '(?:(?:[zcs]h?|[rdtgkh])u[%(i)s])|'
    '(?:(?:[zcs]h?|[rdtnlgkh])u[%(o)s])|'
    '(?:(?:[zcs]h|[rgkh])u[%(a)s])|'
    '(?:(?:[zcs]h?|[rbpmfdngkhw])?[%(e)s]n%(consonant_end)s)|'
    '(?:(?:[zcs]h?|[rbpmfdtnlgkhwy])?[%(a)s]n%(consonant_end)s)|'
    '(?:(?:[zcs]h?|[rpmfdtnlgkhy])?[%(o)s]u)|'
    '(?:(?:[zcs]h?|[rbpmdtnlgkhy])?[%(a)s]o)|'
    '(?:(?:[zs]h|[bpmfdtnlgkhwz])?[%(e)s]i)|'
    '(?:(?:[zcs]h?|[bpmdtnlgkhw])?[%(a)s]i)|'
    '(?:(?:[zcs]h?|[rjqxybpmdtnl])[%(i)s])|'
    '(?:(?:[zcs]h?|[rwbpmfdtnlgkhjqxwy])[%(u)s])|'
    '(?:(?:[zcs]h?|[rmdtnlgkhy])?[%(e)s])|'
    '(?:[bpmfwyl]?[%(o)s])|'
    '(?:(?:[zcs]h|[bpmfdtnlgkhzcswy])?[%(a)s])'
    ')(?:r%(consonant_end)s)?[0-5]?'
) % {
    'consonant_end': _consonant_end, 'a': _a, 'e': _e, 'i': _i,
    'o': _o, 'u': _u, 'v': _v
}

word = (
    """(?:%(as)s(?:-(?=%(as)s)|'(?=[%(a)s%(e)s%(o)s])(?=%(as)s))?[0-9]*)+"""
) % {'as': syllable, 'a': _a, 'e': _e, 'o': _o}

sent = sentence = (
    """(?:%(word)s|[%(non_stops)s\s])+[.!?]['"\]\}\)]*"""
) % {'word': word, 'non_stops': non_stops}