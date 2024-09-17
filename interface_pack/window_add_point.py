import tkinter as tk
from function_recording.function import check_float
from tkinter import messagebox
class AddPoint(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Add Point')
        self.geometry('300x100')

        self.entry = tk.Entry(self, width=100)
        self.entry.pack(padx=5, pady=5)
        self.entry.bind('<Return>', lambda e: self.new_point())
        self.entry.focus()


    def new_point(self):
        if check_float(self.entry.get()):
            self.result = self.entry.get()
            self.destroy()
        else:
            messagebox.showerror('Error', 'Введите число')




