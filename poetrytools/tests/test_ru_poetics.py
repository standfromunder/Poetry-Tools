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
        self.assertTrue(self.poetryRUS.rhymes('счастье', 'ненастье'))

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
        # poems[1912] = ['Мы странно сошлись. Средь салонного круга,\n    В пустом разговоре его,\n Мы словно украдкой, не зная друг друга,\n    Свое угадали родство.\n \n И сходство души не по чувства порыву,\n    Слетевшему с уст наобум,\n Проведали мы, но по мысли отзыву\n    И проблеску внутренних дум.\n \n Занявшись усердно общественным вздором,\n    Шутливое молвя словцо,\n Мы вдруг любопытным, внимательным взором\n    Взглянули друг другу в лицо.\n \n И каждый из нас, болтовнею и шуткой\n    Удачно мороча их всех,\n Подслушал в другом свой заносчивый, жуткой,\n    Ребенка спартанского смех.\n \n И, свидясь, в душе мы чужой отголоска\n    Своей не старались найти,\n Весь вечер вдвоем говорили мы жестко,\n    Держа свою грусть взаперти.\n \n Не зная, придется ль увидеться снова,\n    Нечаянно встретясь вчера,\n С правдивостью странной, жестоко, сурово\n    Мы распрю вели до утра,\n \n Привычные все оскорбляя понятья,\n    Как враг беспощадный с врагом,–\n И молча друг другу, и крепко, как братья,\n    Пожали мы руку потом.']
        # poems[1944] = ['Когда б он знал, что пламенной душою\n С его душой сливаюсь тайно я!\n Когда б он знал, что горькою тоскою\n Отравлена младая жизнь моя!\n Когда б он знал, как страстно и как нежно\n Он, мой кумир, рабой своей любим...\n Когда б он знал, что в грусти безнадежной\n Увяну я, непонятая им!..\n        Когда б он знал!..\n \n Когда б он знал, как дорого мне стоит,\n Как тяжело мне с ним притворной быть!\n Когда б он знал, как томно сердце ноет,\n Когда велит мне гордость страсть таить!..\n Когда б он знал, какое испытанье\n Приносить мне спокойный взор его,\n Когда в замен немаго обожанья\n Я тщетно жду улыбки от него.\n        Когда б он знал!..\n \n Когда б он знал, в душе его убитой\n Любви бы вновь язык заговорил,\n И юности восторг полузабытый\n Его бы вновь согрел и оживил! –\n И я тогда, счастливица!.. любима...\n Любима им, была бы, может быть!\n Надежда льстит тоске неутолимой;\n Не любит он... а мог бы полюбить!\n        Когда б он знал!..']
        # poems[1952] = ['Поздняя осень. Грачи улетели,\n Лес обнажился, поля опустели,\n \n Только не сжата полоска одна...\n Грустную думу наводит она.\n \n Кажется, шепчут колосья друг другу:\n «Скучно нам слушать осенную вьюгу,\n \n Скучно склоняться до самой земли,\n Тучные зерна купая в пыли!\n \n Нас, что ни ночь, разоряют станицы\n Всякой пролетной прожорливой птицы,\n \n Заяц нас топчет, и буря нас бьет...\n Где же наш пахарь? чего еще ждет?\n \n Или мы хуже других уродились?\n Или недружно цвели-колосились?\n \n Нет! мы не хуже других – и давно\n В нас налилось и созрело зерно.\n \n Не для того же пахал он и сеял\n Чтобы нас ветер осенний развеял?..»\n \n Ветер несет им печальный ответ:\n – Вашему пахарю моченьки нет.\n \n Знал, для чего и пахал он и сеял,\n Да не по силам работу затеял.\n \n Плохо бедняге – не ест и не пьет,\n Червь ему сердце больное сосет,\n \n Руки, что вывели борозды эти,\n Высохли в щепку, повисли, как плети.\n \n Очи потускли, и голос пропал,\n Что заунывную песню певал,\n \n Как на соху, налегая рукою,\n Пахарь задумчиво шел полосою.']
        # poems[1954] = ['Сходилась я и расходилась\n Со многими в земном пути;\n Не раз мечтами поделилась,\n Не раз я молвила: «Прости!»\n \n Но до прощанья рокового\n Уже стояла я одна;\n И хладное то было слово,\n Пустой отзы́в пустого сна.\n \n И каждая лишала встреча\n Меня призра́ка моего,\n И не звала я издалеча\n Назад душою никого.\n \n И не по них мне грустно было,\n Мне грустно было по себе,\n Что сердца радостная сила\n Уступит жизненной судьбе;\n \n Что не нисходит с небосклона\n Богиня к жителям земным;\n Что все мы, с жаром Иксиона,\n Обнимем облако и дым.\n \n Мне было тягостно и грустно,\n Что лжет улыбка и слеза,\n И то, что слышим мы изустно,\n И то, чему глядим в глаза.\n \n И я встречаю, с ним не споря,\n Спокойно ныне бытие;\n И горестней младого горя\n Мне равнодушие мое.']
        # poems[1962] = ['Грустный вид и грустный час –\n Дальний путь торопит нас...\n Вот, как призрак гробовой,\n Месяц встал – и из тумана\n Осветил безлюдный край...\n    Путь далек – не унывай...\n \n Ах, и в этот самый час,\n Там, где нет теперь уж нас,\n Тот же месяц, но живой,\n Дышит в зеркале Лемана...\n Чудный вид и чудный край –\n    Путь далек – не вспоминай...\n \n Родной ландшафт... Под дымчатым навесом\n    Огромной тучи снеговой\n Синеет даль – с ее угрюмым лесом,\n    Окутанным осенней мглой...\n Всё голо так – и пусто-необъятно\n    В однообразии немом...\n Местами лишь просвечивают пятна\n    Стоячих вод, покрытых первым льдом.\n \n Ни звуков здесь, ни красок, ни движенья –\n    Жизнь отошла – и, покорясь судьбе,\n В каком-то забытьи изнеможенья,\n    Здесь человек лишь снится сам себе.\n Как свет дневной, его тускнеют взоры,\n    Не верит он, хоть видел их вчера,\n Что есть края, где радужные горы\n    В лазурные глядятся озера...']
        # poems[1969] = ['Он, честь дворянскую ногами попирая,\n Сам родом дворянин по прихоти судьбы,\n В ворота ломится потерянного рая,\n Где грезятся ему и розги, и рабы.\n \n Все тайны – наголо! Все души – нараспашку!..\n Так люди не были правдивы никогда.\n Но можно маску снять; зачем снимать рубашку?\n Пусть лицемерья нет; зачем же нет стыда?\n Что ж! Просто ль их теснят приличные одежды?\n Иль представляются им выше наконец:\n Гонитель знания – стыдливого невежды,\n И робкого льстеца – отъявленный подлец?\n \n Друзьям бесстыдным лжи – свет правды ненавистен.\n И вот они на мысль, искательницу истин,\n Хотели б наложить молчания печать –\n И с повелением – безропотно молчать!\n \n Чернить особенно людей он честных хочет.\n Блудница трезвая, однако, не порочит\n Нахально женщину за то лишь, что она –\n И мать хорошая, и честная жена.\n Вот только где теперь встречаются примеры,\n Как и в бесстыдности блюдется чувство меры.\n \n Для творческих идей дух времени – препона;\n От лучших замыслов получится урод.\n Из мрамора резцом ваяют Аполлона,\n Но разве вылепишь его из нечистот?']
        # poems[1970] = ['Глядит эта тень, поднимаясь вдали,\n Глазами в глаза мне уныло.\n Призвали его из родной мы земли,\n Но долго заняться мы им не могли,\n      Нам некогда было.\n \n Взносились из сердца его полноты\n Напевы, как дым из кадила;\n Мы песни хвалили; но с юной мечты\n Снять узы недуга и гнет нищеты\n      Нам некогда было.\n \n Нельзя для чужих забывать же потреб\n Все то, что нам нужно и мило;\n Он дик был и странен, был горд и нелеп;\n Узнать – он насущный имеет ли хлеб,\n      Нам некогда было.\n \n Вели мы беседу, о том говоря,\n Что чувств христианских светило\n Восходит, что блещет святая заря;\n Возиться с нуждой и тоской дикаря\n      Нам некогда было.\n \n Стоял той порой он в своем чердаке,–\n Души разбивалася сила,–\n Стоял он, безумный, с веревкой в руке...\n В тот вечер спросить о больном бедняке\n      Нам некогда было.\n \n Стон тяжкий пронесся во мраке ночном.\n Есть грешная где-то могила,\n Вдали от кладбища,– на месте каком,\n Не знаю доселе; проведать о том\n      Нам некогда было.']
        # poems[1972] = ['И больно, и сладко,\n Когда, при начале любви,\n То сердце забьется украдкой,\n То в жилах течет лихорадка,\n То жар запылает в крови...\n      И больно, и сладко!..\n \n      Пробьет час свиданья,–\n Потупя предательский взор,\n В волненьи, в томленьи незнанья,\n Боясь и желая признанья,\n Начнешь и прервешь разговор...\n      И в муку свиданье!..\n \n      Не вымолвишь слова...\n Немеешь... робеешь... дрожишь...\n Душа, проклиная оковы,\n Вся в речи излиться б готова...\n Но только глядишь и молчишь –\n      Нет силы, нет слова!..\n \n      Настанет разлука,–\n И, холодно, гордо простясь,\n Уйдешь с своей тайной и мукой!..\n А в сердце истома и скука,\n И вечностью нам каждый час,\n      И смерть нам разлука!..\n \n      И сладко, и больно...\n И трепет безумный затих;\n И сердцу легко и раздольно...\n Слова полились бы так вольно,\n Но слушать уж некому их,–\n      И сладко, и больно!..']
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

        # print(poems[1426])
        # poems[1895] = ['Приближение лета отпраздновать,\nНарядилась сударыня-ноченька,'
        #                '\nОблака\xa0 свои вышила стразами.\nМимо ветер\xa0 летел неустойчивый,\n\nВидел он, как глазастая модница\nНовой тучкою запад украсила,\nТолько он не привык церемониться…\nИ раскрыл ей объятия страстные.\n\nПоиграл, не стесняясь, обновкою,\nЖался к ночке, запутывал косы ей.\nОт толчков и касаний неловкого\nПробудился фонарь под берёзою,\n\nСерой\xa0 шляпой, каймой\xa0 \xa0 отороченной,\nВсё\xa0 махал, да подмигивал весело,\nГлядя, как обнимается ноченька\nС разгулявшимся ветром-повесою.']
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
