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

# Global Vars
#global actualRadioVariable ?

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
        # newWord2
        def newWord2():
            newWin.destroy()
            newWin2 = Tk()

            if radioVariable.get() == "rule":
                # Info to fill
                newName, newDesc, newEx = ""
                # Function for button handler
                def nextButtonPressed():
                    newName = nameEntry.get()
                    newDesc = descriptionEntry.get()
                    newEx = exampleEntry.get()
                    self.ruleList.append(Rule(newName, newDesc, newEx))
                    # addRule(curs, Rule(newName, newDesc, newEx), db)
                # Window for creating rule
                title = Label(newWin2, text="New Rule", font=("Helvetica", 24))

                nameEntryLabel = Label(newWin2, text="Name:", font=("Helvetica"))
                nameEntry = Entry(newWin2, font=("Helvetica"))

                # NOTE: Some way to enforce a character count relative to the max size of the database entry would be good to implement
                descriptionEntryLabel = Label(newWin2, text="Description:", font=("Helvetica"))
                descriptionScrollbar = Scrollbar(newWin2)
                descriptionEntry = Entry(newWin2, font=("Helvetica"), xscrollcommand=descriptionScrollbar.set)
                descriptionScrollbar.config(command=descriptionEntry.xview)

                exampleEntryLabel = Label(newWin2, text="Example:", font=("Helvetica"))
                exampleScrollbar = Scrollbar(newWin2)
                exampleEntry = Entry(newWin2, font=("Helvetica"), xscrollcommand=exampleScrollbar.set)
                exampleScrollbar.config(command=exampleEntry.xview)

                nextButton = Button(newWin2, command=nextButtonPressed, text="Next", font=("Helvetica"))

                # Geometry
                title.grid(row=0, column=0, columnspan=2)
                nameEntryLabel.grid(row=1, column=0)
                nameEntry.grid(row=1, column=1)
                descriptionEntryLabel.grid(row=2, column=0)
                descriptionEntry.grid(row=2, column=1, columnspan=3, rowspan=2)
                exampleEntryLabel.grid(row=4, column=0)
                exampleEntry.grid(row=4, column=1, columnspan=3, rowspan=2)
                nextButton.grid(row=5, column=1, columnspan=2)

                newWin2.mainloop()
            elif radioVariable.get() == "verb":
                # info to fill
                newEng, newFre, newType, newPP = ""
                newEtre, newReflex = False
                newPres, newImp, newFutur = []
                # There's a lot

                # Relevant functions
                def moreButtonCallback():
                    moreButtonFrame.grid(row=3, column=0, columnspan=5, rowspan=10)
                    presentConjugationFrame.grid(row=0, column=0, columspan=2, rowspan=6)
                    imparfaitConjugationFrame.grid(row=0, column=2, columspan=2, rowspan=6)
                    futurConjugationFrame.grid(row=6, column=0, columnspan=5, rowspan=3)
                    #

                def lessButtonCallback():
                    pass
                def nextButtonPressed():
                    pass # Fill everything then call the database access function to add it to DB

                # Widget setup
                title = Label(newWin2, text="Verb", font=("Helvetica"))

                # Gonna have inputs outside then a button saying more which expands all the conjugations so that they don't clog up the screen if they won't be set immediately
                englishEntryLabel = Label(newWin2, text="English:", font=("Helvetica"))
                englishEntry = Entry(newWin2, font=("Helvetica"))

                frenchEntryLabel = Label(newWin2, text="French:", font=("Helvetica"))
                frenchEntry = Entry(newWin2, font=("Helvetica"))

                reflexiveLabel = Label(newWin2, text="Is Reflexive:", font=("Helvetica"))
                reflexiveSpinboxEntry = Spinbox(newWin2, values=["Yes", "No"])

                typeLabel = Label(newWin2, text="Type:", font=("Helvetica"))
                typeSpinboxEntry = Spinbox(newWin2, values=["ER Verb", "RE Verb", "IR Verb", "Irregular"])

                moreButton = Button(newWin2, text="More...", font=("Helvetica"), command=moreButtonCallback)
                lessButton = Button(newWin2, text="Less...", font=("Helvetica"), command=lessButtonCallback)
                # All the stuff that the more button activates. It just calls the grid method on the frame
                # Upon reflection, this could all be a loop. but fuck it we're here now may as well follow through
                # If I ever needed to reduce the size of this file or optimise for some reason:
                # Make a list to store all these then a list to store "je, tu, on" etc
                # Have some loop that sticks makes as many widgets as we need with those subjects and sticks them in the other list
                # That would probably take like 10 lines so we'd save a bit of space probably
                # Probably make setting the grid up a bit easier too
                # Hell it would make everything easier but I've invested too much time now to change it for no reason
                # Frames 
                presentConjugationFrame = Frame(moreButtonFrame, text="Present Conjugation", font=("Helvetica"))

                # Gonna try just making a loop and list for this cuz bloody hell
                presLabels, presEntries, impLabels, impEntries, futurLabels, futurEntries = []
                subjects = ["je:", "tu:", "on:", "nous:", "vous:", "ils:"]

                # Logic: have to do 3 seperate loops because of different frames. May as well seperate out lists too for convenience
                for i in range(6):
                    presLabels.append(Label(presentConjugationFrame, text=subjects[i], font=("Helvetica")))
                    presEntries.append(Entry(presentConjugationFrame, font=("Helvetica")))
                for i in range(6):
                    impLabels.append(Label(impConjugationFrame, text=subjects[i], font=("Helvetica")))
                    impEntries.append(Entry(impConjugationFrame, font=("Helvetica")))
                for i in range(6):
                    futurLabels.append(Label(futurConjugationFrame, text=subjects[i], font=("Helvetica")))
                    futurEntries.append(Entry(futurConjugationFrame, font=("Helvetica")))
                # That did seriously take about a 10th as long

                moreButtonFrame = Frame(newWin2, text="More", font=("Helvetica"))

                usesEtreLabel = Label(moreButtonFrame, text="Uses Etre in Passe Compose:", font=("Helvetica"))
                usesEtreSpinbox = Spinbox(moreButtonFrame, values=["Yes", "No"])

                ppEntryLabel = Label(moreButtonFrame, text="Past Participle:", font=("Helvetica"))
                ppEntry = Entry(moreButtonFrame, font=("Helvetica"))


                presentJeEntryLabel = Label(presentConjugationFrame, text="Je:", font=("Helvetica"))
                presentJeEntry = Entry(presentConjugationFrame, font=("Helvetica"))

                presentTuEntryLabel = Label(presentConjugationFrame, text="Tu:", font=("Helvetica"))
                presentTuEntry = Entry(presentConjugationFrame, font=("Helvetica"))

                presentOnEntryLabel = Label(presentConjugationFrame, text="On:", font=("Helvetica"))
                presentOnEntry = Entry(presentConjugationFrame, font=("Helvetica"))

                presentNousEntryLabel = Label(presentConjugationFrame, text="Nous:", font=("Helvetica"))
                presentNousEntry = Entry(presentConjugationFrame, font=("Helvetica"))

                presentVousEntryLabel = Label(presentConjugationFrame, text="Vous:", font=("Helvetica"))
                presentVousEntry = Entry(presentConjugationFrame, font=("Helvetica"))

                presentIlsEntryLabel = Label(presentConjugationFrame, text="Ils:", font=("Helvetica"))
                presentIlsEntry = Entry(presentConjugationFrame, font=("Helvetica"))

                imparfaitConjugationFrame = Frame(moreButtonFrame, text="Imparfait Conjugation", font=("Helvetica"))

                imparfaitJeEntryLabel = Label(imparfaitConjugationFrame, text="Je:", font=("Helvetica"))
                imparfaitJeEntry = Entry(imparfaitConjugationFrame, font=("Helvetica"))

                imparfaitTuEntryLabel = Label(imparfaitConjugationFrame, text="Tu:", font=("Helvetica"))
                imparfaitTuEntry = Entry(imparfaitConjugationFrame, font=("Helvetica"))

                imparfaitOnEntryLabel = Label(imparfaitConjugationFrame, text="On:", font=("Helvetica"))
                imparfaitOnEntry = Entry(imparfaitConjugationFrame, font=("Helvetica"))

                imparfaitNousEntryLabel = Label(imparfaitConjugatioNFrame, text="Nous:", font=("Helvetica"))
                imparfaitNousEntry = Entry(imparfaitConjugationFrame, font=("Helvetica"))

                imparfaitVousEntryLabel = Label(imparfaitConjugationFrame, text="Vous:", font=("Helvetica"))
                imparfaitVousEntry = Entry(imparfaitConjugationFrame, font=("Helvetica"))

                imparfaitIlsEntryLabel = Label(imparfaitConjguationFrame, text="Ils:", font=("Helvetica"))
                imparfaitIlsEntry = Entry(imparfaitConjugationFrame, font=("Helvetica"))

                futurConjugationFrame = Frame(moreButtonFrame, text="Future Simple Conjugation", font=("Helvetica"))

                futurJeEntryLabel = Label(futurConjugationFrame, font=("Helvetica"), text="Je:")
                futurJeEntry = Entry(futurConjugationFrame, font=("Helvetica"))

                futurTuEntryLabel = Label(futurConjugationFrame, font=("Helvetica"), text="Tu:")
                futurTuEntry = Entry(futurConjugationFrame, font=("Helvetica"))

                futurOnEntryLabel = Label(futurConjugationFrame, font=("Helvetica"), text="On:")
                futurOnEntry = Entry(futurConjugationFrame, font=("Helvetica"))

                futurNousEntryLabel = Label(futurConjugationFrame, font=("Helvetica"), text="Nous:")
                futurNousEntry = Entry(futurConjugationFrame, font=("Helvetica"))

                futurVousEntryLabel = Label(futurConjugationFrame, font=("Helvetica"), text="Vous:")
                futurVousEntry = Entry(futurConjugationFrame, font=("Helvetica"))

                futurIlsEntryLabel = Label(futurConjugationFrame, font=("Helvetica"), text="Ils:")
                futurIlsEntry = Entry(futurConjugationFrame, font=("Helvetica"))

                goButton = Button(newWin2, text="Next", command=nextButtonPressed)

                # Geometry
                title.grid(row=0, column=2)
                englishEntryLabel.grid(row=1, column=0)
                englishEntry.grid(row=1, column=1)
                frenchEntryLabel.grid(row=1, column=3) # 2 per line
                frenchEntry.grid(row=1, column=4)
                reflexiveLabel.grid(row=2, column=0) # TODO finish this
                reflexiveSpinboxEntry.grid(row=2, column=1)
                typeLabel.grid(row=2, column=3)
                typeSpinboxEntry.grid(row=2, column=4)
                moreButton.grid(row=3, column=1)
                goButton.grid(row=3, column=3)
                # Note not rending all the conjugations cuz they go under "more..."
            elif radioVariable.get() == "noun":
                pass
            elif radioVariable.get() == "adjective":
                pass
            else:
                pass


        radioVariable = StringVar() # This doesn't get set for some reason
        # RadioButton Function
        def setRadioVariable():
            pass
        #    actualRadioVariable = radioVariable.get()
        #    print(actualRadioVariable)
        #    print(radioVariable.get())
        # Widgets
        title = Label(newWin, text="Select type to add.", font=("Helvetica", 24))
        r1 = Radiobutton(newWin, text="Rule", variable=radioVariable, value="rule", command=setRadioVariable)
        r2 = Radiobutton(newWin, text="Verb", variable=radioVariable, value="verb", command=setRadioVariable)
        r3 = Radiobutton(newWin, text="Noun", variable=radioVariable, value="noun", command=setRadioVariable)
        r4 = Radiobutton(newWin, text="Adjective", variable=radioVariable, value="adjective", command=setRadioVariable)
        r5 = Radiobutton(newWin, text="Other word", variable=radioVariable, value="misc", command=setRadioVariable)
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
            self.newWord()
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
