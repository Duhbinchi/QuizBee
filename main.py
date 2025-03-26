"""
Note: Username = TechWizard and Password = admin

TO DO (base requirements): 
- Score System
- Login (check if working)
- Handling this: For some reason, the hp 0 is a jpg file ??

Suggestions / Comments / Questions:
- Make it into OOP-like more in a sense more functions and the code is more organized
- Shuffle the questions order as well?
- Font for the Login = Arial 20 bold
- Bind Enter key to the OK button

- HP bar has a white space when changed idk why
- Reason: Some images have transparent background, some don't...
"""


from tkinter import *
from tkinter import messagebox
import random

class ITQuizBeeLogin(Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)

        self.title("Log In")
        self.labelLog = Label(self)
        self.inputFont = ('Arial', 8)

        self.photoLogInImage = PhotoImage(file='logIN20.png')
        self.photoButtonOK = PhotoImage(file='OK20.png')
        self.labelLog.config(image=self.photoLogInImage)

        # Name and Password
        self.entryTxtUname = Entry(self, fg='white', bg='brown', width=28, font=self.inputFont)
        self.entryTxtPw = Entry(self, fg='white', bg='brown', width=28, font=self.inputFont, show="*")  # Hides password input

        # Buttons
        self.btnQuit = Button(self, text='x', command=self.exit)
        self.btnOk = Button(self, image=self.photoButtonOK, bg='lime', command=self.validate)
        self.bind('<Return>', self.validate)

        # Placement
        self.labelLog.pack()
        self.entryTxtUname.place(x=35, y=101)
        self.entryTxtPw.place(x=35, y=161)
        self.btnQuit.place(x=195, y=30)
        self.btnOk.place(x=97, y=191)

    # Functions
    def exit(self):
        messagebox.askokcancel("Quit", "Are you sure you want to quit?")
        if messagebox.askokcancel:
            self.destroy()

    def validate(self, event=None): # event=None is for the bind function
        enteredUsername = self.entryTxtUname.get().strip()  
        enteredPassword = self.entryTxtPw.get().strip()    

        logInDict = {}
        try:
            with open("UserAccount.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(";")
                        if len(parts) >= 2:
                            username = parts[0].strip()
                            stored_password = parts[1].strip()
                            logInDict[username] = stored_password

        except FileNotFoundError:
            messagebox.showerror("Error", "No user accounts found. Please register first.")
            return

        if enteredUsername in logInDict and logInDict[enteredUsername] == enteredPassword:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.destroy()
            game = GameWindow()
            game.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")



class GameWindow(Tk):
    def __init__(self):
        super().__init__()
        
        self.resizable(False, False)

        self.title("IT Quiz Bee")
        self.counter = -1 # Counter for the questions
        self.hp = 5

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

        # Images
        self.photoGameImage = PhotoImage(file='bgQuiz50.png')
        self.labelGame = Label(self, bg='orange')
        self.labelGame.config(image=self.photoGameImage)

        self.gameFrame = Frame(self, bg='orange', width=1005, height=739)
        self.hpLabel = Label(self.gameFrame, bg='orange')
        self.photoHP = PhotoImage(file='hp5.png')
        self.hpLabel.config(image=self.photoHP)

        # Button and Questions
        self.labelQuestion = Label(self.gameFrame,  font='Arial 20 bold', fg='white', height=7, bg='orange', justify=CENTER, wraplength=400)
        self.answerButtonA = Button(self.gameFrame, font='Arial 20 bold', bg='brown', fg='white', activebackground='lime', command=lambda: self.checkAnswer(self.questionDict[firstQuestion]['optA']))
        self.answerButtonB = Button(self.gameFrame, font='Arial 20 bold', bg='brown', fg='white', activebackground='red', command=lambda: self.checkAnswer(self.questionDict[firstQuestion]['optB']))
        self.answerButtonC = Button(self.gameFrame, font='Arial 20 bold', bg='brown', fg='white', activebackground='red', command=lambda: self.checkAnswer(self.questionDict[firstQuestion]['optC']))
        self.answerButtonD = Button(self.gameFrame, font='Arial 20 bold', bg='brown', fg='white', activebackground='red', command=lambda: self.checkAnswer(self.questionDict[firstQuestion]['optD']))
        
        # Placement
        self.labelGame.pack()
        self.gameFrame.place(x=186, y=65, anchor=NW)
        self.hpLabel.pack(side=TOP)
        self.labelQuestion.pack(side=TOP)
        buttonList = [self.answerButtonA, self.answerButtonB, self.answerButtonC, self.answerButtonD]
        self.nextQuestion()  # Call nextQuestion to display the first question


    # Functions
    def shuffleAndPackButtons(self, buttonList):
        random.shuffle(buttonList)
        for button in buttonList:
            button.pack(fill=X)


    def checkAnswer(self, selectedAnswer):
        currentQuestion = list(self.questionDict.keys())[self.counter]
        correctAnswer = self.questionDict[currentQuestion]['optA']  # A is always the correct answer
    
        if selectedAnswer == correctAnswer:
            messagebox.showinfo("Correct!", "You selected the correct answer!")
            self.hp = min(self.hp + 1, 5) # HP cannot exceed 5
        else:
            messagebox.showerror("Wrong!", "That's not the correct answer.")
            self.hp = max(self.hp - 1, 0) # HP cannot be negative
    
        # Check if the game is over
        if self.hp == 0:
            self.healthStatus(self.hp)
            self.gameOver(self.hp)
        else:
            self.nextQuestion()

        self.healthStatus(self.hp)


    def healthStatus(self, hp):
        # Update the HP image based on the current HP
        try:
            self.photoHP.config(file=f'hp{hp}.png')  
        except:
            pass
            # self.photoHP.config(file='hp0.jpg')  # For some reason, the hp 0 is a jpg file ???

        self.hpLabel.config(image=self.photoHP, bg='orange')


    def nextQuestion(self):
        self.counter += 1

        try:
            currentQuestionKey = list(self.questionDict.keys())[self.counter]
            currentQuestion = self.questionDict[currentQuestionKey]

            # Medyo nakakalito, but based to so dictionary
            self.labelQuestion.config(text=currentQuestion['question'])

            # Update buttons appropriate commands... because earlier, the commands were set to the first question only
            newButtons = [
                (self.answerButtonA, currentQuestion['optA'], currentQuestion['optA']),
                (self.answerButtonB, currentQuestion['optB'], currentQuestion['optB']),
                (self.answerButtonC, currentQuestion['optC'], currentQuestion['optC']),
                (self.answerButtonD, currentQuestion['optD'], currentQuestion['optD'])
            ]

            random.shuffle(newButtons)
            
            # Clear old buttons and repack with new commands
            oldButtons = [self.answerButtonA, self.answerButtonB, self.answerButtonC, self.answerButtonD]   
            for button in oldButtons:
                button.pack_forget()
            
            # Repack shuffled buttons with updated commands
            for btn, text, correct in newButtons:
                btn.config(text=text, 
                          command=lambda c=correct: self.checkAnswer(c))
                btn.pack(fill=X)
    
        except IndexError:
            self.gameOver(self.hp)

    
    def gameOver(self, hp ):
        if hp == 0:
            messagebox.showerror("Game Over - Ran out of HP", "You ran out of health points. Game Over.")
        else:
            messagebox.showinfo("Finished!", "You have completed the quiz!")
            self.showScore()

        self.destroy()

    
    def showScore(self):
        pass

        
if __name__ == "__main__":
    app = ITQuizBeeLogin()
    app.mainloop()