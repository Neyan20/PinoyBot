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
    
def is_singular_letter(word, letters):

    for l in letters:
        if l == word.lower():
            return 1
    return 0

def is_number(word, numbers):
    for a in word:
        if a not in numbers:
            return 0
    return 1

def has_number(word, numbers):
    for a2 in word:
        if a2 in numbers:
            return 1
    return 0

def find_vowel_ratio(word, vowels):
    vowel_count = 0
    
    for a3 in word:
        if a3 in vowels:
            vowel_count += 1
    
    return (vowel_count/len(word))

def count_double_vowels(word, vowels):
    cur_vowel = ' '
    dw_count = 0

    for a4 in range(len(word) - 1):
        if word[a4] in vowels:
            cur_vowel = word[a4]
            if word[a4+1] == cur_vowel:
                dw_count += 1
    
    return dw_count

def has_double_a(word):
    lower_word = word.lower()

    return "aa" in lower_word

def has_double_e(word):
    lower_word = word.lower()

    return "ee" in lower_word

def has_double_i(word):
    lower_word = word.lower()

    return "ii" in lower_word

def has_double_o(word):
    lower_word = word.lower()

    return "oo" in lower_word

def has_double_u(word):
    lower_word = word.lower()

    return "uu" in lower_word

def count_double_consonants(word, consonants):
    cur_cons = ' '
    dc_count = 0

    for a5 in range(len(word) - 1):
        if word[a5] in consonants:
            cur_cons = word[a5]
            if word[a5+1] == cur_cons:
                dc_count += 1
    return dc_count

    # two_consonants = 0
    # three_consonants = 0 #tch, thr, thy

def count_two_consonants(word, consonants):
    c2_count = 0

    for a8 in range(len(word) - 1):
        if (word[a8] in consonants) and (word[a8 + 1] in consonants):
            c2_count += 1

    return c2_count

def count_three_consonants(word, consonants):
    c3_count = 0

    for a9 in range(len(word) - 2):
        if (word[a9] in consonants) and (word[a9 + 1] in consonants) and (word[a9 + 2] in consonants):
            c3_count += 1

    return c3_count

def has_repeated_2_letter_syllables(word):
    pair2 = ' '
    for a6 in range(len(word) - 3):
        pair_2 = (word[a6] + word[a6 + 1]).lower()

        if pair_2 == (word[a6+2] + word[a6+3]):
            return 1
    return 0

def has_repeated_3_letter_syllables(word):
    trio = ' '
    for a7 in range(len(word) - 5):
        pair_1 = (word[a7] + word[a7+1] + word[a7+2]).lower()

        if pair_1 == (word[a7+3] + word[a7+4] + word[a7+5]):
            return 1
    return 0

def may_unlapi(word):
    unlapi_list = ["ma", "na", "um", "ka", "pa"]
    if ((word[0] + word[1]) in unlapi_list):
        return 1
    return 0

    # [c]um[v], [c]in[v]
def may_gitlapi(word, consonants, vowels):
    gitlapi_list = ["um", "in"]
    for a10 in range(1, len(word) - 2):
        if (((word[a10] + word[a10 + 1]) in gitlapi_list) and
            (word[a10 - 1] in consonants) and (word[a10 + 2] in vowels)):
            return 1
    return 0

def may_hulapi(word):
    hulapi_list = ["an", "in"]
    if((word[len(word) - 2] + word[len(word) - 1]) in hulapi_list):
        return 1
    return 0

    # specific_fil_sounds = 0 # ie. (ts, kw, diy[vowel], ngg)
def count_fil_sounds(word, vowel):
    two_fil_sounds = ["ts", "kw"]
    three_fil_sounds = ["diy", "ngg"]
    fil_counter = 0

def features_list(word, index):
    vowels = ['a', 'e', 'i','o' ,'u']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h',
                  'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',
                  's', 't', 'v', 'w', 'x', 'y', 'z']
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
               'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    all_caps = is_all_caps(word)
    #capitalized = 0 # if capitalized + index > 0

    #update, number = 0 if the word is multi-digit (eg "100") which is incorrect
    if len(word) == 1:
        singular_letter = is_singular_letter(word.lower(), letters)
        number = is_number(word, numbers)
    else:
        singular_letter = 0
        number = 0
    # is_symbol = 0

    # has_number = has_number(word)
    # has_symbol = 0

    vowel_ratio = find_vowel_ratio(word.lower(), vowels)
    # add double_a, double_e, double_i, double_o
    double_vowels = count_double_vowels(word.lower(), vowels)
    double_consonants = count_double_consonants(word.lower(), consonants)
    two_consonants = count_two_consonants(word.lower(), consonants)
    three_consonants = count_three_consonants(word.lower(), consonants) #tch, thr, thy

    repeated_2_letter_syllables = has_repeated_2_letter_syllables(word.lower()) # ie. dadaan, baba, lalakad
    repeared_3_letter_syllables = has_repeated_3_letter_syllables(word.lower()) # ie. basbasan, pagpagin
    # unlapi = 0 # ma, na
    # gitlapi = 0 # [c]um[v], [c]in[v]
    # hulapi = 0 # an, in
    # specific_fil_sounds = 0 # ie. (ts, kw, diy[vowel], ngg)
    # fil_diphthongs = 0 # (iw, uy, ey, oy, ay, aw)

    # prefix
    # suffix
    # specific_eng_sounds = 0 # ie. (ch, qu, ie, ph)

    return [all_caps, singular_letter, number,
            vowel_ratio, double_vowels, double_consonants, two_consonants, three_consonants,
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