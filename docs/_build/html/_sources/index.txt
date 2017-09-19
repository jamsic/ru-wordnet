.. wiki-ru-wordnet documentation master file, created by
   sphinx-quickstart on Tue Sep 19 19:04:38 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

wiki-ru-wordnet документация
============================

wiki-ru-wordnet -- это семантическая сеть типа WordNet для русского языка, составленная из данных русского Викисловаря (https://ru.wiktionary.org/).

Она умеет:

1. выдавать синсеты, содержащие заданное слово;

2. выдавать гиперонимы и гипонимы заданных синсетов;

3. искать общие гиперонимы и гипонимы для двух синсетов.

Распространяется по лицензии MIT.


.. toctree::
   :maxdepth: 2

Установка
---------

Для установки воспользуйтесь pip::

    pip install wiki-ru-wordnet

Код писался на python3.4, но скорее всего совместим и с python2.

Получение синсетов
------------------

Модуль состоит из единственного класса :class:`WikiWordnet`
::

    >>> from wiki_ru_wordnet import WikiWordnet
    >>> wikiwordnet = WikiWordnet()

Объект этого класса подгружает в память сразу всю лексическую базу и требует порядка 150Мб, поэтому будьте бдительны, пожалуйста.

Синсет -- это множество слов, объединенных одним смыслом (синонимов). С помощью метода :meth:`WikiWordnet.get_synsets` можно получить все синсеты, содержащие заданное слово:

    >>> wikiwordnet.get_synsets('медведь')
    [<wiki_ru_wordnet.synset.Synset at 0x7f3d25ff66d8>,
     <wiki_ru_wordnet.synset.Synset at 0x7f3d25ff6710>,
     <wiki_ru_wordnet.synset.Synset at 0x7f3d25ff6748>]

Объект :class:`Synset` хранит в себе множество слов, входящих в синсет, которые можно получить с помощью метода `Synset.get_words`:

    >>> synsets = wikiwordnet.get_synsets('медведь')
    >>> synset1 = synsets[0]
    >>> synset1.get_words()
    {<wiki_ru_wordnet.word.Word at 0x7f3d2a3f2cf8>, 
     <wiki_ru_wordnet.word.Word at 0x7f3d28f7beb8>, 
     <wiki_ru_wordnet.word.Word at 0x7f3d29014128>, 
     <wiki_ru_wordnet.word.Word at 0x7f3d28e18c88>}

Объект класса :class:`Word` хранит у себя слово и его значение, которое оно принимает в данном синсете. Их можно получить методами :meth:`Word.lemma` и :meth:`Word.definition` соответственно. Например, чтобы наконец получить синонимы из синсета:

    >>> for w in synset1.get_words():
    >>>     print(w.lemma())
        медведь
        топтыгин
        мишка
        косолапый

или узнать значения значения слов в оставшихся синсетах (первый, очевидно, про животное):

    >>> for synset in synsets[1:]:
    >>>     print({w.definition() for w in synset.get_words()})
        {'медведь~ru~медведь~ru~{{п.|ru}} сильный и крупный, но неуклюжий человек {{пример}}~30488~17082'}
        {'медведь~ru~медведь~ru~{{п.|ru}}, {{бирж.|ru}} участник фондового рынка, играющий на понижение котировок акций {{пример|{{выдел|Медведи}} продают акции с расчётом выкупить их потом подешевле, или просто продают, чтобы зафиксировать уже полученную прибыль.}}~45855~20502'}

Определения взяты полностью из Викисловаря, но могут не всегда совпадать с его текущей онлайн-версией.

Получение гиперонимов и гипонимов
---------------------------------

Для получения гиперонимов (более общих сущностей) и гипонимов (частных сущностей) заданного синсета (не слова!) можно воспользоваться методами :meth:`WikiWordnet.get_hypernyms` и :meth:`WikiWordnet.get_hyponyms`. Оба этих метода принимают в качестве аргумента синсет:

   >>> for hypernym in wikiwordnet.get_hypernyms(synset1):
   >>>     print({w.lemma() for w in hypernym.get_words()})
       {'хищник'}
       {'зверь', 'млекопитающее'}

   >>> for hyponym in wikiwordnet.get_hyponyms(synset1):
   >>>     print({w.lemma() for w in hyponym.get_words()})
       {'медвежонок'}
       {'панда'}
       {'коала'}
       {'шатун'}
       {'гризли'}
       {'белый медведь'}
       {'губач'}
       {'петун'}

Стоит отметить, что эти методы возвращают гиперонимы и гипонимы только первого уровня, то есть ближайшие. Это значит, что для того, чтобы получить _нимы более высокого уровня, нужно вызывать соответствующие функции рекурсивно.

Получение общих гиперонимов и гипонимов
---------------------------------------

Для получения общих гиперонимов и гипонимов можно воспользоваться методами :meth:`WikiWordnet.get_common_hypernyms` и :meth:`WikiWordnet.get_common_hyponyms`, которые принимают в качестве аргументов 2 синсета и возвращают список из кортежей (synset, dist1, dist2), где synset -- объект класса :class:`Synset`, общий гипероним или гипоним, а dist1 и dist2 -- расстояние от synset1 и synset2 до synset в графе:

    >>> synset2 = wikiwordnet.get_synsets('горилла')[0]
    >>> common_hypernyms = wikiwordnet.get_common_hypernyms(synset1, synset2)
    >>> for ch, dst1, dst2 in sorted(common_hypernyms, key=lambda x: x[1] + x[2]):
    >>>     print({c.lemma() for c in ch.get_words()}, dst1 + dst2)
        {'млекопитающее', 'зверь'} 5
        {'позвоночное'} 6
        {'животное'} 8
        {'живот'} 9
        {'существо', 'создание'} 10
        {'скот', 'животное', 'тварь', 'животина'} 11

Да, у слова "живот" есть значение "животное":)

С помощью методов :meth:`WikiWordnet.get_lowest_common_hypernyms` и :meth:`WikiWordnet.get_lowest_common_hyponyms` можно забрать ближайшие гиперонимы или гипонимы двух синсетов:

    >>> synset2 = wikiwordnet.get_synsets('горилла')[0]
    >>> common_hypernyms = wikiwordnet.get_lowest_common_hypernyms(synset1, synset2)
    >>> for ch, dst1, dst2 in sorted(common_hypernyms, key=lambda x: x[1] + x[2]):
    >>>     print({c.lemma() for c in ch.get_words()}, dst1 + dst2)
        {'млекопитающее', 'зверь'} 5


   >>> synset2 = wikiwordnet.get_synsets('детёныш')[0]
   >>> common_hyponyms = wikiwordnet.get_lowest_common_hyponyms(synset1, synset2)
   >>> for ch, dst1, dst2 in sorted(common_hyponyms, key=lambda x: x[1] + x[2]):
   >>>     print({c.lemma() for c in ch.get_words()}, dst1 + dst2)
       {'медвежонок'} 2
       {'петун'} 2

Поддержка
---------

По всем вопросам можно писать на почту jamsic@yandex.ru

Исходный код выложен в открытый доступ на Github: https://github.com/jamsic/ru-wordnet

