import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from data_constant import *

dict_add_function = {
    'Материал': add_material,
    'Покрытие': add_coating,
    'Инструмент': add_tool
}


class AddConstant(tk.Toplevel):
    def __init__(self, type_, file_name):
        tk.Toplevel.__init__(self)
        self.title(f"Add {type_}")
        self.geometry("300x100")
        self.type_ = type_
        self.file_name = file_name
        self.label = tk.Label(self, text=f"Впишите {type_}")
        self.label.pack(padx=5, pady=5)
        self.entry = tk.Entry(self, width=50)
        self.entry.bind("<Return>", self.add)
        self.entry.pack(padx=5, pady=5)
        self.button = tk.Button(self, text="Добавить", command=self.add)
        self.button.pack(padx=5, pady=5)
        self.entry.focus()

    def add(self, event=None):
        dict_add_function[self.type_](self.entry.get(), self.file_name)
        self.destroy()
