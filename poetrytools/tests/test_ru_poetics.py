import os
import unittest
import sqlite3
import json
import re
from poetrytools.PoetryRU import PoetryRU

class TestENPoems(unittest.TestCase):

    def setUp(self):
        self.poetryRUS = PoetryRU('cmudict/ru_cmudict.json')
        self.number = 0

    def open_poem(self, poem):
        with open(os.path.join('..','poems_0', 'ru', poem), encoding='utf-8') as f:
            return self.poetryRUS.tokenize(f.read())

    def open_test(self, test):
        with open(os.path.join('..', 'poems_0', 'test_files', test), encoding='utf-8') \
                as f:
            return self.poetryRUS.tokenize(f.read())


    def test_easy_rhyme(self):
        easy_test = self.open_test('easy_tests.txt')
        print(easy_test)
        for pair in easy_test:
            print(pair[0], pair[1])
            self.assertTrue(self.poetryRUS.rhymes(pair[0], pair[1]))

    def test_rhyme(self):
        import pandas as pd
        rhymes = pd.read_csv('no_rhymes.csv')
        counter = 0
        counter_true = 0
        for index, row in rhymes.iterrows():
            try:
                if self.poetryRUS.rhymes(row['line1'],row['line2']):
                    counter_true += 1
                counter += 1
                print(counter, counter_true)
            except:
                continue
        print(counter_true / counter)

    def test_rhyme_scheme(self):
        poem = """Я недругов своих прощаю
И даже иногда жалею
А спорить с ними не желаю
Поскольку в споре одолею"""
        tokenized_poem = self.poetryRUS.tokenize(poem)
        rhyme_scheme = self.poetryRUS.guess_rhyme_type(tokenized_poem)
        print('Rhyme scheme: {}'.format(rhyme_scheme))

    def test_count_shemes(self):
        with open('Modern.json') as gold:
            gold = json.load(gold)
        print(len(gold))
        dict_gold = {}

        for i in gold:
            dict_gold[i] = gold.count(i)
        st4 = 0
        st5 = 0
        st6 = 0
        st8 = 0
        for i in dict_gold.items():
            if len(i[0]) == 4:
                st4 += i[1]
            elif len(i[0]) == 5:
                st5 += i[1]
            elif len(i[0]) == 6:
                st6 += i[1]
            elif len(i[0]) == 8:
                st8 += i[1]
        print(f'Четверостишься {st4}')
        print(f'Пятистишья {st5}')
        print(f'Шестистишься {st6}')
        print(f'Восьмистишья {st8}')
        print(sorted(dict_gold.items(), key=lambda x: x[1], reverse=True))


    def test_count_stanzas(self):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT poem FROM poems where period = 'Современная поэзия'")
        poems = cursor.fetchall()

        def sort_poems(poem):
            poem = poem[0]
            poem_len = 0
            tokenized_poem = self.poetryRUS.tokenize(poem)
            stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
            for stanza in stanzas:
                if len(stanza) < 10:
                    poem_len += len(stanza)
                else:
                    poem_len += len(stanza) + 100
            return poem_len
        sorted_poems = sorted(poems, key=sort_poems)
        # while ('</em></em>',) in sorted_poems:
        #     sorted_poems.remove(('</em></em>',))
        # sorted_poems.remove(('</em>',))
        print(sorted_poems)
        # with open('Modern_sort_poems.json', 'w') as out_file:
        #     json.dump(sorted_poems, out_file)



    def test_rhyme_scheme_Gold(self):
        # sqlite_connection = sqlite3.connect('sqlite_python.db')
        # cursor = sqlite_connection.cursor()
        # cursor.execute("SELECT poem FROM poems where period = 'Золотой век'")
        # poems = cursor.fetchall()
        with open('Gold_sort_poems.json') as poems:
            poems = json.load(poems)
        st = 1900

        # for i,poem in enumerate(poems[st:st+100], start=st):
        #     poem = poem[0]
        #     tokenized_poem = self.poetryRUS.tokenize(poem)
        #     stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
        #     for stanza in stanzas:
        #         for line in stanza:
        #             if not re.fullmatch(r'[а-яА-ЯёЁ]+', line[-1]):
        #                 print(i, line[-1], [poem])
        #
        # with open('Gold_sort_poems.json', 'w') as inp:
        #     json.dump(poems, inp)

        with open('Gold.json', 'r') as in_file, open('Gold2.json', 'w') as out_file:
            all_schemes = json.load(in_file)
            for i,poem in enumerate(poems[st:st+100], start=st):
                poem = poem[0]
                tokenized_poem = self.poetryRUS.tokenize(poem)
                stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
                for stanza in stanzas:
                    rhyme_scheme = self.poetryRUS.guess_rhyme_type(stanza)
                    if rhyme_scheme == 'X' or rhyme_scheme == '':
                        continue
                    print('Rhyme scheme for poem number {} {}: {} \n'.format(i, stanza,
                                                                          rhyme_scheme))
                    all_schemes.append(rhyme_scheme)

            json.dump(all_schemes, out_file)
        with open('Gold.json', 'w') as in_file, open('Gold2.json', 'r') as out_file:
            all_schemes = json.load(out_file)
            json.dump(all_schemes, in_file)

    def test_rhyme_scheme_Silv(self):
        # sqlite_connection = sqlite3.connect('sqlite_python.db')
        # cursor = sqlite_connection.cursor()
        # cursor.execute("SELECT poem FROM poems where period = 'Золотой век'")
        # poems = cursor.fetchall()
        with open('Silver_sort_poems.json') as poems:
            poems = json.load(poems)
        st = 1900

        # for i,poem in enumerate(poems[st:st+100], start=st):
        #     poem = poem[0]
        #     tokenized_poem = self.poetryRUS.tokenize(poem)
        #     stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
        #     for stanza in stanzas:
        #         for line in stanza:
        #             if not re.fullmatch(r'[а-яА-ЯёЁ]+', line[-1]):
        #                 print(i, line[-1], [poem])

        # with open('Silver_sort_poems.json', 'w') as inp:
        #     json.dump(poems, inp)

        with open('Silver.json', 'r') as in_file, open('Silver2.json', 'w') as out_file:
            all_schemes = json.load(in_file)
            for i,poem in enumerate(poems[st:st+100], start=st):
                poem = poem[0]
                tokenized_poem = self.poetryRUS.tokenize(poem)
                stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
                for stanza in stanzas:
                    rhyme_scheme = self.poetryRUS.guess_rhyme_type(stanza)
                    if rhyme_scheme == 'X' or rhyme_scheme == '':
                        continue
                    print('Rhyme scheme for poem number {} {}: {} \n'.format(i, stanza,
                                                                          rhyme_scheme))
                    all_schemes.append(rhyme_scheme)

            json.dump(all_schemes, out_file)
        with open('Silver.json', 'w') as in_file, open('Silver2.json', 'r') as out_file:
            all_schemes = json.load(out_file)
            json.dump(all_schemes, in_file)

    def test_rhyme_scheme_Soviet(self):
        # sqlite_connection = sqlite3.connect('sqlite_python.db')
        # cursor = sqlite_connection.cursor()
        # cursor.execute("SELECT poem FROM poems where period = 'Золотой век'")
        # poems = cursor.fetchall()
        with open('Soviet_sort_poems.json') as poems:
            poems = json.load(poems)
        st = 1900

        # for i,poem in enumerate(poems[st:st+100], start=st):
        #     poem = poem[0]
        #     tokenized_poem = self.poetryRUS.tokenize(poem)
        #     stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
        #     for stanza in stanzas:
        #         for line in stanza:
        #             if not re.fullmatch(r'[а-яА-ЯёЁ]+', line[-1]):
        #                 print(i, line[-1], [poem])

        # poems[1902] = ['Кончался август.\n Примолкнул лес.\n Стозвездный Аргус\n Глядел с небес.\n \n А на рассвете\n В пустых полях\n Усатый ветер\n Гулял, как лях.\n \n Еще чуть светел\n Вдали рассвет...\n Гуляет ветер,\n Гуляет Фет.\n \n Среди владений\n И по лесам\n Последний гений\n Гуляет сам.\n \n Не близок полдень,\n Далек закат.\n А он свободен\n От всех плеяд...']
        # poems[1992] = ['Мы с тобою станем старше.\n Загрустим. Начнем седеть.\n На прудах на Патриарших\n Не придется нам сидеть.\n \n Потолчем водицу в ступе,\n Надоест, глядишь, толочь –\n Потеснимся и уступим\n Молодым скамью и ночь.\n \n И усядется другая\n На скамью твою, глядишь..\n Но пока что, дорогая,\n Ты, по-моему, сидишь?\n \n И, насколько мне известно,\n Я! – не кто-нибудь другой –\n Занимаю рядом место\n С этой самой дорогой.\n \n Так пока блестит водица\n И не занята скамья,\n Помоги мне убедиться\n В том, что эта ночь – моя!']
        # with open('Soviet_sort_poems.json', 'w') as inp:
        #     json.dump(poems, inp)


        with open('Soviet.json', 'r') as in_file, open('Soviet2.json', 'w') as out_file:
            all_schemes = json.load(in_file)
            for i,poem in enumerate(poems[st:st+100], start=st):
                poem = poem[0]
                tokenized_poem = self.poetryRUS.tokenize(poem)
                stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
                for stanza in stanzas:
                    rhyme_scheme = self.poetryRUS.guess_rhyme_type(stanza)
                    if rhyme_scheme == 'X' or rhyme_scheme == '':
                        continue
                    print('Rhyme scheme for poem number {} {}: {} \n'.format(i, stanza,
                                                                          rhyme_scheme))
                    all_schemes.append(rhyme_scheme)

            json.dump(all_schemes, out_file)
        with open('Soviet.json', 'w') as in_file, open('Soviet2.json', 'r') as out_file:
            all_schemes = json.load(out_file)
            json.dump(all_schemes, in_file)


    def test_rhyme_scheme_Modern(self):
        # sqlite_connection = sqlite3.connect('sqlite_python.db')
        # cursor = sqlite_connection.cursor()
        # cursor.execute("SELECT poem FROM poems where period = 'Золотой век'")
        # poems = cursor.fetchall()
        with open('Modern_sort_poems.json') as poems:
            poems = json.load(poems)
        st = 1900

        # for i, poem in enumerate(poems[st:st+100], start=st):
        #     poem = poem[0]
        #     tokenized_poem = self.poetryRUS.tokenize(poem)
        #     stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
        #     for stanza in stanzas:
        #         for line in stanza:
        #             if not re.fullmatch(r'[а-яА-ЯёЁ]+', line[-1]):
        #                 print(i,line[-1], [poem])

        # with open('Modern_sort_poems.json', 'w') as inp:
        #    json.dump(poems, inp)

        with open('Modern.json', 'r') as in_file, open('Modern2.json', 'w') as out_file:
            all_schemes = json.load(in_file)
            for i,poem in enumerate(poems[st:st+100], start=st):
                poem = poem[0]
                tokenized_poem = self.poetryRUS.tokenize(poem)
                stanzas = self.poetryRUS.split_into_stanzas(tokenized_poem)
                for stanza in stanzas:
                    rhyme_scheme = self.poetryRUS.guess_rhyme_type(stanza)
                    if rhyme_scheme == 'X' or rhyme_scheme == '':
                        continue
                    print('Rhyme scheme for poem number {} {}: {} \n'.format(i, stanza,
                                                                          rhyme_scheme))
                    all_schemes.append(rhyme_scheme)

            json.dump(all_schemes, out_file)
        with open('Modern.json', 'w') as in_file, open('Modern2.json', 'r') as out_file:
            all_schemes = json.load(out_file)
            json.dump(all_schemes, in_file)


    def test_hard_rhyme(self):
        hard_test = self.open_test('hard_tests.txt')
        for pair in hard_test:
            print(pair[0], pair[1])
            self.assertTrue(self.poetryRUS.rhymes(pair[0], pair[1]))



    def test_poem_1(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aa')

    def test_poem_2(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aaaa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aaaa')

    def test_poem_3(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aaabaaabbbabbcdcdb.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aaabaaabbbabbcdcdb')

    def test_poem_4(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aabb.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aabb')

    def test_poem_5(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aabbcc.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aabbcc')

    def test_poem_6(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aabbccaa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aabbccaa')

    def test_poem_7(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aabbccdd.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aabbccdd')

    def test_poem_8(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aabcbc.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aabcbc')

    def test_poem_9(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aax.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aaX')

    def test_poem_10(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aaxa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aaXa')

    def test_poem_11(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_aaxb.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aaXX')

    def test_poem_12(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_ab.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'XX')

    def test_poem_14(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_abab.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'abab')

    def test_poem_15(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_ababcdcd.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'ababcdcd')

    '''def test_poem_16(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_ababcdcdefef.txt'))
        for stanza in stanzas:
            rhyme_scheme_string, rhyme = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'ababcdcdefef')'''

    def test_poem_17(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_abaxb.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'abaXb')

    def test_poem_18(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_abba.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'abba')

    def test_poem_19(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_abbaa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'abbaa')

    def test_poem_20(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_abbab.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'abbab')

    '''def test_poem_21(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_abbabcbcddefef.txt'))
        for stanza in stanzas:
            rhyme_scheme_string, rhyme = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'abbabcbcddefef')'''

    def test_poem_22(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_axa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aXa')

    def test_poem_23(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_xaa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'Xaa')

    def test_poem_24(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_xabab.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'Xabab')

    def test_poem_25(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_xaxbab.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'XaXbab')

    def test_poem_26(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('rhyme_axaa.txt'))
        for stanza in stanzas:
            rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanza)
            for line in stanza:
                print(' '.join(line))
            print(rhyme_scheme_string, '\n')
            self.assertTrue(rhyme_scheme_string == 'aXaa')

    def test_poem_27(self):
        stanzas = self.poetryRUS.split_into_stanzas(self.open_poem('problems.txt'))
        rhyme_scheme_string = self.poetryRUS.guess_rhyme_type(stanzas[0][:4])
        for line in stanzas[0]:
            print(' '.join(line))
        print(rhyme_scheme_string, '\n')
        self.assertTrue(rhyme_scheme_string == 'aaaa')


if __name__ == '__main__':
    unittest.main()
