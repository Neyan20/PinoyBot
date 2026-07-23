"""
pinoybot.py

PinoyBot: Filipino Code-Switched Language Identifier

This module provides the main tagging function for the PinoyBot project, which identifies the language of each word in a code-switched Filipino-English text. The function is designed to be called with a list of tokens and returns a list of tags ("ENG", "FIL", "CS", or "OTH").

Model training and feature extraction should be implemented in a separate script. The trained model should be saved and loaded here for prediction.
"""

import os
# import pickle
import joblib
from typing import List

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

# Main tagging function
def tag_language(tokens: List[str]) -> List[str]:
    """
    Tags each token in the input list with its predicted language.
    Args:
        tokens: List of word tokens (strings).
    Returns:
        tags: List of predicted tags ("ENG", "FIL", "CS", or "OTH"), one per token.
    """
    # 1. Load your trained model from disk (e.g., using pickle or joblib)
    #    Example: with open('trained_model.pkl', 'rb') as f: model = pickle.load(f)
    #    (Replace with your actual model loading code)

    # 2. Extract features from the input tokens to create the feature matrix
    #    Example: features = ... (your feature extraction logic here)

    # 3. Use the model to predict the tags for each token
    #    Example: predicted = model.predict(features)

    # 4. Convert the predictions to a list of strings ("ENG", "FIL", or "OTH")
    #    Example: tags = [str(tag) for tag in predicted]

    # 5. Return the list of tags
    #    return tags

    # You can define other functions, import new libraries, or add other Python files as needed, as long as
    # the tag_language function is retained and correctly accomplishes the expected task.

    # Currently, the bot just tags every token as FIL. Replace this with your more intelligent predictions.





    # 1.
    trained_model = joblib.load("trainedbot")

    # 2.
    feature_matrix = []
    for w, word in enumerate(tokens):
        feature_matrix.append(features_list(word, w))

    # 3.
    # similar to trainingbot.py, y_pred = model...
    y_pred = trained_model.predict(feature_matrix)
    return y_pred

    # 4.

    # 5.
    

    #return ['FIL' for i in tokens]

if __name__ == "__main__":
    # Example usage
    example_tokens = ["Sa", "akin", "itong", "football", "ko", "why"]
    print("Tokens:", example_tokens)
    tags = tag_language(example_tokens)
    print("Tags:", tags)

    