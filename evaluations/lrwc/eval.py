import wiki_ru_wordnet

wordn = wiki_ru_wordnet.WikiWordnet()

test_filename = 'lrwc-1.1-aggregated.tsv'

def is_hyp(wordnet, ssa, ssb):
    for a in ssa:
        for b in ssb:
            common_hypernyms = wordn.get_common_hypernyms(a, b, max_level=10)
            for ch, da, db in common_hypernyms:
                if not db:
                    return True
    return False

tp, tn, fp, fn = 0,0,0,0

results = []
with open(test_filename) as handle:
    for line in handle:
        a, b, *rest, ans, rel = line.split()
        ans = True if ans == 'true' else False
        try:
            ssa = wordn.get_synsets(a)
            ssb = wordn.get_synsets(b)
        except Exception as e:
            ssa = None
            ssb = None
        if ssa and ssb:
           ans2 = is_hyp(wordn, ssa, ssb) or is_hyp(wordn, ssb, ssa)
           if ans == ans2 and ans:
               tp += 1
           if ans == ans2 and not ans:
               tn += 1
           if ans != ans2 and ans:
               fn += 1
           if ans != ans2 and not ans:
               fp += 1
           results.append((a, b, ans, ans2),)
print(tp, fp, tn, fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
fmeasure = 2 * precision * recall / (precision + recall)
accuracy = (tp + tn) / (tp+tn+fp+fn)
print(precision, recall, fmeasure, accuracy)

