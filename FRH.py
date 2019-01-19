#! /usr/bin/env python
# FRH.py
# French Revision Helper main file
# Hugo Sebesta

# External modules for import:
import MySQLdb
#from tkinter import *
#from tkinter import messagebox

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
from Funcs import *
from GUI import *

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
#   past_participle | varchar(10) - NOTE: SHOULD BE INCREASED
#   (je-ils)_pres_conj | varchar(30) - Conjugation for je-ils in present tense (different column for each subject)
#   (je-ils)_imp_conj | varchar(30) - Conjugation for je-ils in l'imparfait
#   (je-ils)_futur_conj | varchar(30) - Conjugation for je-ils in le futur simple
#   etre | char(1) - either 'y' or 'n'
# rule -
#   name | idk
#   description | varchar(150)
#   example | varchar(80)


# ALL OF THE FOLLOWING FUNCTIONS HAVE BEEN MOVED TO funcs.py
# Functions defined in this file (descriptions):
# x Initialise word lists (this is where C would've been better but fuck me the GUI (and SQL server con) would be impossible and I don't think the memory issues will be that bad)
# x Initialise rule lists
# x Add word
# x Add rule
# x Modify rule or word - UNTESTED
# x Delete rule or word - UNTESTED

# Main script

# SQL Server Connection

serverVars = []

# Call function to open dialogue to get server values from user
# SQL Server Connection
serverVars = openingDialogueScreen() # Not sure why but this opens 2 windows...

try:
    database = MySQLdb.connect(serverVars[0], serverVars[1], serverVars[2], serverVars[3])
except:
    # Failed! Check connection details
    print("Error: Incorrect login details! Restart application!")
    errorInvalidLogin()
    quit()

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
    #print(word.englishDef) # Testing purposes
# Defined all word lists
ruleList = initRuleList(cursor)

# Init Done
# Call main window class with word variables

# This file is disintegrating into documentation as all of its functions get replaced by instances of classes in other files
# This is a good thing, nice and neat
# One day I'll clean all these comments too!

mainGUICLass = mainGUI(Tk(), verbList, nounList, adjectiveList, miscWordList, ruleList)
database.close()
