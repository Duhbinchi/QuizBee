from tkinter import * ; from tkinter import messagebox
import random
import winsound
from windowDrag import DraggableWindow

class GameWindow(Tk, DraggableWindow):
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

        # Dictionary for questions and answers
        self.questionDict = self.loadQuestions()
        
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
    def loadQuestions(self):
        questionDict = {}

        try:
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
            questionItems = list(questionDict.items())  # Convert to list for shuffling
            random.shuffle(questionItems)
            return dict(questionItems)  # Convert back to dictionary
        
        except FileNotFoundError:
            messagebox.showerror("Error", "Questions file not found.")
            return {}


    def shuffleAndPackButtons(self, buttonList):
        random.shuffle(buttonList)
        for button in buttonList:
            button.pack(fill=X)


    def checkAnswer(self, selectedAnswer):
        # Based on dictionary
        currentQuestion = list(self.questionDict.keys())[self.counter]
        correctAnswer = self.questionDict[currentQuestion]['optA']  # A is always the correct answer
    
        if selectedAnswer == correctAnswer:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            self.score += 1
            self.scoreLabel.config(text=f"Score: {self.score}")
            self.hp = min(self.hp + 1, 5) # HP cannot exceed 5
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)
            self.hp = max(self.hp - 1, 0) # HP cannot be negative
    
        # Check if you died
        if self.hp == 0:
            self.healthStatus(self.hp)

            # Check if the game is over and ask if user wants to retry or destroy the application
            response = messagebox.askquestion("Game Over", "You ran out of health points. Would you like to retry?")
            
            if response == 'yes':
                # Reset the game variables
                self.counter = -1 ; self.hp = 5 ; self.score = 0
                self.scoreLabel.config(text=f"Score: {self.score}")
                self.healthStatus(self.hp)
                self.nextQuestion()
            else:
                self.gameFinish(self.hp)
                self.destroy()

        else:
            if self.counter >= 50:
                # Check if the player has answered all questions
                self.gameFinish(self.hp)
            else:
                self.healthStatus(self.hp)
                self.nextQuestion()

        
    def healthStatus(self, hp):
        try:
            # Update the HP image based on the current HP
            self.photoHP.config(file=f'hp{hp}.png')  
            self.hpLabel.config(image=self.photoHP, bg='orange')
        except:
            pass
        

    def nextQuestion(self):
        self.counter += 1 # initial value is -1 so it will be 0 (first question)

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
        if hp == 0: # Lost
            messagebox.showerror("Game Over - Ran out of HP", "You ran out of health points. Game Over.")
        else: # Won
            messagebox.showinfo("Finished!", "You have completed the quiz!")
        
        self.showScore()
        self.destroy()

    
    def showScore(self):
        messagebox.showinfo("Score", f"Your score is {self.score} out of 50.")

   