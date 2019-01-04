# FRH.py
# French Revision Helper main file
# Hugo Sebesta

# External modules for import:
import MySQLdb

# My modules for import:
# Classes imports the following classes:
# Word - Generic Word class
# Adjective - Adjective Word class
# Noun - Noun Word class
# Misc - Misc Word Class
# Verb - Verb Word Class (Also contains autoConjugate method for automatically conjugating verbs for various included tenses)
# Rule - Grammar rule class
# The following enum replacing classes:
# IRVerb, ERVerb, REVerb, IrregularVerb
# Masculine, Feminine, Plural
# The following functions returning ints
# JE (0), TU (1), ON (2), NOUS (3), VOUS (4), ILS (5)
from Classes import *


# Testing Stuff:
#print("Hello World!")

# Testing concepts
# newHello = hello[:-3]
# print(newHello)

# print("Attempting word declaration")
# newWord = Word("one", "un")
# newWord.commentText = "NUMBER"
# print("English: " + newWord.englishDef)
# print("French: " + newWord.frenchDef)
# print("Comment: " + newWord.commentText)

# newAdjective = Adjective("blue", "bleu", 's')
# print("J'ai deux " + newAdjective.plural + " garcons")

# newNoun = Noun("house", "MAISON", "s", Feminine)
# print(newNoun.gender)
# print("Je vais retourner aux " + newNoun.plural)
