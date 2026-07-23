import csv
import joblib

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
# from sklearn.naive_bayes import MultinomialNB

def is_all_caps(word):
    if (word.upper() == word):
        return 1
    return 0

def is_capitalized_midway(word):
    if(word[0].upper() == word[0]):
        return 1
    return 0
    
def is_singular_letter(word):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
               'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for l in letters:
        if l == word.lower():
            return 1
    return 0

def is_number(word):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for a in word:
        if a not in numbers:
            return 0
    return 1

def has_number(word):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for b in word:
        if b in numbers:
            return 1
    return 0


def find_vowel_ratio(word):
    vowels = ['a', 'e', 'i','o' ,'u']
    vowel_count = 0
    
    for c in word:
        if c in vowels:
            vowel_count += 1
    
    return (vowel_count/len(word))

def count_double_vowels(word):
    vowels = ['a', 'e', 'i','o' ,'u']
    cur_vowel = ' '
    dw_count = 0

    for d in range(len(word) - 1):
        if word[d] in vowels:
            cur_vowel = word[d]
            if word[d+1] == cur_vowel:
                dw_count += 1
    
    return dw_count

def count_double_consonants(word):
    consonants = ['b', 'c', 'd', 'f', 'g', 'h',
               'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',
               's', 't', 'v', 'w', 'x', 'y', 'z']

    cur_cons = ' '
    dc_count = 0

    for e in range(len(word) - 1):
        if word[e] in consonants:
            cur_cons = word[e]
            if word[e+1] == cur_cons:
                dc_count += 1
    return dc_count

def has_repeated_2_letter_syllables(word):
    pair = ' '
    for f in range(len(word) - 3):
        pair_1 = (word[f] + word[f + 1]).lower()

        if pair_1 == (word[f+2] + word[f+3]):
            return 1
    return 0

def has_repeated_3_letter_syllables(word):
    trio = ' '
    for g in range(len(word) - 5):
        pair_1 = (word[g] + word[g+1] + word[g+2]).lower()

        if pair_1 == (word[g+3] + word[g+4] + word[g+5]):
            return 1
    return 0

def has_unlapi(word):
    return 0

def has_gitlapi(word):
    return 0

def has_hulapi(word):
    return 0

def features_list(word, index):
    all_caps = is_all_caps(word)
    #capitalized = 0 # if capitalized + index > 0

    if len(word) == 1:
        singular_letter = is_singular_letter(word)
        number = is_number(word)
    else:
        singular_letter = 0
        number = 0
    # is_symbol = 0

    # has_number = has_number(word)
    # has_symbol = 0

    vowel_ratio = find_vowel_ratio(word)
    double_vowels = count_double_vowels(word)
    double_consonants = count_double_consonants(word)
    # two_consonants = 0
    # three_consonants = 0 #tch, thr, thy

    repeated_2_letter_syllables = has_repeated_2_letter_syllables(word) # ie. dadaan, baba, lalakad
    repeared_3_letter_syllables = has_repeated_3_letter_syllables(word) # ie. basbasan, pagpagin
    # unlapi = 0 # ma, na
    # gitlapi = 0 # [c]um[v], [c]in[v]
    # hulapi = 0 # an, in
    # specific_fil_sounds = 0 # ie. (ts, kw, diy[vowel], ngg)
    # fil_diphthongs = 0 # (iw, uy, ey, oy, ay, aw)

    # specific_eng_sounds = 0 # ie. (ch, qu, ie, ph)

    return [all_caps, singular_letter, number,
            vowel_ratio, double_vowels, double_consonants,
            repeated_2_letter_syllables, repeared_3_letter_syllables]

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

# feature matrix
feature_matrix = []

for w, word in enumerate(words):
    feature_matrix.append(features_list(word, w))

fw = 0
for fm in feature_matrix:
    print(words[fw], fm)
    fw += 1

# 70 15 15
# X_train - selected feature rows, y_train - corresponding tags, X/y_vt - unselected
# X/y_valid - validation, X/y_test - test
X_train, X_vt, y_train, y_vt = train_test_split(feature_matrix, tags, test_size = 0.3)
X_valid, X_test, y_valid, y_test = train_test_split(X_vt, y_vt, test_size = 0.5)

# gnb - train model - multinombialNB
model = GaussianNB()
# y_pred
# y_pred = model.fit(X_train, y_train).predict(X_valid)
model.fit(X_train, y_train) # train the model
y_pred = model.predict(X_valid) # test model

print(y_pred) # predicted
print(y_valid) # actual

# export model
joblib.dump(model, "trainedbot")