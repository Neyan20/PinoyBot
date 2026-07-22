import csv

from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import GaussianNB
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

def has_double_vowels(word):
    vowels = ['a', 'e', 'i','o' ,'u']
    cur_vowel = ' '

    for d in range(len(word) - 1):
        if word[d] in vowels:
            cur_vowel = word[d]
            if word[d+1] == cur_vowel:
                return 1
    
    return 0

def features_list(word, index):
    all_caps = 0
    capitalized = 0 # if capitalized + index > 0

    singular_letter = 0
    is_number = 0
    has_number = 0
    is_symbol = 0
    has_symbol = 0

    vowel_ratio = 0
    double_vowels = 0
    double_consonants = 0

    repeated_2_letter_syllables = 0 # ie. dadaan, baba, lalakad
    repeared_3_letter_syllables = 0 # ie. basbasan, pagpagin
    ngg = 0 # remove, is in specific_fil_sounds
    unlapi = 0 # ie. ma
    gitlapi = 0 # um[vowel]
    hulapi = 0 # ie. an, in
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
