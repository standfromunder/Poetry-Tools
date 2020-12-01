from poetrytools.Poetry import Poetry
from poetrytools.simpletokenizer import tokenize

import re


class PoetryRU(Poetry):
    def __init__(self, path_to_dictionary):
        super(PoetryRU, self).__init__(path_to_dictionary)
        self.language = 'RU'

    def tokenize(self, poem):
        tokens = []
        # Problematic characters to replace before regex
        replacements = {u'-': u' ', u'—': u' ', u'\'d': u'ed'}

        for original, replacement in replacements.items():
            replaced = poem.replace(original, replacement)
        # TODO: I just switch off accents removal, due to russian ё
        # I think, I should implement something more intelligent
        # replaced = remove_accents(replaced)

        # Keep apostrophes, discard other non-alphanumeric symbols
        cleaned = re.sub(r'[^0-9a-zA-ZА-Яа-яЁё\s\']', '', replaced)

        for line in cleaned.split('\n'):
            tokens.append([word for word in line.strip().split(' ')])
        return tokens

    def __language_specific_syllables__(self, syllables):
        # Work around some limitations of CMU
        equivalents = {"ER0": "R"}
        return [equivalents[syl] if syl in equivalents else syl for syl in syllables]
