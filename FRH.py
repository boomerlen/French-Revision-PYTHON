# FRH.py
# French Revision Helper main file
# Hugo Sebesta

from Classes import *

print("Hello World!")

# Testing concepts
hello = "this is a string"
newHello = hello[:-3]
print(newHello)

print("Attempting word declaration")
newWord = Word("one", "un")
newWord.commentText = "NUMBER"
print("English: " + newWord.englishDef)
print("French: " + newWord.frenchDef)
print("Comment: " + newWord.commentText)

newAdjective = Adjective("blue", "bleu", 's')
print("J'ai deux " + newAdjective.plural + " garcons")

newNoun = Noun("house", "MAISON", "s", Feminine)
print(newNoun.gender)
print("Je vais retourner aux " + newNoun.plural)
