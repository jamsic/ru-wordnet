from wiki_ru_wordnet import Wordnet
import numpy as np


class Measurer:

    def __init__(self):
        self.wordn = Wordnet()

    def get_measure(self, w1, w2):
        synsets1 = self.wordn.get_synsets(w1)
        synsets2 = self.wordn.get_synsets(w2)
        #print(w1, w2)
        #print(w1, w2, synsets1, synsets2)
        #if not synsets1 or not synsets2:
        #    return -1
        most_close_measure = 10000
        for s1 in synsets1:
            for s2 in synsets2:
                hypers = self.wordn.common_hyperonyms(s1, s2)
                if hypers:
                    for h, dst_to_first, dst_to_scnd in hypers:
                        if most_close_measure > dst_to_first + dst_to_scnd:
                            most_close_measure = dst_to_first + dst_to_scnd
        return np.exp(-most_close_measure)

def are_in_same_synset(m, w1, w2):
    synsets1 = m.wordn.get_synsets(w1)
    synsets2 = m.wordn.get_synsets(w2)
    for s in synsets1:
        if w2 in m.wordn.get_synwords(s):
            return True
    for s in synsets2:
        if w1 in m.wordn.get_synwords(s):
            return True
    return False

def is_hyper(m, w1, w2):
    synsets = m.wordn.get_synsets(w1)
    for s in synsets:
        hyperonyms = m.wordn.get_hyperonyms(s)
        for h in hyperonyms:
            print(m.wordn.get_synwords(h))
    synsets1 = m.wordn.get_synsets(w1)
    synsets2 = m.wordn.get_synsets(w2)
    most_close_measure = 10000
    for s1 in synsets1:
        for s2 in synsets2:
            hypers = m.wordn.common_hyperonyms(s1, s2)
            if hypers:
                print(s1, s2)
                for h, dst_to_first, dst_to_scnd in hypers:
                    if most_close_measure > dst_to_first + dst_to_scnd:
                        most_close_measure = dst_to_first + dst_to_scnd
                    print(h, dst_to_first, dst_to_scnd)
                    print(m.wordn.get_synwords(h))
    print(most_close_measure, 1 / (1+most_close_measure), np.exp(-most_close_measure), 1 - np.exp(-most_close_measure))

if __name__ == '__main__':
    print('main')
    m = Measurer()
    w1, w2 = 'собака', 'пёс'
    #w1, w2 = 'собака', 'животное'
    #w1, w2 = 'бакс', 'доллар'
    print(are_in_same_synset(m, w1, w2))
    print(is_hyper(m, w1, w2))

    vals = [0,1,2,3,4,5,6,7,8]
    for val in vals:
        print(val, np.exp(-val), np.log(1+val), 1/(1+np.log(1+val)), np.exp(-val/4))
