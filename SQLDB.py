# SQLDB.py
# Module containing class used to manage the database which can be passed between everything and used by the GUI interface
# Hugo Sebesta

import MySQLdb
from tkinter import messagebox

from Classes import *
from Funcs import *

class DB:
    "Class containing all methods for database use and access"

    serverIP = "58.168.115.13"
    serverUser = "client"
    serverPass = "password"
    serverDBName = "frh"

    database = None # Override it immediately
    cursor = None # yet

    def __init__(self, ip = "58.168.115.13", user = "client", passwd = "password", db = "frh"):
        self.serverIP = ip
        self.serverUser = user
        self.serverPass = passwd
        self.serverDBName = db
        try:
            self.database = MySQLdb.connect(self.serverIP, self.serverUser, self.serverPass, self.serverDBName)
        except:
            messagebox.showerror("ERROR", "Cannot connect to server!")
            quit()
        self.cursor = self.database.cursor()

    def initWordList(self):
        "Returns a list of all words from the database"
        words = []
        try:
            self.cursor.execute("SELECT * FROM adjective")
            adjectives = self.cursor.fetchall()
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
            self.cursor.execute("SELECT * FROM misc")
            misc = self.cursor.fetchall()
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
            self.cursor.execute("SELECT * FROM noun")
            nouns = self.cursor.fetchall()
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
            self.cursor.execute("SELECT * FROM verb")
            verbs = self.cursor.fetchall()
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

    def initRuleList(self):
        'Returns a list of all rules from the database'
        rules = []
        try:
            self.cursor.execute("SELECT * FROM rule")
            rs = self.cursor.fetchall()
        except:
            print("Error: Unable to fetch rules from server")
        for row in rs:
            desc = row[0]
            ex = row[1]
            rules.append(Rule(desc, ex))
        return rules

    def addWord(self, word):
        'Adds a word to the database given the database cursor, the word, and the database object'
        if word.__class__.__name__ == "Adjective":
            if word.gender.__class__.__name__ == "Masculine":
                gender = 'm'
            else:
                gender = 'f'
            query = "INSERT INTO adjective (english, french, plural, feminine, comment) VALUES ('" + word.englishDef + "', '" + word.frenchDef + "', '" + word.pluralEnd + "', '" + fem + "', '" + word.commentText + "')"
            try:
                self.cursor.execute(query)
                self.database.commit()
            except:
                print("Error: Failed to add word")
                self.database.rollback()
                return False
        elif word.__class__.__name__ == "Noun":
            if word.gender.__class__.__name__ == "Masculine":
                gender = 'm'
            else:
                gender = 'f'
            query = "INSERT INTO noun (english, french, plural, gender, comment) VALUES ('" + word.englishDef + "', '" + word.frenchDef + "', '" + word.plural + "', '" + gender + "', '" + word.commentText + "')"
            try:
                self.cursor.execute(query)
                self.database.commit()
            except:
                print("Error: Failed to add word")
                self.database.rollback()
                return False
        elif word.__class__.__name__ == "Misc":
            query = "INSERT INTO misc (english, french, comment) VALUES ('" + word.englishDef + "', '" + word.frenchDef + "', '" + word.commentText + "')"
            try:
                self.cursor.execute(query)
                self.database.commit()
            except:
                print("Error: Failed to add word")
                self.database.rollback()
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
                self.cursor.execute(query)
                self.database.commit()
            except:
                self.database.rollback()
                print("Error: Failed to add word " + word.englishDef + " to database")
        return None

    def addRule(self, rule):
        "Inserts a rule into the SQL Server"
        query = "INSERT INTO rule (name, description, example) VALUES ('" + rule.name + "', '"+ rule.description + "', '"
        if not rule.example:
            query = query + "')"
        else:
            query = query + rule.example + "')"
        try:
            self.cursor.execute(query)
            self.database.commit()
        except:
            self.database.rollback()
            print("Error: Failed to add rule to database")
        return None

    def modifyRule(self, rule, newRule):
        "Modifies a Rule in the SQL Server"
        queryStem = "UPDATE rule SET "
        if rule.example != newRule.example:
            newQuery = queryStem + "example = '" + newRule.example + "' WHERE NAME = '" + rule.name + "'"
            try:
                self.cursor.execute(newQuery)
                self.database.commit()
            except:
                self.database.rollback()
        if rule.description != newRule.description:
            newQuery = queryStem + "description = '" + newRule.description + "' WHERE NAME = '" + rule.name + "'"
            try:
                self.cursor.execute(newQuery)
                self.database.commit()
                print("Error: Unable to modify rule")
            except:
                self.database.rollback()
                print("Error: Unable to modify rule")
        return None

    def deleteObject(self, obj):
        "Deletes an object from the SQL server"
        if obj.__class__.__name__ != "Rule":
            query = "DELETE FROM " + obj.__class__.__name__.lower() + " WHERE english = '" + obj.englishDef + "'"
        else:
            query = "DELETE FROM rule WHERE name = '" + obj.name + "'"
        try:
            self.cursor.execute(query)
            self.database.commit()
        except:
            self.database.rollback()
            print("Error: Failed to delete object!")
            return False
        return None

    def modifyWord(self, word, newWord):
        "Modifies the SQL DB of a word given the original word object and the new word object "
        # This version is optimised against the old one by just deleting and replacing the word
        self.deleteObject(word)
        # And replace
        self.addWord(newWord)
        # Much easier lmao
        return None

    def __del__(self):
        try:
            self.database.close()
        except:
            pass # We won't actually every get here in practice just that the compiler doesn't know that
