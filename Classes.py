# Classes.py
# Module containing all classes used in this project declared by me
# Hugo Sebesta

# Typedef Classes and Funcs:

class VerbType: pass

class IRVerb(VerbType): pass
class ERVerb(VerbType) : pass
class REVerb(VerbType) : pass
class IrregularVerb(VerbType) : pass

class WordGender: pass
class Masculine(WordGender) : pass
class Feminine(WordGender) : pass
class Plural(WordGender) : pass

def JE(): # needs to be a (enum) func because it needs to be used to dereference lists
    return 0
def TU():
    return 1
def ON():
    return 2
def NOUS():
    return 3
def VOUS():
    return 4
def ILS():
    return 5

# General Classes:

class Word:
    'Common base class for all Words'
    englishDef = ''
    frenchDef = ''
    commentText = ''

    def __init__(self, english, french):
        self.englishDef = english.lower()
        self.frenchDef = french.lower()

class Verb (Word):
    'Class for the verb word subset'
    verbType = IrregularVerb
    isReflexive = False
    pastParticiple = ''
    presentConjugation = []
    imparfaitConjugation = []
    futureSimpleConjugation = []
    usesEtreInPasseCompose = False

    def __init__(self, english, french, type = IrregularVerb, reflexive = False):
        self.englishDef = english.lower()
        self.frenchDef = french.lower()
        self.verbType = type
        self.isReflexive = reflexive

    def autoConjugate(self, etre = False):
        'Automatically conjugates REGULAR verbs based on their type. NOTE: You must fix members that are irregular for specific tenses if the conjugation is regular in present tense'
        if self.verbType == IrregularVerb: # Make sure its not irregular
            return 'CANNOT AUTOCONJUGATE IRREGULAR VERB'
        elif self.verbType == ERVerb or self.frenchDef.endswith('er'): # Verb is ER
            verbStem = self.frenchDef[:-2]
            self.presentConjugation[JE()] = verbStem + 'e'
            self.presentConjugation[TU()] = verbStem + 's'
            self.presentConjugation[ON()] = verbStem + 'e'
            self.presentConjugation[NOUS()] = verbStem + 'ons'
            self.presentConjugation[VOUS()] = verbStem + 'ez'
            self.presentConjugation[ILS()] = verbStem + 'ent'

            imparfaitVerbStem = verbStem
            self.imparfaitConjugation[JE()] = imparfaitVerbStem + 'ais'
            self.imparfaitConjugation[TU()] = imparfaitVerbStem + 'ais'
            self.imparfaitConjugation[ON()] = imparfaitVerbStem + 'ait'
            self.imparfaitConjugation[NOUS()] = imparfaitVerbStem + 'ions'
            self.imparfaitConjugation[VOUS()] = imparfaitVerbStem + 'iez'
            self.imparfaitConjugation[ILS()] = imparfaitVerbStem + 'aient'

            self.pastParticiple = verbStem + 'é'

            self.futureSimpleConjugation[JE()] = self.frenchDef + 'ai'
            self.futureSimpleConjugation[TU()] = self.frenchDef + 'as'
            self.futureSimpleConjugation[ON()] = self.frenchDef + 'a'
            self.futureSimpleConjugation[NOUS()] = self.frenchDef + 'ons'
            self.futureSimpleConjugation[VOUS()] = self.frenchDef + 'ez'
            self.futureSimpleConjugation[ILS()] = self.frenchDef + 'ont'
        elif self.verbType == IRVerb or self.frenchDef.endswith('ir'): # Verb is IR
            verbStem = self.frenchDef[:-2]
            self.presentConjugation[JE()] = verbStem + 'is'
            self.presentConjugation[TU()] = verbStem + 'is'
            self.presentConjugation[ON()] = verbStem + 'it'
            self.presentConjugation[NOUS()] = verbStem + 'issons'
            self.presentConjugation[VOUS()] = verbStem + 'issez'
            self.presentConjugation[ILS()] = verbStem + 'issent'

            imparfaitVerbStem = self.presentConjugation[NOUS()][:-3]
            self.imparfaitConjugation[JE()] = imparfaitVerbStem + 'ais'
            self.imparfaitConjugation[TU()] = imparfaitVerbStem + 'ais'
            self.imparfaitConjugation[ON()] = imparfaitVerbStem + 'ait'
            self.imparfaitConjugation[NOUS()] = imparfaitVerbStem + 'ions'
            self.imparfaitConjugation[VOUS()] = imparfaitVerbStem + 'iez'
            self.imparfaitConjugation[ILS()] = imparfaitVerbStem + 'aient'

            self.pastParticiple = verbStem + 'i'

            self.futureSimpleConjugation[JE()] = self.frenchDef + 'ai'
            self.futureSimpleConjugation[TU()] = self.frenchDef + 'as'
            self.futureSimpleConjugation[ON()] = self.frenchDef + 'a'
            self.futureSimpleConjugation[NOUS()] = self.frenchDef + 'ons'
            self.futureSimpleConjugation[VOUS()] = self.frenchDef + 'ez'
            self.futureSimpleConjugation[ILS()] = self.frenchDef + 'ont'
        elif self.verbType == REVerb or self.frenchDef.endswich('re'): # Verb is RE
            verbStem = self.frenchDef[:-2]
            self.presentConjugation[JE()] = verbStem + 's'
            self.presentConjugation[TU()] = verbStem + 's'
            self.presentConjugation[ON()] = verbStem
            self.presentConjugation[NOUS()] = verbStem + 'ons'
            self.presentConjugation[VOUS()] = verbStem + 'sez'
            self.presentConjugation[ILS()] = verbStem + 'ent'

            imparfaitVerbStem = verbStem
            self.imparfaitConjugation[JE()] = imparfaitVerbStem + 'ais'
            self.imparfaitConjugation[TU()] = imparfaitVerbStem + 'ais'
            self.imparfaitConjugation[ON()] = imparfaitVerbStem + 'ait'
            self.imparfaitConjugation[NOUS()] = imparfaitVerbStem + 'ions'
            self.imparfaitConjugation[VOUS()] = imparfaitVerbStem + 'iez'
            self.imparfaitConjugation[ILS()] = imparfaitVerbStem + 'aient'

            self.pastParticiple = verbStem + 'u'

            futureStem = self.frenchDef[:-1]
            self.futureSimpleConjugation[JE()] = futureStem + 'ai'
            self.futureSimpleConjugation[TU()] = futureStem + 'as'
            self.futureSimpleConjugation[ON()] = futureStem + 'a'
            self.futureSimpleConjugation[NOUS()] = futureStem + 'ons'
            self.futureSimpleConjugation[VOUS()] = futureStem + 'ez'
            self.futureSimpleConjugation[ILS()] = futureStem + 'ont'
        else:
            return 'NO VERB TYPE DEFINED'
