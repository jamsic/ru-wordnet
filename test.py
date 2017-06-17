from wiki_ru_wordnet import Wordnet

wordn = Wordnet()

word = 'медведь'
words = wordn.get_words(word)
# все значения слова
for w in words:
    print(w.word)
    print(w.meaning)
# все синсеты, содержащие слово
synsets = wordn.get_synsets(word)
# гиперонимы и гипонимы для каждого
for synset in synsets:
    print('синсет: ', wordn.get_synwords(synset))
    hyperonyms = wordn.get_hyperonyms(synset)
    for h in hyperonyms:
        print('гипероним:\t', h.id, wordn.get_synwords(h))
    hyponyms = wordn.get_hyponyms(synset)
    for h in hyponyms:
        print('гипоним:\t\t\t', h.id, wordn.get_synwords(h))
    if not hyperonyms and not hyponyms:
        print('\t', 'у этого синсета нет ни гиперонимов, ни гипонимов')

# общий ближайший гипероним (если несколько, возвращаются все)
sid1 = 35791
sid2 = 34927
synset1 = wordn.get_synset_by_id(sid1)
synset2 = wordn.get_synset_by_id(sid2)
hyps = wordn.common_hyperonyms(synset1, synset2)
print('общие гиперонимы {0} и {1}:'.format(wordn.get_synwords(synset1),
                                           wordn.get_synwords(synset2)))
for hyperonym, dist_to_fst, dist_to_scd in hyps:
    print(dist_to_fst, dist_to_scd, wordn.get_synwords(hyperonym))

# общий ближайший гипоним (если несколько, возвращаются все)
sid1 = 7368
sid2 = 1644
synset1 = wordn.get_synset_by_id(sid1)
synset2 = wordn.get_synset_by_id(sid2)
hyps = wordn.common_hyponyms(synset1, synset2)
print('общие гипонимы {0} и {1}:'.format(wordn.get_synwords(synset1),
                                           wordn.get_synwords(synset2)))
for hyponym, dist_to_fst, dist_to_scd in hyps:
    print(dist_to_fst, dist_to_scd, wordn.get_synwords(hyponym))

