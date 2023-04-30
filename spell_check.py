import pandas as pd
from spellchecker import SpellChecker


def Correct(excel, column):
    specific_column = excel[column]
    
    spell = SpellChecker(distance=1)
    return spell.correction(x)