from tkinter import *

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
        self.btnOk = Button(self, image=self.photoButtonOK, command=self.validate)

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
        # self.attributes('-fullscreen', True)

        self.photoGameImage = PhotoImage(file='bgQuiz50.png')
        self.labelGame = Label(self)
        self.labelGame.config(image=self.photoGameImage)

        self.gameFrame = Frame(self, bg='orange', width=1005, height=739)
        self.hpLabel = Label(self.gameFrame, bg='orange')
        self.photoHP = PhotoImage(file='hp5.png')
        self.hpLabel.config(image=self.photoHP)

        self.labelQuestion = Label(self.gameFrame, text='', font='Arial 20 bold', fg='white', height=7, bg='orange', justify=CENTER)
        self.answerButtonA = Button(self.gameFrame, text='A', font='Arial 20 bold', fg='white', bg='brown', width=15,command=self.checkAnswer, value='correct')
        self.answerButtonB = Button(self.gameFrame, text='B', font='Arial 20 bold', fg='white', bg='brown', width=15, command=self.checkAnswer, value='wrong')
        self.answerButtonC = Button(self.gameFrame, text='C', font='Arial 20 bold', fg='white', bg='brown', width=15, command=self.checkAnswer, value='wrong')
        self.answerButtonD = Button(self.gameFrame, text='D', font='Arial 20 bold', fg='white', bg='brown', width=15, command=self.checkAnswer, value='wrong')



        questionDict = {}
        with open('QandA.txt', 'r') as f:
            for line in f:
                lines = line.strip().split(';')
                
                questionDict[lines[0]] = {
                    'question': lines[0],
                    'optA': lines[1],
                    'optB': lines[2],
                    'optC': lines[3],
                    'optD': lines[4]
                }            

        # Create question dynamically for each item
        for question,answer in questionDict.items():
            self.labelQuestion.config(text=answer['question'])
            self.answerButtonA.config(text=answer['optA'])
            self.answerButtonB.config(text=answer['optB'])
            self.answerButtonC.config(text=answer['optC'])
            self.answerButtonD.config(text=answer['optD'])

        # Placement
        self.labelGame.pack()
        self.gameFrame.place(x=320,y=65)
        self.hpLabel.pack(side=TOP)
        self.labelQuestion.pack(fill=X)
        
        # self.answerButtonA.pack(fill=X)
        # self.answerButtonB.pack(fill=X)
        # self.answerButtonC.pack(fill=X)
        # self.answerButtonD.pack(fill=X)

        import random
        # buttonList = 
        

if __name__ == "__main__":
    app = ITQuizBeeLogin()
    app.mainloop()