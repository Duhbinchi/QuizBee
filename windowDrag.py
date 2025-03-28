from tkinter import messagebox

class DraggableWindow:
    # Since the titlebar is removed, this module is made to drag/move the window  
    def startMove(self, event):
        self._offsetX = event.x
        self._offsetY = event.y


    def doMove(self, event):
        x = self.winfo_pointerx() - self._offsetX
        y = self.winfo_pointery() - self._offsetY
        self.geometry(f"+{x}+{y}")


    def exit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()