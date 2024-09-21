import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from data_constant import *

dict_add_function = {
    'Материал': add_material,
    'Покрытие': add_coating,
    'Инструмент': add_tool,
    'Этап': add_stage,
}


class AddConstant(tk.Toplevel):
    """
    Класс для создания окна добавления нового постоянного элемента (константы).

    Окно позволяет пользователю ввести новый материал, покрытие, инструмент или этап
    и добавить его в соответствующий файл данных.

    Наследует от tk.Toplevel для создания отдельного всплывающего окна.
    """
    def __init__(self, type_, file_name):
        """
        Инициализирует окно добавления константы.

        :param type_: Строка, определяющая тип добавляемого элемента ('Материал', 'Покрытие', 'Инструмент', 'Этап').
        :param file_name: Имя файла, в который будет сохранен новый элемент.
        """
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
        """
        Обрабатывает добавление нового элемента.

        Вызывает соответствующую функцию добавления из словаря dict_add_function,
        передавая ей введенное пользователем значение и имя файла. Затем закрывает окно.

        :param event: Событие, вызвавшее функцию (по умолчанию None).
        """
        dict_add_function[self.type_](self.entry.get(), self.file_name)
        self.destroy()
