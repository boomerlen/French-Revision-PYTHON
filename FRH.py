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

# The database has the following layout:
# Login details: 'client', 'password'
# IP: 192.168.0.94 (local obviously)
# Database: frh
# Tables:
# adjective -
#   english | varchar(40)
#   french | varchar(30)
#   plural | varchar(32)
#   feminine | varchar(30)
#   comment | varchar(80)
# noun -
#   english | varchar(40)
#   french | varchar(30)
#   plural | varchar(32)
#   gender | char(1) - Either 'm' or 'f'
#   comment | varchar(80)
# misc -
#   english | varchar(40)
#   french | varchar(30)
#   comment | varchar(100)
# verb -
#   english | varchar(40)
#   french | varchar(30)
#   type | char(1) - either 0, 1, 2, 3 - er, re, ir, irregular
#   reflexive | char(1) - either 'y' or 'n'
#   past_participle | varchar(10)
#   (je-ils)_pres_conj | varchar(30) - Conjugation for je-ils in present tense (different column for each subject)
#   (je-ils)_imp_conj | varchar(30) - Conjugation for je-ils in l'imparfait
#   (je-ils)_futur_conj | varchar(30) - Conjugation for je-ils in le futur simple
#   etre | char(1) - either 'y' or 'n'
# rule -
#   description | varchar(150)
#   example | varchar(80)

# Functions defined in this file (descriptions):
# Initialise word lists (this is where C would've been better but fuck me the GUI (and SQL server con) would be impossible and I don't think the memory issues will be that bad)
# Initialise rule lists
# Add word
# Add rule
# Modify rule or word
# Delete rule or word
# View rule or word
# List words by english or french
# List rules
# Others when I think of them

# Functions
def initWordList(curs):
    # Returning a list of all words
    words = []
    try:
        curs.execute("SELECT * FROM adjective")
        adjectives = curs.fetchall()
    except:
        print("Error: Unable to fetch adjectives from server")
        return
    for row in adjectives:
        eng = row[0]
        fre = row[1]
        plu = row[2]
        fem = row[3]
        com = row[4]
        newAdj = Adjective(eng, fre, plu, fem)
        newAdj.comment = com
        words.append(newAdj)
    try:
        curs.execute("SELECT * FROM misc")
        misc = curs.fetchall()
    except:
        print("Error: Unable to fetch miscs from server")
        return False
    for row in misc:
        eng = row[0]
        fre = row[1]
        com = row[2]
        newMisc = Misc(eng, fre)
        newMisc.comment = com
        words.append(newMisc)
    try:
        curs.execute("SELECT * FROM noun")
        nouns = curs.fetchall()
    except:
        print("Error: Unable to fetch nouns from server")
        return False
    for row in nouns:
        eng = row[0]
        fre = row[1]
        plu = row[2]
        gen = row[3]
        com = row[4]
        newNoun = Noun(eng, fre, plu)
        if gen == 'f':
            newNoun.gender = Feminine()
        else:
            newNoun.gender = Masculine()
        newNoun.comment = com
        words.append(newNoun)
    try:
        curs.execute("SELECT * FROM verb")
        verbs = curs.fetchall()
    except:
        print("Error: Unable to fetch verbs from server")
        return False
    pres_conj = []
    imp_conj = []
    futur_conj = []
    for row in verbs:
        eng = row[0]
        fre = row[1]
        type = row[2]
        reflex = row[3]
        past_p = row[4]
        try:
            for i in range(6):
                pres_conj[i] = row[5 + i]
            for i in range(6):
                imp_conj[i] = row[11 + i]
            for i in range(6):
                futur_conj = row[17 + i]
            usesEtre = row[23]
        except:
            print("NOTE: Verb " + eng + " lacks some values. Fix please user!")
        newVerb = Verb(eng, fre)
        if type == "0":
            newVerb.type = ERVerb
        elif type == "1":
            newVerb.type = REVerb
        elif type == "2":
            newVerb.type = IRVerb
        else:
            newVerb.type = IrregularVerb
        if reflex == 'y':
            newVerb.isReflexive = True
        else:
            newVerb.isReflexive = False
        newVerb.pastParticiple = past_p
        newVerb.presentConjugation = pres_conj
        newVerb.imparfaitConjugation = imp_conj
        newVerb.futureSimpleConjugation = futur_conj
        words.append(newVerb)

    return words

def initRuleList(curs):
    rules = []
    try:
        curs.execute("SELECT * FROM rule")
        rs = curs.fetchall()
        for row in rs:
            desc = rs[0]
            ex = rs[1]
            rules.append(Rule(desc, ex))
    except:
        print("Error: Unable to fetch rules from server")
    return rules
# Main script

# SQL Server Connection
# Vars
dbIP = "192.168.0.94"
dbUser = "client"
dbPass = "password"
db = "frh"

database = MySQLdb.connect(dbIP, dbUser, dbPass, db)
cursor = database.cursor()
cursor.execute("SELECT VERSION()") # Verify connection
databaseVersion = cursor.fetchone()
print("Database Version is %s. Connection Successful!" % databaseVersion)

# All we need to pass to functions responsible for managing database access

# Initialisation
wordList = initWordList(cursor)
verbList = []
nounList = []
adjectiveList = []
miscWordList = []
for word in wordList:
    if word.__class__.__name__ == 'Adjective':
        adjectiveList.append(word)
    elif word.__class__.__name__ == 'Noun':
        nounList.append(word)
    elif word.__class__.__name__ == "Misc":
        miscWordList.append(word)
    elif word.__class__.__name__ == "Verb":
        verbList.append(word)
# Defined all word lists
ruleList = initRuleList(cursor)
# Init Done

# TEST:

for x in wordList:
    print(x.englishDef)
#while 1:
    # Do thing
    #break
database.close()
