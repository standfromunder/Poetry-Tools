# -*- coding: utf-8 -*-

import json
import os
import pandas as pd
from string import ascii_lowercase
from russian_g2p.russian_g2p.Accentor import Accentor
from russian_g2p.russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme
from poetrytools.countsyl import count_syllables


class Poetry:
    def __init__(self, path_to_CMU):
        self.CMU = None
        self.__load__CMU__file(path_to_CMU)

    # def tokenize(self, poem : str):
    #     pass

    def __load__CMU__file(self, path_to_CMU : str):
        # Load up the CMU dictionary
        with open(os.path.join(os.path.dirname(__file__), path_to_CMU)) as json_file:
            self.CMU = json.load(json_file)

    @staticmethod
    def num_vowels(syllables):
        vowels = ('E', 'Y', 'U', 'I', 'O', 'A')
        vowels_counter = 0
        for cur in syllables:
            if cur in vowels:
                vowels_counter += 1
        return vowels_counter

    def caching(function):
        memo = {}
        def wrapper(self, word):
            if word[0] in memo:
                # print(f'{word[0]} in memo {memo}')
                return memo[word[0]]
            else:
                res, num_vowels = function(self, word)
                memo[word[0]] = res, num_vowels
                # print(memo)
                return res, num_vowels
        return wrapper

    @caching
    def get_syllables(self, word):
        """
        Look up a word in the CMU dictionary, return a list of syllables
        """
        '''try:
            return self.CMU[word.lower()]
        except KeyError:
            try:
                return self.CMU[self.replace_similar_vowels(word).lower()]
            except KeyError:
                return False'''
        word_with_accent, num_vowels = Accentor().do_accents([word])
        print(word_with_accent)
        if len(word_with_accent) == 1:
            return [Grapheme2Phoneme().word_to_phonemes(word_with_accent[0][0])], num_vowels
        return [Grapheme2Phoneme().word_to_phonemes(word) for word in
                word_with_accent], num_vowels


    def replace_similar_vowels(self, word):
        return self.__similar_vowels__(word)

    def __similar_vowels__(self, word):
        pass

    def add_stunning_consonants(self, syllables):
        return self.__stunning_consonants__(syllables)

    def __stunning_consonants__(self, syllables):
        pass

    def replace_vowel(self, syllables):
        return self.__vowel_reduction__(syllables)

    def __vowel_reduction__(self, syllables):
        pass

    def replace_syllables(self, syllables):
        return self.__language_specific_syllables__(syllables)

    def __language_specific_syllables__(self, syllables):
        # Work around some limitations of CMU
        # equivalents = {"ER0": "R"}
        # def replace_syllables(syllables):
        #     return [equivalents[syl] if syl in equivalents else syl for syl in syllables]
        pass

    def rhymes(self, word1, word2, level=2):
        """
        For each word, get a list of various syllabic pronunications. Then check whether the last level number of syllables is pronounced the same. If so, the words probably rhyme
        """
        pronunciations, num_vowels1 = self.get_syllables([word1])
        # print(pronunciations)
        pronunciations2, num_vowels2 = self.get_syllables([word2])
        # print(pronunciations2)


        if not (pronunciations and pronunciations2):
            return False
        syls = level # Default number of syllables to check back from
        # If word only has a single vowel (i.e. 'stew'), then we reduce this to 1 otherwise we won't find a monosyllabic rhyme

        for syllables in pronunciations:
            syls = level # Default number of syllables to check back from
            # If word only has a single vowel (i.e. 'stew'), then we reduce this to 1 otherwise we won't find a monosyllabic rhyme
            if num_vowels1 == 1 or len(syllables) == 1:
                syls = 1
                syllables1_without_acc = syllables[:-1] + [syllables[
                    -1].replace(
                    '0', '')]
                # print(syllables1_without_acc)
                for syllables2 in pronunciations2:
                    if syllables2[-syls:] == syllables1_without_acc[-syls:]:
                        # print(syllables, syllables2)
                        return True
            # syllables = self.replace_syllables(syllables)
            # syllables = self.add_stunning_consonants(syllables)
            # syllables = self.replace_vowel(syllables)
            for syllables2 in pronunciations2:
                print(syllables, syllables2)
                if num_vowels2 == 1 or len(syllables2) == 1:
                    syls = 1
                    syllables2_without_acc = syllables2[:-1] + [syllables2[
                        -1].replace(
                        '0', '')]
                    # print(syllables2_without_acc)
                    if syllables[-syls:] == syllables2_without_acc[-syls:]:
                        # print(syllables, syllables2)
                        return True

                # syllables2 = self.replace_syllables(syllables2)
                # syllables2 = self.add_stunning_consonants(syllables2)
                # syllables2 = self.replace_vowel(syllables2)
                # if '0' in syllables[-1] or '0' in syllables2[-1]:
                #
                #     if syllables[-syls-1:-1] == syllables2[-syls:]:
                #         return True
                #     elif syllables[-syls:] == syllables2[-syls-1:-1]:
                #         return True
                #     elif syllables[-syls-1:-1] == syllables2[-syls-1:-1]:
                #         return True
                if syllables[-syls:] == syllables2[-syls:]:
                    # print(syllables, syllables2)
                    return True
        if word1[-level:] == word2[-level:]:
            return True
        return False

        # if pronunciations[-syls:] == pronunciations2[-syls:]:
        #     #print(syllables, syllables2)
        #     return True
        # return False

    def is_accented(self, word):
        for acc in word:
            if '+' in acc:
                return True
        return False


    # def rhyme2(self, word1, word2):
    #     self.__russian_vowels = {'а', 'о', 'у', 'э', 'ы', 'и', 'я', 'ё', 'ю', 'е'}
    #     word1_with_accent = Accentor().do_accents([[word1]])[0][0]
    #     word2_with_accent = Accentor().do_accents([[word2]])[0][0]
    #     rhyme_pairs = \
    #         [('и', 'ы'), ('и', 'ый'), ('ы', 'ый'), ('и', 'е'), ('и', 'ий'), ('у','уй'),
    #      ('ой', 'о'), ('кий', 'ки'), ('ей', 'е'), ('ай', 'о'), ('ой', 'а'), ('ей', 'и'),
    #      ('ий', 'е'), ('и', 'ьи'), ('и', 'ья'), ('ьи', 'ья'), ('и', 'ье'), ('е', 'ье'),
    #      ('к', 'г'), ('х', 'к',), ('г', 'х'), ('а', 'о'), ('е', 'и'), ('ья', 'ье'),
    #      ('ьи', 'ье'), ('ом', 'ым'), ('ит', 'ет'), ('ин', 'ен'), ('ий', 'а'), ('ой', 'а'),
    #      ('ый', 'а'), ('о', 'у'), ('уг', 'ок'), ('ах', 'ых'), ('е', 'ы'), ('ив', 'ов'),
    #      ('и', 'ой'), ('и', 'а'), ('я', 'и'), ('а', 'ы'), ('ы', 'у'), ('я', 'е'),
    #      ('ы', 'о'), ('ый', 'о'), ('ы', 'ой'), ('у', 'ой'), ('у', 'ый'), ('ы', 'ей'),
    #      ('ешь', 'ишь'), ('он', 'ен'), ('ел', 'ол'), ('ей', 'ой'), ('ом', 'ем'),
    #      ('ть', 'дь'), ('д', 'т'), ('ор', 'ер'), ('ом', 'им'), ('ой', 'ый')]
    #     if '+' in word1_with_accent and '+' in word2_with_accent:
    #         vowels_counter = 0
    #         for i,cur in enumerate(word1_with_accent[::-1]):
    #             if cur in self.__russian_vowels:
    #                 vowels_counter += 1
    #                 if '+'==word1_with_accent[-i]:
    #                     str_syl_1 = vowels_counter
    #                     break
    #         vowels_counter = 0
    #         for i, cur in enumerate(word2_with_accent[::-1]):
    #             if cur in self.__russian_vowels:
    #                 vowels_counter += 1
    #                 if '+' == word1_with_accent[-i]:
    #                     str_syl_2 = vowels_counter
    #                     break
    #         if str_syl_1 == str_syl_2:
    #             for pair in rhyme_pairs:
    #                 if word1[-len(pair[0]):] == pair[0] and word2[-len(pair[1]):] == pair[1]:
    #                     return True
    #                 elif word2[-len(pair[0]):] == pair[0] and word1[-len(pair[1]):] == pair[1]:
    #                     return True
    #                 elif word1[-2:] == word2[-2:]:
    #                     return True
    #     else:
    #         pass
    #     return False


    def rhyme_scheme(self, tokenized_poem):
        """
        Get a rhyme scheme for the poem. For each line, lookahead to the future lines of the poem and see whether last words rhyme.
        """

        num_lines = len(tokenized_poem)

        # By default, nothing rhymes
        scheme = ['X'] * num_lines

        rhyme_notation = list(ascii_lowercase)
        currrhyme = -1  # Index into the rhyme_notation

        for lineno in range(0, num_lines):
            matched = False
            for futurelineno in range(lineno + 1, num_lines):
                # If next line is not already part of a rhyme scheme
                if scheme[futurelineno] == 'X':
                    base_line = tokenized_poem[lineno]
                    current_line = tokenized_poem[futurelineno]
                    # print(base_line, current_line)

                    if base_line == ['']:  # If blank line, represent that in the notation
                        scheme[lineno] = ' '

                    elif self.rhymes(base_line[-1], current_line[-1]):
                        if not matched:  # Increment the rhyme notation
                            matched = True
                            currrhyme += 1
                        scheme[lineno] = scheme[futurelineno] = rhyme_notation[currrhyme]
                        # print(scheme)
        return scheme

    def split_into_stanzas(self, tokenized_poem):

        poem_stanzas = [[]]
        for line in tokenized_poem:
            if line != ['']:
                poem_stanzas[len(poem_stanzas) - 1].append(line)
            else:
                poem_stanzas.append([])
        return poem_stanzas

    def guess_rhyme_type(self, tokenized_poem):
        """
        Guess a poem's rhyme via Levenshtein distance from candidates
        """
        joined_lines = ''.join(self.rhyme_scheme(tokenized_poem))
        joined_lines = joined_lines.replace(' ', '')

        return joined_lines
