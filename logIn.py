from tkinter import * ; from tkinter import messagebox
from game import GameWindow
from windowDrag import DraggableWindow


class ITQuizBeeLogin(Tk, DraggableWindow):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.overrideredirect(True)
        self.geometry("+500+150")

        # Private login dictionary
        self._logInDict = self._loadUserAccounts()

        # Make the window background transparent
        self.wm_attributes('-transparentcolor', 'maroon')
        self.title("Log In")
        self.labelLog = Label(self, bg='maroon')
        self.inputFont = ('Arial', 8)
        self.photoLogInImage = PhotoImage(file='logIN20.png')
        self.photoButtonOK = PhotoImage(file='OK20.png')
        self.labelLog.config(image=self.photoLogInImage)

        try:
            self.hidePass = PhotoImage(file='hidePass.png')
        except:
            self.hidePass = None

        # Name and Password
        self.txtUname = Entry(self, fg='white', bg='brown', width=28, font=self.inputFont)
        self.txtPw = Entry(self, fg='white', bg='brown', width=28, font=self.inputFont, show="*")  # Hides password input

        # Buttons
        self.btnQuit = Button(self, text='X', command=self.exit, borderwidth=0)
        self.btnOk = Button(self, image=self.photoButtonOK, bg='lime', command=self.validate)
        self.bind('<Return>', self.validate)

        if self.hidePass:
            self.btnShow = Button(self, image=self.hidePass, bg='brown', width=16, height=16)
            self.btnShow.place(x=187,y=158)
        else:
            self.btnShow = Button(self, text='Show', bg='brown', fg='white')
            self.btnShow.place(x=170,y=156)

        self.btnShow.bind('<ButtonPress-1>', lambda event: self.show())
        self.btnShow.bind('<ButtonRelease-1>', lambda event: self.hide())

        # Extra: Dragging the window
        self.labelLog.bind("<ButtonPress-1>", self.startMove)
        self.labelLog.bind("<B1-Motion>", self.doMove)

        # Placement
        self.labelLog.pack()
        self.txtUname.place(x=35, y=101)
        self.txtPw.place(x=35, y=161)
        self.btnQuit.place(x=195, y=30)
        self.btnOk.place(x=97, y=191)


    # Private method to load user accounts
    def _loadUserAccounts(self):
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


    def validate(self, event=None):
        enteredUsername = self.txtUname.get().strip()
        enteredPassword = self.txtPw.get().strip()

        if enteredUsername in self._logInDict and self._logInDict[enteredUsername] == enteredPassword:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.destroy()
            game = GameWindow()
            game.mainloop()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            

    def show(self):
        self.txtPw.config(show='')
        

    def hide(self):
        self.txtPw.config(show='*')
