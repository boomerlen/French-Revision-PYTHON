# GUI.py
# Module containing the window classes I am using with TKinter
# By Hugo Sebesta

# External
from tkinter import *
from tkinter import messagebox
import os
# Mine
from Classes import *
from Funcs import *

def openingDialogueScreen():
    # Default vars:
    dbIP = "192.168.0.94"
    dbUser = "client"
    dbPass = "password"
    db = "frh"

    openingDialogue = Tk()
    title = Label(openingDialogue, text="WELCOME", font=("Helvetica", 44))

    frame = LabelFrame(openingDialogue, text="Connection Details:", font=("Helvetica"))

    ipEntryText = Label(frame, text="Server IP")
    dbIPStrVar = StringVar(frame, value=dbIP)
    ipEntry = Entry(frame, font=("Helvetica"), textvariable=dbIPStrVar)

    userEntryText = Label(frame, text="Server User")
    dbUserStrVar = StringVar(frame, value=dbUser)
    userEntry = Entry(frame, font=("Helvetica"), textvariable=dbUserStrVar)

    passEntryText = Label(frame, text="Server Password")
    dbPassStrVar = StringVar(frame, value=dbPass)
    passEntry = Entry(frame, font=("Helvetica"), textvariable=dbPassStrVar)

    dbEntryText = Label(frame, text="Database")
    dbStrVar = StringVar(frame, value=db)
    dbEntry = Entry(frame, font=("Helvetica"), textvariable=dbStrVar)

    # Geometry/layout
    ipEntryText.grid(column=0, row=1)
    ipEntry.grid(column=1, row=1)

    userEntryText.grid(column=0, row=2)
    userEntry.grid(column=1, row=2)

    passEntryText.grid(column=0, row=3)
    passEntry.grid(column=1, row=3)

    dbEntryText.grid(column=0, row=4)
    dbEntry.grid(column=1, row=4)

    toReturn = []
    def openingDialogueGoButton():
        toReturn.append(ipEntry.get())
        toReturn.append(userEntry.get())
        toReturn.append(passEntry.get())
        toReturn.append(dbEntry.get())
        openingDialogue.destroy()

    go = Button(frame, text="Go!", command=openingDialogueGoButton)
    go.grid(column=1, row=5)

    title.grid(column=0, row=0, columnspan=2)
    frame.grid(column=0, row=1, columnspan=3)

    openingDialogue.mainloop()
    return toReturn

def errorInvalidLogin():
    messagebox.showerror("ERROR", "Invalid login details!")
    return None

class mainGUI:
    master = Tk()
    verbList = []
    nounList = []
    adjectiveList = []
    miscWordList = []
    ruleList = []




    def newWord(self):
        newWin = Tk()
        radioVariable = ""

        # newWord2
        def newWord2():
            newWin.quit()
            newWin2 = Tk()
            if radioVariable == "rule":
                # Info to fill
                newName, newDesc, newEx = ""
                # Window for creating rule
                title = Label(newWin2, text="New Rule", font=("Helvetica", 24))

                nameEntryLabel = Label(newWin2, text="Name:", font=("Helvetica"))
                nameEntry = Entry(newWin2, font=("Helvetica"))

                descriptionFrame = Frame(newWin2)
                descriptionEntryLabel = Label(descriptionFrame, text="Description", font=("Helvetica"))
                descriptionScrollbar = Scrollbar(descriptionFrame)
                descriptionEntry = Entry(descriptionFrame, font=("Helvetica"))
                # do more stuff
            elif radioVariable == "verb":
                pass
            elif radioVariable == "noun":
                pass
            elif radioVariable == "adjective":
                pass
            else:
                pass

        # Widgets
        title = Label(newWin, text="Select type to add.", font=("Helvetica", 24))
        r1 = Radiobutton(newWin, text="Rule", variable=radioVariable, value="rule")
        r2 = Radiobutton(newWin, text="Verb", variable=radioVariable, value="verb")
        r3 = Radiobutton(newWin, text="Noun", variable=radioVariable, value="noun")
        r4 = Radiobutton(newWin, text="Adjective", variable=radioVariable, value="adjective")
        r5 = Radiobutton(newWin, text="Other word...", variable=radioVariable, value="misc")
        next = Button(newWin, text="Next", command=newWord2)

        r1.select()

        # Layout
        title.grid(row=0, column=0,columnspan=3)
        r1.grid(row=1, column=0, columnspan=3)
        r2.grid(row=2, column=0, columnspan=3)
        r3.grid(row=3, column=0, columnspan=3)
        r4.grid(row=4, column=0, columnspan=3)
        r5.grid(row=5, column=0, columnspan=3)
        next.grid(row=6, column=1)

        # done
        newWin.mainloop()

    def __init__(self, root, verbs, nouns, adjectives, miscs, rules):
        # Initial variable setting
        self.master = root
        self.verbList = verbs
        self.nounList = nouns
        self.adjectiveList = adjectives
        self.miscWordList = miscs
        self.ruleList = rules

        # Rendering the main menu
        # Make all the widgets

        # Menubar
        # Commands
        def menuFileOpen():
            os.execl("FRH.py", "1") # this doesnt work :)
            pass
        def menuFileExport():
            # tf we wanna do here jesus
            pass
        def menuFileClose():
            # yea idk what this one wouuld do either
            pass

        def menuEditNew():
            pass
        def menuEditUndo():
            pass
        def menuEditCut():
            pass
        def menuEditCopy():
            pass
        def menuEditPaste():
            pass
        def menuEditDelete():
            pass

        def menuHelpAbout():
            pass
        def menuHelpHelp():
            pass
        # Widgets
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=menuFileOpen)
        filemenu.add_command(label="Export", command=menuFileExport)
        filemenu.add_command(label="Close", command=menuFileClose)
        filemenu.add_separator()
        filemenu.add_command(labe="Exit", command=self.master.quit) # This might be wrong
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="New...", command=menuEditNew)
        editmenu.add_command(label="Undo", command=menuEditUndo)
        editmenu.add_command(label="Cut", command=menuEditCut)
        editmenu.add_command(label="Copy", command=menuEditCopy)
        editmenu.add_command(label="Paste", command=menuEditPaste)
        editmenu.add_command(label="Delete", command=menuEditDelete)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=menuHelpAbout)
        helpmenu.add_command(label="Help", command=menuHelpHelp)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # Done, make modifications to the root window
        self.master.config(menu=menubar)
        self.master.mainloop()
