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
    
def is_singular_letter(word, letters):

    for l in letters:
        if l == word:
            return 1
    return 0

def is_number(word, numbers):
    for a in word:
        if a not in numbers:
            return 0
    return 1

def has_number(word, numbers):
    for a in word:
        if a in numbers:
            return 1
    return 0

def find_symbol_ratio(word, letters, numbers):
    count = 0

    for a in word:
        if ((a not in letters) and (a not in numbers)):
            count += 1

    return (count/len(word))


def find_vowel_ratio(word, vowels):
    vowel_count = 0
    
    for a in word:
        if a in vowels:
            vowel_count += 1
    
    return (vowel_count/len(word))

def count_double_vowels(word, vowels):
    cur_vowel = ' '
    dw_count = 0

    for a in range(len(word) - 1):
        if word[a] in vowels:
            cur_vowel = word[a]
            if word[a+1] == cur_vowel:
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

    for a in range(len(word) - 1):
        if word[a] in consonants:
            cur_cons = word[a]
            if word[a+1] == cur_cons:
                dc_count += 1
    return dc_count

    # two_consonants = 0
    # three_consonants = 0 #tch, thr, thy

def count_two_consonants(word, consonants):
    c2_count = 0

    for a in range(len(word) - 1):
        if (word[a] in consonants) and (word[a + 1] in consonants):
            c2_count += 1

    return c2_count

def count_three_consonants(word, consonants):
    c3_count = 0

    for a in range(len(word) - 2):
        if (word[a] in consonants) and (word[a + 1] in consonants) and (word[a + 2] in consonants):
            c3_count += 1

    return c3_count

def has_repeated_2_letter_syllables(word):
    pair2 = ' '
    for a in range(len(word) - 3):
        pair = (word[a] + word[a + 1])

        if pair == (word[a+2] + word[a+3]):
            return 1
    return 0

def has_repeated_3_letter_syllables(word):
    trio = ' '
    for a in range(len(word) - 5):
        pair = (word[a] + word[a+1] + word[a+2])

        if pair == (word[a+3] + word[a+4] + word[a+5]):
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
    for a in range(1, len(word) - 2):
        if (((word[a] + word[a + 1]) in gitlapi_list) and
            (word[a - 1] in consonants) and (word[a + 2] in vowels)):
            return 1
    return 0

def may_hulapi(word):
    hulapi_list = ["an", "in"]
    if((word[len(word) - 2] + word[len(word) - 1]) in hulapi_list):
        return 1
    return 0

    # specific_fil_sounds = 0 # ie. (ts, kw, diy[vowel], ngg)
def count_fil_sounds(word):
    two_fil_sounds = ["ts", "kw", "ks",
                      "iw", "uy", "ey", "oy", "ay", "aw"]
    three_fil_sounds = ["diy", "ngg",
                        "ala", "san", "isa", "ito", "ama", "ila", "pag", "ara", "ata", "kan", "ali"]
    two_fil_counter = 0
    thr_fil_counter = 0

    if(len(word) > 2):
        for a in range(len(word) - 2):
            if((word[a] + word[a+1]) in two_fil_sounds):
                two_fil_counter += 1

    if(len(word) > 3): 
        for b in range(len(word) - 3):
            if((word[b] + word[b+1] + word[b+2]) in three_fil_sounds):
                thr_fil_counter += 1

    return two_fil_counter, thr_fil_counter

def count_eng_letters(word):
    eng_letters = ['c', 'f', 'j', 'q', 'v', 'x', 'z']
    count = 0

    for a in word:
        if a in eng_letters:
            count += 1
    return count

def count_eng_sounds(word):
    count = 0
    eng_sounds = ["ch", "qu", "ie", "ph"]

    if (len(word) > 2):
        for a in range(len(word) - 1):
            if ((word[a] + word[a+1]) in eng_sounds):
                count += 1

    return count

def has_eng_prefix(word):
    prefixes_2l = ["en", "em", "in", "im", "re", "un"]
    prefixes_3l = ["dis", "mid", "mis", "sub"]

    if (((word[0] + word[1]) in prefixes_2l) or
        ((word[0] + word[1] + word[2]) in prefixes_3l)):
        return 1
    return 0

def has_eng_suffix(word):
    suffixes_2l = ["ed", "er", "en", "ic", "ty"]

    if ((word[len(word) - 1] + word[len(word) - 2]) in suffixes_2l):
        return 1
    return 0

def features_list(word, index):
    vowels = ['a', 'e', 'i','o' ,'u']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h',
                  'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',
                  's', 't', 'v', 'w', 'x', 'y', 'z']
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
               'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    # length = len(word)
    all_caps = is_all_caps(word)
    #capitalized = 0 # if capitalized + index > 0

    #update, number = 0 if the word is multi-digit (eg "100") which is incorrect
    number = is_number(word, numbers)
    if len(word) == 1:
        singular_letter = is_singular_letter(word.lower(), letters)

        if (singular_letter == 1) or (number == 1):
            is_symbol = 0
        else:
            is_symbol = 1
    else:
        singular_letter = 0
        is_symbol = 0
    # is_symbol = 0

    # has_number = has_number(word)
    symbol_ratio = find_symbol_ratio(word, letters, numbers)

    vowel_ratio = find_vowel_ratio(word.lower(), vowels)

    # add double_a, double_e, double_i, double_o
    if(len(word) >= 2):
        double_vowels = count_double_vowels(word.lower(), vowels)
        double_consonants = count_double_consonants(word.lower(), consonants)
        two_consonants = count_two_consonants(word.lower(), consonants)
    else:
        double_vowels = double_consonants = two_consonants = 0

    if(len(word) >= 3):
        three_consonants = count_three_consonants(word.lower(), consonants) #tch, thr, rst
    else:
        three_consonants = 0

    if(len(word) >= 4):
        repeated_2_letter_syllables = has_repeated_2_letter_syllables(word.lower()) # ie. dadaan, baba, lalakad
    else:
        repeated_2_letter_syllables = 0

    if(len(word) >= 6):
        repeated_3_letter_syllables = has_repeated_3_letter_syllables(word.lower()) # ie. basbasan, pagpagin
    else:
        repeated_3_letter_syllables = 0

    if (len(word) >= 3):
        unlapi = may_unlapi(word.lower()) # ma, na
        hulapi = may_hulapi(word.lower()) # an, in
    else:
        unlapi = 0
        hulapi = 0

    if (len(word) >= 4):
        gitlapi = may_gitlapi(word.lower(), consonants, vowels)
    else:
        gitlapi = 0

    fil_sound_pair, fil_sound_trio = count_fil_sounds(word.lower())
    # specific_fil_sounds = 0 # ie. (ts, kw, diy[vowel], ngg)
    # fil_diphthongs = 0 # (iw, uy, ey, oy, ay, aw)
    # done

    specific_eng_letters = count_eng_letters(word.lower()) # c, f, j, q, v, x, z
    specific_eng_sounds = count_eng_sounds(word.lower())
    
    eng_prefix = has_eng_prefix(word.lower())
    eng_suffix = has_eng_suffix(word.lower())

    return [all_caps, singular_letter, number, is_symbol,
            symbol_ratio, vowel_ratio,
            double_vowels, #double_a, double_e, double_i, double_o, double_u
            double_consonants, two_consonants, three_consonants,
            repeated_2_letter_syllables, repeated_3_letter_syllables,
            unlapi, gitlapi, hulapi, fil_sound_pair, fil_sound_trio,
            specific_eng_letters, specific_eng_sounds, eng_prefix, eng_suffix]

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

    # 4/5.
    return y_pred
    #return ['FIL' for i in tokens]

if __name__ == "__main__":
    # Example usage
    example_tokens = ["Sa", "akin", "itong", "football", "ko", "why"]
    print("Tokens:", example_tokens)
    tags = tag_language(example_tokens)
    print("Tags:", tags)

    