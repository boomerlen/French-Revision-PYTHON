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
# x Initialise word lists (this is where C would've been better but fuck me the GUI (and SQL server con) would be impossible and I don't think the memory issues will be that bad)
# x Initialise rule lists
# x Add word
# x Add rule
# Modify rule (x) or word
# Delete rule or word
# View rule or word
# List words by english or french
# List rules
# Others when I think of them

# Functions
def evalGender(gen):
    "Translates a gender class into a gender character identifier"
    if gen.__class__.__name__ == "Masculine":
        return "m"
    else:
        return "f"

def evalType(type):
    "Translates a type class into a type id"
    if type.__class__.__name__ == "ERVerb":
        return "0"
    if type.__class__.__name__ == "REVerb":
        return "1"
    if type.__class__.__name__ == "IRVerb":
        return "2"
    else:
        return "3"

def initWordList(curs):
    'Returns a list of all words from the database'
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
    'Returns a list of all rules from the database'
    rules = []
    try:
        curs.execute("SELECT * FROM rule")
        rs = curs.fetchall()
    except:
        print("Error: Unable to fetch rules from server")
    for row in rs:
        desc = row[0]
        ex = row[1]
        rules.append(Rule(desc, ex))
    return rules

def addWord(curs, word, db):
    'Adds a word to the database given the database cursor, the word, and the database object'
    if word.__class__.__name__ == "Adjective":
        if word.gender.__class__.__name__ == "Masculine":
            gender = 'm'
        else:
            gender = 'f'
        query = "INSERT INTO adjective (english, french, plural, feminine, comment) VALUES ('" + word.englishDef + "', '" + word.frenchDef + "', '" + word.pluralEnd + "', '" + fem + "', '" + word.commentText + "')"
        try:
            curs.execute(query)
            database.commit()
        except:
            print("Error: Failed to add word")
            database.rollback()
            return False
    elif word.__class__.__name__ == "Noun":
        if word.gender.__class__.__name__ == "Masculine":
            gender = 'm'
        else:
            gender = 'f'
        query = "INSERT INTO noun (english, french, plural, gender, comment) VALUES ('" + word.englishDef + "', '" + word.frenchDef + "', '" + word.plural + "', '" + gender + "', '" + word.commentText + "')"
        try:
            curs.execute(query)
            database.commit()
        except:
            print("Error: Failed to add word")
            database.rollback()
            return False
    elif word.__class__.__name__ == "Misc":
        query = "INSERT INTO misc (english, french, comment) VALUES ('" + word.englishDef + "', '" + word.frenchDef + "', '" + word.commentText + "')"
        try:
            curs.execute(query)
            database.commit()
        except:
            print("Error: Failed to add word")
            database.rollback()
            return False
    elif word.__class__.__name == "Verb":
        # SUICIDE TIME
        if word.verbType.__class__.__name__ == ERVerb: # Verb TYpe covered
            type = 0
        elif word.verbType.__class__.__name__ == REVerb:
            type = 1
        elif word.verbType.__class__.__name__ == IRVerb:
            type = 2
        else:
            type = 3
        if word.isReflexive: # Reflexive covered
            reflex = 'y'
        else:
            reflex = 'n'
        if word.usesEtreInPasseCompose: # Etre covered
            etre = 'y'
        else:
            etre = 'n'
        # Huge expression time
        query = "INSERT INTO verb (english, french, type, reflexive, past_participle, je_pres_conj, tu_pres_conj, on_pres_conj, nous_pres_conj, vous_pres_conj, ils_pres_conj, je_imp_conj, tu_imp_conj, on_imp_conj, nous_imp_conj, vous_imp_conj, ils_imp_conj, je_futur_conj, tu_futur_conj, on_futur_conj, nous_futur_conj, vous_futur_conj, ils_futur_conj, etre) VALUES ('"
        queryCommonText = "', '"
        queryFinalText = "')"
        # Gonna make all of the texts to output into a single list to iterate through adding the before and after text to it
        queryTexts = []
        queryTexts.append(word.englishDef)
        queryTexts.append(word.frenchDef)
        queryTexts.append(str(type))
        queryTexts.append(word.pastParticiple) # NOTE: Need to increase size of past pasticiple in database as it is WAY too small (error on my part)
        # Need to do this this way as if the conjugation tables are empty this presents issues
        i = 0
        while i < 6:
            try:
                var = word.presentConjugation[i]
            except:
                var = ''
            queryTexts.append(var)
            i = i + 1
        i = 0
        while i < 6:
            try:
                var = word.imparfaitConjugation[i]
            except:
                var = ''
            queryTexts.append(var)
            i = i + 1
        i = 0
        while i < 6:
            try:
                var = word.futureSimpleConjugation[i]
            except:
                var = ''
            queryTexts.append(var)
        queryTail = ''
        for x in range(23):
            queryTail = queryTail + queryTexts[x] + queryCommonText
        queryTail = queryTail + queryTexts[23] + queryFinalText
        query = query + queryTail
        try:
            curs.execute(query)
            db.commit()
        except:
            db.rollback()
            print("Error: Failed to add word " + word.englishDef + " to database")
    return None

def addRule(curs, rule, db):
    query = "INSERT INTO rule (name, description, example) VALUES ('" + rule.name + "', '"+ rule.description + "', '"
    if not rule.example:
        query = query + "')"
    else:
        query = query + rule.example + "')"
    try:
        curs.execute(query)
        db.commit()
    except:
        db.rollback()
        print("Error: Failed to add rule to database")
    return None

def modifyRule(curs, db, rule, newRule):
    queryStem = "UPDATE rule SET "
    if rule.example != newRule.example:
        newQuery = queryStem + "example = '" + newRule.example + "' WHERE NAME = '" + rule.name + "'"
        try:
            curs.execute(newQuery)
            db.commit()
        except:
            db.rollback()
    if rule.description != newRule.description:
        newQuery = queryStem + "description = '" + newRule.description + "' WHERE NAME = '" + rule.name + "'"
        try:
            curs.execute(newQuery)
            db.commit()
            print("Error: Unable to modify rule")
        except:
            db.rollback()
            print("Error: Unable to modify rule")
    return None

def modifyWord(curs, db, word, newWord):
    "Modifies the SQL DB of a word given the original word object and a new word object"
    # Issues with this function:
    # INCREDIBLY slow compared to simply deleting and recreating the SQL Table entry for any modification in object greater than 1 change
    # Particularly in the Verb set if you are modifying an entire object
    # Could result in up to 23 SQL Update queries which could theoretically be reduced to 2
    # Also no check on out of range errors in the conjugation lists
    # Would probably be good to have another function that just calls the delete then create functions for large modify operations
    if word.__class__.__name__ == "Adjective":
        queryStem = "UPDATE adjective SET "
        if word.frenchDef != newWord.frenchDef:
            query = queryStem + "french = '" + newWord.frenchDef + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.plural != newWord.plural:
            query = queryStem + "plural = '" + newWord.plural + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.feminine != newWord.feminine:
            query = queryStem + "feminine = '" + newWord.feminine + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.commnetText != newWord.commentText:
            query = queryStem + "comment = '" + newWord.commentText + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        return None
    if word.__class__.__name__ == "Noun":
        queryStem = "UPDATE noun SET "
        if word.frenchDef != newWord.frenchDef:
            query = queryStem + "french = '" + newWord.frenchDef + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.plural != newWord.plural:
            query = queryStem + "plural = '" + newWord.plural + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.gender != newWord.gender:
            gender = evalGender(newWord.gender)
            query = queryStem + "gender = '" + gender + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.commnetText != newWord.commentText:
            query = queryStem + "comment = '" + newWord.commentText + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        return None
    if word.__class__.__name__ == "Verb":
        # PAIN
        if word.frenchDef != newWord.frenchDef:
            query = queryStem + "french = '" + newWord.frenchDef + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.type != newWord.type:
            type = evalType(newWord.type)
            query = queryStem + "type = '" + type + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.reflexive != newWord.reflexive:
            if newWord.reflexive:
                refl = "y"
            else:
                refl = "n"
            query = queryStem + "reflexive = '" + refl + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.pastParticiple != newWord.pastParticiple:
            query = queryStem + "past_participle = '" + newWord.pastParticiple + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.presentConjugation[0] != newWord.presentConjugation[0]:
            query = queryStem + "je_pres_conj = '" + newWord.presentConjugation[0] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.presentConjugation[1] != newWord.presentConjugation[1]:
            query = queryStem + "tu_pres_conj = '" + newWord.presentConjugation[1] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.presentConjugation[2] != newWord.presentConjugation[2]:
            query = queryStem + "on_pres_conj = '" + newWord.presentConjugation[2] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.presentConjugation[3] != newWord.presentConjugation[3]:
            query = queryStem + "nous_pres_conj = '" + newWord.presentConjugation[3] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.presentConjugation[4] != newWord.presentConjugation[4]:
            query = queryStem + "vous_pres_conj = '" + newWord.presentConjugation[4] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.presentConjugation[5] != newWord.presentConjugation[5]:
            query = queryStem + "ils_pres_conj = '" + newWord.presentConjugation[5] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.imparfaitConjugation[0] != newWord.imparfaitConjugation[0]:
            query = queryStem + "je_imp_conj = '" + newWord.imparfaitConjugation[0] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.imparfaitConjugation[1] != newWord.imparfaitConjugation[1]:
            query = queryStem + "tu_imp_conj = '" + newWord.imparfaitConjugation[1] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.imparfaitConjugation[2] != newWord.imparfaitConjugation[2]:
            query = queryStem + "on_imp_conj = '" + newWord.imparfaitConjugation[2] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.imparfaitConjugation[3] != newWord.imparfaitConjugation[3]:
            query = queryStem + "nous_imp_conj = '" + newWord.imparfaitConjugation[3] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.imparfaitConjugation[4] != newWord.imparfaitConjugation[4]:
            query = queryStem + "vous_imp_conj = '" + newWord.imparfaitConjugation[4] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.imparfaitConjugation[5] != newWord.imparfaitConjugation[5]:
            query = queryStem + "ils_imp_conj = '" + newWord.imparfaitConjugation[5] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.futureSimpleConjugation[0] != newWord.futureSimpleConjugation[0]:
            query = queryStem + "je_imp_conj = '" + newWord.futureSimpleConjugation[0] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.futureSimpleConjugation[1] != newWord.futureSimpleConjugation[1]:
            query = queryStem + "tu_imp_conj = '" + newWord.futureSimpleConjugation[1] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.futureSimpleConjugation[2] != newWord.futureSimpleConjugation[2]:
            query = queryStem + "on_imp_conj = '" + newWord.futureSimpleConjugation[2] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.futureSimpleConjugation[3] != newWord.futureSimpleConjugation[3]:
            query = queryStem + "nous_imp_conj = '" + newWord.futureSimpleConjugation[3] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.futureSimpleConjugation[4] != newWord.futureSimpleConjugation[4]:
            query = queryStem + "vous_imp_conj = '" + newWord.futureSimpleConjugation[4] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.futureSimpleConjugation[5] != newWord.futureSimpleConjugation[5]:
            query = queryStem + "ils_imp_conj = '" + newWord.futureSimpleConjugation[5] + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.usesEtreInPasseCompose != newWord.usesEtreInPasseCompose:
            if newWord.usesEtreInPasseCompose:
                etre = "y"
            else:
                etre = "n"
            query = queryStem + "etre = '" + etre + "' WHERE english = '" + word.englishDef  + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
            return None
    if word.__class__.__name__ == "Misc":
        if word.commnetText != newWord.commentText:
            query = queryStem + "comment = '" + newWord.commentText + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
        if word.frenchDef != newWord.frenchDef:
            query = queryStem + "french = '" + newWord.frenchDef + "' WHERE english = '" + word.englishDef + "'"
            try:
                curs.execute(query)
                db.commit()
            except:
                db.rollback()
            return None
    return False

def deleteObject(curs, db, obj):
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
    print(word.englishDef) # Testing purposes
# Defined all word lists
ruleList = initRuleList(cursor)
# Init Done

database.close()
