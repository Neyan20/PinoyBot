import csv

from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import GaussianNB
# from sklearn.naive_bayes import MultinomialNB

def features_list(word, index):
    all_caps = 0
    capitalized = 0 # if capitalized + index > 0

    singular_letter = 0
    is_symbol = 0
    has_symbol = 0

    vowel_ratio = 0
    double_vowels = 0
    double_consonants = 0

    repeated_syllables = 0 # ie. dadaan, baba, lalakad
    ngg = 0 # remove, is in specific_fil_sounds
    unlapi = 0
    gitlapi = 0 # um[vowel]
    hulapi = 0
    specific_fil_sounds = 0 # ie. (ts, ngg, diy[vowel])
    specific_eng_sounds = 0 # ie. (ch, qu, ie)

    return [word, vowel_ratio, double_vowels]

# read file
sentence = []
words = []
tags = []

with open("dataset.csv", "r") as f:
    data = csv.reader(f)

    next(data)
    for row in data:
        # print(row)
        words.append(row[3])
        tags.append(row[4])

# convert the words into a sample matrix
feature_matrix = []

for word_no in range(len(words)):
    feature_matrix.append(features_list(words[word_no], word_no))

print(feature_matrix)

# 70 15 15
# train_test_split(feature_matrix, tags)

# gnb - train model
