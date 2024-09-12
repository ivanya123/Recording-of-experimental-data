import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os
import json
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt

from data_constant import *
from function_recording.function import *
from function_recording.experiment import Experiment


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

    def add_point_(self):
        self.frame_point = tk.LabelFrame(self.canvas_point, text=f"{self.count_point + 1}")
        self.frame_point.grid(row=0, column=self.count_point + 1, padx=5, pady=5)

        self.new_spin = Spinner(self.frame_point)
        self.new_spin.pack(padx=5, pady=5)

        self.new_entry = Entry_wear(self.frame_point, 0.01)
        self.new_entry.pack(padx=5, pady=5)

        self.list_point.append((self.new_spin, self.new_entry))

        self.graphik()
        self.count_point += 1

    def graphik(self):
        self.experiment.table = self.experiment.table.drop(index=list(range(self.count_point + 1)))
        self.experiment.table.loc[0] = [0, 0, 0]
        # print(self.experiment.table)
        for point in self.list_point[:-1]:
            self.experiment.add_point(float(point[0].get()), float(point[1].get()))

        fig, ax = self.experiment.graphik()
        if self.canvas_graph:
            self.canvas_graph.get_tk_widget().destroy()
        self.canvas_graph = FigureCanvasTkAgg(fig, master=self)
        self.canvas_graph.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_graph.draw()

        plt.close()

    def __init__(self,
                 material: str,
                 coating: str,
                 tool: str,
                 length_piece: float,
                 a: float,
                 b: float):
        super().__init__()
        self.canvas_graph = None
        self.geometry("1000x500")
        self.title("Запись данных об износе")
        self.count_point = 0
        self.list_point: list[tuple[tk.Spinbox, tk.Entry]] = []

        self.material = material
        self.coating = coating
        self.tool = tool
        self.length_piece = length_piece
        self.a = a
        self.b = b
        self.text_title = (f"Материал: {material}, Покрытие: {coating}, Инструмент: {tool}\n"
                           f"Длина заготовки: {length_piece} мм, Сечение(axb): {a}мм x {b}мм")

        self.canvas_point = tk.Canvas(self, width=1000, height=200)
        self.canvas_point.pack(padx=5, pady=5)
        self.frame_point = tk.LabelFrame(self.canvas_point, text="0")
        self.frame_point.grid(row=0, column=0, padx=5, pady=5)

        self.label_title = tk.Label(self, text=self.text_title)
        self.label_title.pack(padx=5, pady=5)
        self.button_add_point = tk.Button(self, text="Добавить точку", command=self.add_point_)
        self.button_add_point.pack(padx=5, pady=5, anchor='w')
        # self.frame_experiment = tk.LabelFrame(self.canvas_point, text="Проход")
        # self.frame_experiment.pack(padx=5, pady=5, anchor='w')
        self.spin_passage = tk.Spinbox(self.frame_point, from_=1, to=140)
        self.spin_passage.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.spin_passage.bind('<MouseWheel>', lambda event: plus(event, self.spin_passage))
        self.spin_passage.index = 0

        # self.frame_wear = tk.LabelFrame(self.canvas_point, text="Износ(мкм)")
        # self.frame_wear.pack(padx=5, pady=5, anchor='w')
        self.spin_wear = tk.Entry(self.frame_point)
        self.spin_wear.insert(0, '0.05')
        self.spin_wear.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.spin_wear.bind('<MouseWheel>', lambda event, step=0.01: plus(event, self.spin_wear, step))
        self.spin_wear.index = 0

        self.list_point.append((self.spin_passage, self.spin_wear))

        self.experiment = Experiment(self.material, self.coating, self.tool, 2000, 200,
                                     self.a, self.b, self.length_piece)

    def destroy(self):
        if self.canvas_graph:
            self.canvas_graph.get_tk_widget().destroy()
        super().destroy()


class Spinner(tk.Spinbox):
    def __init__(self, master=None, step_=1, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<MouseWheel>', lambda event, step=step_: plus(event, self, func=master.master.master.graphik))
        self.insert(0, '1')


class Entry_wear(tk.Entry):

    def __init__(self, master=None, step_=1, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<MouseWheel>', lambda event, step=step_: plus(event, self, step, master.master.master.graphik))
        self.insert(0, '0.05')


class Point_frame(tk.LabelFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


if __name__ == '__main__':
    app = Main()
    app.mainloop()
