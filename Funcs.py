# Funcs.py
# Module containing all the main functions used in my program
# Used to be used to navigate the SQL Database before moving all that code to SQLDB.py
# Now just contains a couple of resolution functions of extremely limited use
# By Hugo Sebesta

from Classes import *

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
