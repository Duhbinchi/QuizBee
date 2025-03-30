"""
Note: Username = TechWizard and Password = admin

TO DO (base requirements): 
- Make code more OOP and organized

TO DO (additional requirements):
- Toggle the password visibility when the user clicks a button
- Testing

Suggestions / Comments / Questions:
- Show Player Name and Their Previous Highscore
- Dynamic Leaderboard
- Note: "Add kayo dito if you have any suggestions or comments"

"""


from tkinter import *
from tkinter import messagebox
import winsound
import random

class ITQuizBeeLogin(Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.overrideredirect(True)
        self.geometry("+500+150")

        # Initialize the login dictionary
        self.logInDict = self.loadUserAccounts()

        # Make the window background transparent
        self.wm_attributes('-transparentcolor', 'maroon')
        self.title("Log In")
        self.labelLog = Label(self, bg='maroon')
        self.inputFont = ('Arial', 8)
        self.photoLogInImage = PhotoImage(file='logIN20.png')
        self.photoButtonOK = PhotoImage(file='OK20.png')
        self.labelLog.config(image=self.photoLogInImage)

        # Name and Password
        self.entryTxtUname = Entry(self, fg='white', bg='brown', width=28, font=self.inputFont)
        self.entryTxtPw = Entry(self, fg='white', bg='brown', width=28, font=self.inputFont, show="*")  # Hides password input

        # Buttons
        self.btnQuit = Button(self, text='X', command=self.exit, borderwidth=0)
        self.btnOk = Button(self, image=self.photoButtonOK, bg='lime', command=self.validate)
        self.bind('<Return>', self.validate)

        # Extra: Dragging the window
        self.labelLog.bind("<ButtonPress-1>", self.startMove)
        self.labelLog.bind("<B1-Motion>", self.doMove)

        # Placement
        self.labelLog.pack()
        self.entryTxtUname.place(x=35, y=101)
        self.entryTxtPw.place(x=35, y=161)
        self.btnQuit.place(x=195, y=30)
        self.btnOk.place(x=97, y=191)


    def loadUserAccounts(self):
        logInDict = {}
        try:
            with open("UserAccount.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    parts = line.split(";")
                    if len(parts) >= 2:
                        username = parts[0].strip()
                        storedPassword = parts[1].strip()
                        logInDict[username] = storedPassword

        except FileNotFoundError:
            messagebox.showerror("Error", "No user accounts found.")

        return logInDict

    def validate(self, event=None):  # event=None is for the bind function
        enteredUsername = self.entryTxtUname.get().strip()
        enteredPassword = self.entryTxtPw.get().strip()

        if enteredUsername in self.logInDict and self.logInDict[enteredUsername] == enteredPassword:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.destroy()
            game = GameWindow()
            game.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def exit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()

    # Functions for dragging the window
    # Modify this later so it can inherit from the parent class
    def startMove(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def doMove(self, event):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")

    def exit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()

class GameWindow(Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes('-transparentcolor', 'maroon') 
        self.resizable(False, False)
        self.title("IT Quiz Bee")

        # Variables
        self.counter = -1 # Counter for the questions
        self.hp = 5
        self.score = 0

        self.questionDict = {}
        with open('QandA.txt', 'r') as f:
            for line in f:
                lines = line.strip().split(';')
                self.questionDict[lines[0]] = {
                    'question': lines[0],
                    'optA': lines[1],
                    'optB': lines[2],
                    'optC': lines[3],
                    'optD': lines[4]
                }
        
        # Shuffle the questions
        questionItems = list(self.questionDict.items()) # turns it into a list so that shuffle can be used
        random.shuffle(questionItems) 
        self.questionDict = dict(questionItems) 

        # Images
        self.photoGameImage = PhotoImage(file='bgQuiz50.png')
        self.labelGame = Label(self, bg='maroon')
        self.labelGame.config(image=self.photoGameImage)
        self.scoreLabel = Label(self, text=f"Score: {self.score}", font='Arial 15 bold', bg='#d37537', fg='white', relief="raised")

        self.gameFrame = Frame(self, bg='orange', width=1005, height=739) # Scaling issues depending screen size of the computer
        self.hpLabel = Label(self.gameFrame, bg='orange')
        self.photoHP = PhotoImage(file='hp5.png')
        self.hpLabel.config(image=self.photoHP)

        # Button and Questions
        self.quitButton = Button(self, text='X', fg='white', font="Times 12 bold", bg='#406e5c', relief="raised",command=self.exit)
        self.labelQuestion = Label(self.gameFrame,  font='Arial 20 bold', fg='white', height=7, bg='orange', justify=CENTER, wraplength=400)
        self.answerButtonA = Button(self.gameFrame, font='Times 18 bold', bg='brown', fg='white', activebackground='lime')
        self.answerButtonB = Button(self.gameFrame, font='Times 18 bold', bg='brown', fg='white', activebackground='red')
        self.answerButtonC = Button(self.gameFrame, font='Times 18 bold', bg='brown', fg='white', activebackground='red')
        self.answerButtonD = Button(self.gameFrame, font='Times 18 bold', bg='brown', fg='white', activebackground='red')
        
        # Placement
        self.labelGame.pack()
        self.scoreLabel.place(x=73, y=86)
        self.gameFrame.place(x=186, y=85, anchor=NW)
        self.quitButton.place(x=922, y=70)
        self.hpLabel.pack(side=TOP)
        self.labelQuestion.pack(side=TOP)
        self.nextQuestion()  # Call nextQuestion to display the first question

        # Extra: Dragging the window
        self.labelGame.bind("<ButtonPress-1>", self.startMove)
        self.labelGame.bind("<B1-Motion>", self.doMove)


    # Functions
    def shuffleAndPackButtons(self, buttonList):
        random.shuffle(buttonList)
        for button in buttonList:
            button.pack(fill=X)


    def checkAnswer(self, isCorrect):
        if isCorrect:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            self.score += 1
            self.scoreLabel.config(text=f"Score: {self.score}")
            self.hp = min(self.hp + 1, 5)  # HP cannot exceed 5
            
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)
            self.hp = max(self.hp - 1, 0)  # HP cannot be negative
    
        # Check if the game is over
        if self.hp == 0:
            self.healthStatus(self.hp)
            self.gameFinish(self.hp)

        else:
            # Check if player answered all questions
            if self.counter >= 50: 
                self.gameFinish(self.hp)
            else:
                self.nextQuestion()
    
        self.healthStatus(self.hp)

        
    def healthStatus(self, hp):
        try:
            # Update the HP image based on the current HP
            self.photoHP.config(file=f'hp{hp}.png')  
            self.hpLabel.config(image=self.photoHP, bg='orange')
        except:
            pass
        

    def nextQuestion(self):
        self.counter += 1 # initial vallue is -1 so it will be 0 (first question)

        try:
            currentQuestionKey = list(self.questionDict.keys())[self.counter]
            currentQuestion = self.questionDict[currentQuestionKey]

            # Medyo nakakalito, but based toh so dictionary
            self.labelQuestion.config(text=currentQuestion['question'])

            # Update buttons appropriate commands... because earlier, the commands were set to the first question only
            newButtons = [
                (self.answerButtonA, currentQuestion['optA'], True),
                (self.answerButtonB, currentQuestion['optB'], False),
                (self.answerButtonC, currentQuestion['optC'], False),
                (self.answerButtonD, currentQuestion['optD'], False)
            ]

            random.shuffle(newButtons)
            
            # Clear old buttons
            oldButtons = [self.answerButtonA, self.answerButtonB, self.answerButtonC, self.answerButtonD]   
            for button in oldButtons:
                button.pack_forget()
            
            # Repack shuffled buttons with updated commands
            for btn, text, correct in newButtons:
                btn.config(text=text, command=lambda c=correct: self.checkAnswer(c))
                btn.pack(fill=X)
    
        except IndexError:
            # If the counter exceeds the number of questions, the game is over. The player wins but it's called gameFinish because it's the end of the game
            self.gameFinish(self.hp)

    
    def gameFinish(self, hp ):
        messageTitle = ""
        scoreMessage = f"Your score is {self.score} out of 50."

        if hp == 0: # Lost
            messageTitle = "Game Over! - Ran out of HP"
        else: # Won
            messageTitle = "Congratulations! - You answered all questions!"

        # Ask if the player wants to retrys     
        response = messagebox.askquestion(messageTitle, f"{scoreMessage}\nWould you like to retry?")
        if response == 'yes':
            self.hp = 5 ; self.score = 0 ; self.counter = -1
            self.scoreLabel.config(text=f"Score: {self.score}")
            self.healthStatus(self.hp)
            self.nextQuestion()
        else:
            self.destroy()


    # Functions for dragging the window
    # Modify this later so it can inherit from the parent class
    def startMove(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def doMove(self, event):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")

    def exit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()

        
if __name__ == "__main__":
    app = ITQuizBeeLogin()
    app.mainloop()