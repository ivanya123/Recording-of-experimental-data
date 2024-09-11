import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os
import json

from data_constant import *
from function_recording.function import *


def first_start():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            file_path = json.load(f)
            return file_path['path']
    else:
        file_path = {'path': filedialog.askopenfilename()}
        with open('config.json', 'w') as f:
            json.dump(file_path, f)
        return file_path['path']


class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Запись данных об износе")
        self.geometry("500x500")

        self.file_data = first_start()

        self.list_material = get_material(self.file_data)
        self.list_coating = get_coating(self.file_data)
        self.list_tool = get_tool(self.file_data)

        self.frame_material = tk.LabelFrame(self, text="Материал")
        self.frame_material.pack(padx=5, pady=5)
        self.listbox_material = ttk.Combobox(self.frame_material, values=self.list_material)
        self.listbox_material.set(self.list_material[0])
        self.listbox_material.grid(row=0, column=0, padx=5, pady=5)
        self.material_add = tk.Button(self.frame_material, text="Добавить материал")
        self.material_add.grid(row=0, column=1, padx=5, pady=5)

        self.frame_coating = tk.LabelFrame(self, text="Покрытие")
        self.frame_coating.pack(padx=5, pady=5)
        self.listbox_coating = ttk.Combobox(self.frame_coating, values=self.list_coating)
        self.listbox_coating.set(self.list_coating[0])
        self.listbox_coating.grid(row=0, column=0, padx=5, pady=5)
        self.coating_add = tk.Button(self.frame_coating, text="Добавить покрытие")
        self.coating_add.grid(row=0, column=1, padx=5, pady=5)

        self.frame_tool = tk.LabelFrame(self, text="Инструмент")
        self.frame_tool.pack(padx=5, pady=5)
        self.listbox_tool = ttk.Combobox(self.frame_tool, values=self.list_tool)
        self.listbox_tool.set(self.list_tool[0])
        self.listbox_tool.grid(row=0, column=0, padx=5, pady=5)
        self.tool_add = tk.Button(self.frame_tool, text="Добавить инструмент")
        self.tool_add.grid(row=0, column=1, padx=5, pady=5)

        self.frame_section = tk.LabelFrame(self, text="Сечение")
        self.frame_section.pack(padx=5, pady=5)

        self.text_a = tk.Entry(self.frame_section)
        self.text_a.insert(0, '5')
        self.text_a.pack(padx=5, pady=5)

        self.text_b = tk.Entry(self.frame_section, textvariable='1.5')
        self.text_b.insert(0, '1.5')
        self.text_b.pack(padx=5, pady=5)

        self.frame_piece = tk.LabelFrame(self, text="Длина заготовки")
        self.frame_piece.pack(padx=5, pady=5)

        self.entry_piece = tk.Entry(self.frame_piece)
        self.entry_piece.pack(padx=5, pady=5)

        self.button_new_experiment = tk.Button(self, text="Начать запись нового эксперимента",
                                               command=self.on_click)
        self.button_new_experiment.pack(padx=5, pady=5)

        self.entry_piece.focus()

    def on_click(self):
        material = self.listbox_material.get()
        coating = self.listbox_coating.get()
        tool = self.listbox_tool.get()

        if check_float(self.entry_piece.get()) and check_float(self.text_a.get()) and check_float(self.text_b.get()):
            length_piece = float(self.entry_piece.get())
            a = float(self.text_a.get())
            b = float(self.text_b.get())
            window = NewExperiment(material, coating, tool, length_piece, a, b)
            window.grab_set()
        else:
            messagebox.showerror("Ошибка", "Введите корректные данные")


class NewExperiment(tk.Toplevel):

    def __init__(self,
                 material: str,
                 coating: str,
                 tool: str,
                 length_piece: float,
                 a: float,
                 b: float):
        super().__init__()
        self.geometry("500x500")
        self.title("Запись данных об износе")

        self.material = material
        self.coating = coating
        self.tool = tool
        self.length_piece = length_piece
        self.a = a
        self.b = b
        self.text_title = (f"Материал: {material}, Покрытие: {coating}, Инструмент: {tool}\n"
                           f"Длина заготовки: {length_piece} мм, Сечение(axb): {a}мм x {b}мм")

        self.label_title = tk.Label(self, text=self.text_title)
        self.label_title.pack(padx=5, pady=5)

        self.frame_experimen = tk.LabelFrame(self, text="Количество проходов")
        self.frame_experimen.pack(padx=5, pady=5)
        self.spin_passage = tk.Spinbox(self.frame_experimen, from_=1, to=140, width=10)
        self.spin_passage.grid(row=0, column=0, padx=5, pady=5)
        self.spin_passage.bind('<MouseWheel>', lambda event: plus(event, self.spin_passage))
        self.spin_passage['state'] = 'readonly'

        def plus(event, spinbox):
            if event.delta < 0:
                spinbox['state'] = 'normal'
                num = int(spinbox.get())
                spinbox.delete(0, len(spinbox.get()))
                if num > 1:
                    spinbox.insert(0, num - 1)
                    spinbox['state'] ='readonly'
                else:
                    spinbox.insert(0, num)
                    spinbox['state'] = 'readonly'

            else:
                spinbox['state'] = 'normal'
                num = int(spinbox.get())
                spinbox.delete(0, len(spinbox.get()))
                spinbox.insert(0, num + 1)
                spinbox['state'] = 'readonly'

        self.frame_wear = tk.LabelFrame(self, text="Величина износа (мкм)")


if __name__ == '__main__':
    app = Main()
    app.mainloop()
