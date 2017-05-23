import csv
from measurer import Measurer


filename1 = 'test-words-to-evaluate.csv'
filename2 = 'test-words.csv'

def get_words(file_):
    words = []
    with open(file_, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            word1, word2 = row
            words.append([word1, word2],)
    return words

def write_words(filename, word_pairs):
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for word_pair in word_pairs:
            spamwriter.writerow(word_pair)

measur = Measurer()

words = get_words(filename1)
words = words[1:]
print(len(words))

measured_words = []
measured_words.append(['word1', 'word2', 'sim'])
for w1, w2 in words:
    measure = measur.get_measure(w1, w2)
    #if measure == -1:
    #    continue
    measured_words.append([w1, w2, measure])

write_words(filename2, measured_words)

