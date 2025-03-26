"""
TO DO: 
- 

Suggestions / Comments / Questions:
- Remove the title bar in the Login Window and Game Window / Window Resizable to False
- Make it into OOP-like more in a sense more functions and the code is more organized
- Shuffle the questions order as well?
"""


from tkinter import *
import random
from tkinter import messagebox

class ITQuizBeeLogin(Tk):
    def __init__(self):
        super().__init__()

        self.title("Log In")
        self.labelLog = Label(self)

        self.photoLogInImage = PhotoImage(file='logIN20.png')
        self.photoButtonOK = PhotoImage(file='OK20.png')
        self.labelLog.config(image=self.photoLogInImage)

        # Name
        self.entryTxtUname = Entry(self, fg='white',bg='brown', width=28)
        self.entryTxtPw = Entry(self, fg='white',bg='brown',width=28) # HIDE


        # Buttons
        self.btnQuit = Button(self, text='x', command=self.exit)
        self.btnOk = Button(self, image=self.photoButtonOK, bg='lime',command=self.validate)

        # Placement
        self.labelLog.pack()

        self.entryTxtUname.place(x=35,y=101)
        self.entryTxtPw.place(x=35,y=161)

        self.btnQuit.place(x=195,y=30)
        self.btnOk.place(x=97,y=191)

    
    def exit(self):
        pass

    def validate(self):
        # open the game window
        self.destroy()
        game = GameWindow()
        game.mainloop()


class GameWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("IT Quiz Bee")
        self.counter = 0  

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

        self.photoGameImage = PhotoImage(file='bgQuiz50.png')
        self.labelGame = Label(self, bg='orange')
        self.labelGame.config(image=self.photoGameImage)

        self.gameFrame = Frame(self, bg='orange', width=1005, height=739)
        self.hpLabel = Label(self.gameFrame, bg='orange')
        self.photoHP = PhotoImage(file='hp5.png')
        self.hpLabel.config(image=self.photoHP)

        first_question_key = list(self.questionDict.keys())[0]  # Get the first question key
        
        self.labelQuestion = Label(self.gameFrame, text=self.questionDict[first_question_key]['question'],  font='Arial 20 bold', fg='white', height=7, bg='orange', justify=CENTER, wraplength=400)
        self.answerButtonA = Button(self.gameFrame, text='A', font='Arial 20 bold', fg='white', bg='brown', width=15, command=self.nextQuestion)
        self.answerButtonB = Button(self.gameFrame, text='B', font='Arial 20 bold', fg='white', bg='brown', width=15, command=self.nextQuestion)
        self.answerButtonC = Button(self.gameFrame, text='C', font='Arial 20 bold', fg='white', bg='brown', width=15, command=self.nextQuestion)
        self.answerButtonD = Button(self.gameFrame, text='D', font='Arial 20 bold', fg='white', bg='brown', width=15, command=self.nextQuestion)

        # Placement
        self.labelGame.pack()
        self.gameFrame.place(x=186, y=65, anchor=NW)
        self.hpLabel.pack(side=TOP)
        self.labelQuestion.pack(side=TOP)


        buttonList = [self.answerButtonA, self.answerButtonB, self.answerButtonC, self.answerButtonD]
        random.shuffle(buttonList)
        for button in buttonList:
            button.pack(fill=X)


    def nextQuestion(self):
        self.counter += 1
        try:
            # Get the next question and answers
            question, answer = list(self.questionDict.items())[self.counter]
            self.labelQuestion.config(text=answer['question'])
            
            # Create a list of buttons with their corresponding answers
            buttonList = [
                (self.answerButtonA, answer['optA']),
                (self.answerButtonB, answer['optB']),
                (self.answerButtonC, answer['optC']),
                (self.answerButtonD, answer['optD']),
            ]
            
            # Clear the current button layout
            for button, _ in buttonList:
                button.pack_forget()
            
            # Shuffle the buttons
            random.shuffle(buttonList)
            
            # Re-pack buttons in random order
            for button, text in buttonList:
                button.config(text=text)
                button.pack(fill=X)
        except IndexError:
            # Reset the counter, messagebox informing the user that the quiz is reset
            self.counter = 0
            messagebox.showinfo("Start Over", "Quiz is reset to the first question.")

        
        
    def checkAnswer(self):
        # moves to next question
        pass

        

if __name__ == "__main__":
    app = ITQuizBeeLogin()
    app.mainloop()