"""
pinoybot.py

PinoyBot: Filipino Code-Switched Language Identifier

This module provides the main tagging function for the PinoyBot project, which identifies the language of each word in a code-switched Filipino-English text. The function is designed to be called with a list of tokens and returns a list of tags ("ENG", "FIL", "CS", or "OTH").

Model training and feature extraction should be implemented in a separate script. The trained model should be saved and loaded here for prediction.
"""

import os
import pickle
from typing import List

def is_all_caps(word):
    if (word.upper() == word):
        return 1
    return 0

def is_capitalized_midway(word):
    if(word[0].upper() == word[0]):
        return 1
    return 0
    


def find_vowel_ratio(word):
    vowels = ['a', 'e', 'i','o' ,'u']
    vowel_count = 0
    
    for a in word:
        if a in vowels:
            vowel_count += 1
    
    return (vowel_count/len(word))

def has_double_vowels(word):
    vowels = ['a', 'e', 'i','o' ,'u']
    cur_vowel = ' '

    for b in range(len(word) - 1):
        if word[b] in vowels:
            cur_vowel = word[b]
            if word[b+1] == cur_vowel:
                return 1
    
    return 0

def features_list(word, index):
    all_caps = 0
    capitalized = 0 # if capitalized + index > 0

    singular_letter = 0
    is_symbol = 0
    has_symbol = 0

    vowel_ratio = find_vowel_ratio(word)
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
    return ['FIL' for i in tokens]

if __name__ == "__main__":
    # Example usage
    example_tokens = ["Love", "kita", "."]
    print("Tokens:", example_tokens)
    tags = tag_language(example_tokens)
    print("Tags:", tags)

