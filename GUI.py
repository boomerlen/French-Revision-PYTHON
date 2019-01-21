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
        # NOTE: Forgot about comment text for all words except misc
        # if there is demand, properly implement it.
        newWin = Tk()
        # newWord2
        def newWord2():
            newWin.destroy()
            newWin2 = Tk()

            if radioVariable.get() == "rule": # Testing purposes
                # Info to fill
                newName = ""
                newDesc = ""
                newEx = ""
                # Function for button handler
                def nextButtonPressed():
                    newName = nameEntry.get()
                    newDesc = descriptionEntry.get()
                    newEx = exampleEntry.get()
                    self.ruleList.append(Rule(newName, newDesc, newEx))
                    # addRule(curs, Rule(newName, newDesc, newEx), db)
                    messagebox.showinfo("Done!", "Created rule " + newName + "!")
                    newWin2.destroy()
                    return
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
                exampleEntry = Entry(newWin2, font=("Helvetica"), xscrollcommand=exampleScrollbar.set) # Scrollbar doesn't work
                exampleScrollbar.config(command=exampleEntry.xview)

                nextButton = Button(newWin2, command=nextButtonPressed, text="Next", font=("Helvetica"))

                # Geometry
                title.grid(row=0, column=0, columnspan=2)
                nameEntryLabel.grid(row=1, column=0)
                nameEntry.grid(row=1, column=1)
                descriptionEntryLabel.grid(row=2, column=0)
                descriptionEntry.grid(row=2, column=1, columnspan=3, rowspan=2)
                exampleEntryLabel.grid(row=4, column=0)
                exampleEntry.grid(row=4, column=1, columnspan=3, rowspan=2) # Formatting is off
                nextButton.grid(row=5, column=1, columnspan=2)

                newWin2.mainloop()
            elif radioVariable.get() == "verb": # Testing Purposes
                # info to fill - most complex (ofc)
                newEng = "" # Apparently had to unpack this. Apparently doesn't work like it does in c/c++
                newFre = ""
                newType = ""
                newPP = ""
                newReflex = False
                newEtre = False
                newFutur = []
                newPres = []
                newImp = []
                # populate the lists with default values so we don't get issues
                for i in range(6):
                    newPres.append("")
                    newImp.append("")
                    newFutur.append("")
                # There's a lot

                # Relevant functions
                def moreButtonCallback():
                    moreButtonFrame.grid(row=3, column=0, columnspan=5, rowspan=10)
                    presentConjugationFrame.grid(row=0, column=0, columnspan=2, rowspan=6)
                    imparfaitConjugationFrame.grid(row=0, column=2, columnspan=2, rowspan=6)
                    futurConjugationFrame.grid(row=6, column=0, columnspan=5, rowspan=3)
                    # use the lists with a loop to populate the remaining stuff
                    for i in range(6): # could compress into one loop if desired
                        presLabels[i].grid(row=i, column=0)
                        presEntries[i].grid(row=i, column=1)
                    for i in range(6):
                        impLabels[i].grid(row=i, column=0)
                        impEntries[i].grid(row=i, column=1)
                    for i in range(6):
                        if i % 2 == 0:
                            labelCol = 1
                        else:
                            labelCol = 3
                        futurLabels[i].grid(row=(i/2-(i%2)/2), column=labelCol)
                        futurEntries[i].grid(row=(i/2-(i%2)/2), column=(labelCol+1)) # Complicated maths
                    # Gotta render the less button!
                    moreButton.grid_forget() # This didn't seem to work
                    lessButton.grid(row=19, column=1) # See if Row is correct when testing! (trial and error)
                    goButton.grid(row=19, column=3)
                def lessButtonCallback():
                    moreButtonFrame.grid_forget()
                    lessButton.grid_forget()
                    goButton.grid(row=3, column=3)
                    moreButton.grid(row=3, column=1)
                def nextButtonPressed():
                    # Fill everything then call the database access function to add it to DB
                    # This will be fun
                    # Ordinary values
                    newEng = englishEntry.get()
                    newFre = frenchEntry.get()
                    newType = typeSpinboxEntry.get() # might not work
                    newPP = ppEntry.get()
                    if newType == "ER Verb":
                        actualType = ERVerb()
                    elif newType == "RE Verb":
                        actualType = REVerb()
                    elif newType == "IRVerb":
                        actualType = IRVerb()
                    else:
                        actualType = IrregularVerb()
                    # Harder
                    if reflexiveSpinboxEntry.get() == "Yes":
                        newReflex = True
                    if usesEtreSpinbox.get() == "Yes":
                        newEtre = True
                    # Those lists
                    for i in range(6):
                        newPres[i] = presEntries[i].get()
                        newImp[i] = impEntries[i].get()
                        newFutur[i] = futurEntires[i].get()
                    # All done
                    newVerb = Verb(newEng, newFre, actualType, newReflex)
                    newVerb.pastParticiple = newPP
                    newVerb.presentConjugation = newPres
                    newVerb.imparfaitConjugation = newImp
                    newVerb.futureSimpleConjugation = newFutur
                    newVerb.usesEtreInPasseCompose = newEtre
                    self.verbList.append(newVerb)
                    # call the shit to add the verb to the db passing newVerb
                    messagebox.showinfo("Done!", "Created verb " + newFre + "!")
                    newWin2.destroy()
                    return


                # Widget setup
                title = Label(newWin2, text="Verb", font=("Helvetica"))

                # Frame
                moreButtonFrame = LabelFrame(newWin2, text="More", font=("Helvetica"))

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
                # All the stuff that the more button activates. It just calls the grid method on the frame and then the respective members of the list
                # Frames
                presentConjugationFrame = LabelFrame(moreButtonFrame, text="Present Conjugation", font=("Helvetica"))
                imparfaitConjugationFrame = LabelFrame(moreButtonFrame, text="Imparfait Conjugation", font=("Helvetica"))
                futurConjugationFrame = LabelFrame(moreButtonFrame, text="Future Simple Conjugation", font=("Helvetica"))

                # lists comprising the conjugation table for setting up the labels and entries
                futurEntries = []
                presLabels = []
                presEntries = []
                impLabels = []
                impEntries = []
                futurLabels = []

                subjects = ["je:", "tu:", "on:", "nous:", "vous:", "ils:"]

                # Logic: have to do 3 seperate loops because of different frames. May as well seperate out lists too for convenience
                for i in range(6):
                    presLabels.append(Label(presentConjugationFrame, text=subjects[i], font=("Helvetica")))
                    presEntries.append(Entry(presentConjugationFrame, font=("Helvetica")))
                for i in range(6):
                    impLabels.append(Label(imparfaitConjugationFrame, text=subjects[i], font=("Helvetica")))
                    impEntries.append(Entry(imparfaitConjugationFrame, font=("Helvetica")))
                for i in range(6):
                    futurLabels.append(Label(futurConjugationFrame, text=subjects[i], font=("Helvetica")))
                    futurEntries.append(Entry(futurConjugationFrame, font=("Helvetica")))
                # That did seriously take about a 10th as long
                # Removing the original work I did (in like an hour )

                usesEtreLabel = Label(moreButtonFrame, text="Uses Etre in Passe Compose:", font=("Helvetica"))
                usesEtreSpinbox = Spinbox(moreButtonFrame, values=["Yes", "No"])

                ppEntryLabel = Label(moreButtonFrame, text="Past Participle:", font=("Helvetica"))
                ppEntry = Entry(moreButtonFrame, font=("Helvetica"))

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
                # this is becoming rather aids

                # Start with all the widgets (ah duh)
                # Not too many fields to fill luckily
                newEng = ""
                newFre = ""
                newPlural = ""
                newGen = ""

                # callback function
                def GoButtonCallback():
                    newEng = engEntry.get()
                    newFre = freEntry.get()
                    newPlural = pluralEntry.get()
                    newGen = genderEntry.get()
                    if newGen == "Masculine":
                        gender = Masculine()
                    else:
                        gender = Feminine()
                    self.nounList.append(Noun(newEng, newFre, newPlural, gender))
                    # whatever function I figure out I'm using for the DB
                    newWin2.quit()
                    messagebox.showinfo("Done!", "Added noun " + newFre + "!")
                    return
                # Wdigets
                title = Label(newWin2, text="Noun", font=("Helvetica"))

                engEntryLabel = Label(newWin2, text="English:", font=("Helvetica"))
                engEntry = Entry(newWin2, font=("Helvetica"))

                freEntryLabel = Label(newWin2, text="French:", font=("Helvetica"))
                freEntry = Entry(newWin2, font=("Helvetica"))

                pluralEntryLabel = Label(newWin2, text="Plural Ending:", font=("Helvetica"))
                pluralEntry = Entry(newWin2, font=("Helvetica"))

                genderEntryLabel = Label(newWin2, text="Gender:", font=("Helvetica"))
                pluralEntry = Spinbox(newWin2, values=["Masculine", "Feminine"])

                goButton = Button(newWin2, text="Next", command=GoButtonCallback)

                # Geometry
                title.grid(row=0, column=0, columnspan=2)
                engEntryLabel.grid(row=1, column=0)
                engEntry.grid(row=1, column=1)
                freEntryLabel.grid(row=2, column=0)
                freEntry.grid(row=2, column=1)
                pluralEntryLabel.grid(row=3, column=0)
                pluralEntry.grid(row=3, column=1)
                genderEntryLabel.grid(row=4, column=0)
                genderEntry.grid(row=4, column=1)
                goButton.grid(row=5, column=0, columnspan=2)

            elif radioVariable.get() == "adjective":
                # Usual shit
                newEng = ""
                newFre = ""
                newPluralEnd = ""
                newFemEnd = ""

                # button callback
                def goButtonCallback():
                    newEng = engEntry.get()
                    newFre = freEntry.get()
                    newPluralEnd = pluralEntry.get()
                    newFemEnd = femEntry.get()
                    self.adjectiveList.append(Adjective(newEng, newFre, newPluralEnd, newFemEnd))
                    # Code to add it to DB
                    messagebox.showinfo("Done!", "Added adjective " + newFre + "!")
                    newWin2.quit()
                    return
                # Widgets
                title = Label(newWin2, text="Adjective", font=("Helvetica"))

                engEntryLabel = Label(newWin2, text="English:", font=("Helvetica"))
                engEntry = Entry(newWin2, font=("Helvetica"))

                freEntryLabel = Label(newWin2, text="French:", font=("Helvetica"))
                freEntry = Entry(newWin2, font=("Helvetica"))

                pluralEntryLabel = Label(newWin2, text="Plural Ending:", font=("Helvetica"))
                pluralEntry = Entry(newWin2, font=("Helvetica"))

                femEntryLabel = Label(newWin2, text="Feminine Ending:", font=("Helvetica"))
                femEntry = Entry(newWin2, font=("Helvetica"))

                goButton = Button(newWin2, text="Next", command=goButtonCallback)

                # Geometry
                title.grid(row=0, column=0, columnspan=2)
                engEntryLabel.grid(row=1, column=0)
                engEntry.grid(row=1, column=1)
                freEntryLabel.grid(row=2, column=0)
                freEntry.grid(row=2, column=1)
                pluralEntryLabel.grid(row=3, column=0)
                pluralEntry.grid(row=3, column=1)
                femEntryLabel.grid(row=4, column=0)
                femEntry.grid(row=4, column=1)
                goButton.grid(row=5, column=0, columnspan=2)
            else:
                # misc
                newEng = ""
                newFre = ""
                newCom = ""

                # Callback
                def goButtonCallback():
                    newEng = engEntry.get()
                    newFre = freEntry.get()
                    newCom = comEntry.get()

                    newMisc = Misc(newEng, newFre)
                    newMisc.commentText = newCom

                    self.miscWordList.append(newMisc)
                    # Code to add to db
                    messagebox.showinfo("Done!", "Added misc word " + newFre + "!")
                    newWin2.quit()
                    return
                # Widgets
                title = Label(newWin2, text="Miscelaneous Word", font=("Helvetica"))

                engEntryLabel = Label(newWin2, text="English:", font=("Helvetica")) # This code could probably be declared before the if statement but o well
                engEntry = Entry(newWin2, font=("Helvetica"))

                freEntryLabel = Label(newWin2, text="French:", font=("Helvetica"))
                freEntry = Entry(newWin2, font=("Helvetica"))

                comScrollbar = Scrollbar(newWin2)
                comEntryLabel = Label(newWin2, text="Comment:", font=("Helvetica"))
                comEntry = Entry(newWin2, font=("Helvetica"), xscrollcommand=comScrollbar.get)
                comScrollbar.config(command=comEntry.xview)

                goButton = Button(newWin2, text="Next", command=goButtonCallback)
                
            newWin2.mainloop()

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
