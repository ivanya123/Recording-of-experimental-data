import tkinter.simpledialog
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os
import shelve
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

from data_constant import *
from function_recording.function import *
from function_recording.experiment import Experiment
from interface_pack.class_add import AddConstant
from interface_pack.window_add_point import AddPoint


def first_start():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            file_path = json.load(f)
            return file_path['path'], file_path['save']
    else:
        file_path = {'path': os.path.basename(filedialog.askopenfilename(title='Выберать файл констант')),
                     'save': os.path.basename(filedialog.askdirectory(title="Выберать папку для сохранения данных"))}
        with open('config.json', 'w') as f:
            json.dump(file_path, f, indent=4)
        return file_path['path'], file_path['save']


class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Запись данных об износе")
        self.geometry("500x600")

        self.file_data, self.dir_save = first_start()

        self.list_material = get_material(self.file_data)
        self.list_coating = get_coating(self.file_data)
        self.list_tool = get_tool(self.file_data)
        self.list_stage = get_stage(self.file_data)

        self.frame_material = tk.LabelFrame(self, text="Материал")
        self.frame_material.pack(padx=5, pady=5)
        self.listbox_material = ttk.Combobox(self.frame_material, values=self.list_material)
        self.listbox_material.set(self.list_material[0])
        self.listbox_material.grid(row=0, column=0, padx=5, pady=5)
        self.material_add = tk.Button(self.frame_material, text="Добавить материал",
                                      command=lambda type_='Материал': self.add_type(type_))
        self.material_add.grid(row=0, column=1, padx=5, pady=5)

        self.frame_coating = tk.LabelFrame(self, text="Покрытие")
        self.frame_coating.pack(padx=5, pady=5)
        self.listbox_coating = ttk.Combobox(self.frame_coating, values=self.list_coating)
        self.listbox_coating.set(self.list_coating[0])
        self.listbox_coating.grid(row=0, column=0, padx=5, pady=5)
        self.coating_add = tk.Button(self.frame_coating, text="Добавить покрытие",
                                     command=lambda type_='Покрытие': self.add_type(type_))
        self.coating_add.grid(row=0, column=1, padx=5, pady=5)

        self.frame_tool = tk.LabelFrame(self, text="Инструмент")
        self.frame_tool.pack(padx=5, pady=5)
        self.listbox_tool = ttk.Combobox(self.frame_tool, values=self.list_tool)
        self.listbox_tool.set(self.list_tool[0])
        self.listbox_tool.grid(row=0, column=0, padx=5, pady=5)
        self.tool_add = tk.Button(self.frame_tool, text="Добавить инструмент",
                                  command=lambda type_='Инструмент': self.add_type(type_))
        self.tool_add.grid(row=0, column=1, padx=5, pady=5)

        self.frame_stage = tk.LabelFrame(self, text="Этап")
        self.frame_stage.pack(padx=5, pady=5)
        self.listbox_stage = ttk.Combobox(self.frame_stage, values=self.list_stage)
        self.listbox_stage.set(self.list_stage[5])
        self.listbox_stage.grid(row=0, column=0, padx=5, pady=5)
        self.stage_add = tk.Button(self.frame_stage, text="Добавить этап",
                                   command=lambda type_='Этап': self.add_type(type_))
        self.stage_add.grid(row=0, column=1, padx=5, pady=5)

        self.frame_section = tk.LabelFrame(self, text="Сечение")
        self.frame_section.pack(padx=5, pady=5)

        self.text_a = tk.Entry(self.frame_section)
        self.text_a.insert(0, '5')
        self.text_a.pack(padx=5, pady=5)

        self.text_b = tk.Entry(self.frame_section)
        self.text_b.insert(0, '1.5')
        self.text_b.pack(padx=5, pady=5)

        self.frame_piece = tk.LabelFrame(self, text="Длина заготовки")
        self.frame_piece.pack(padx=5, pady=5)

        self.entry_piece = tk.Entry(self.frame_piece)
        self.entry_piece.pack(padx=5, pady=5)

        self.frame_processing_modes = tk.LabelFrame(self, text="Режимы обработки")
        self.frame_processing_modes.pack(padx=5, pady=5)

        self.spinner_n = tk.Spinbox(self.frame_processing_modes, from_=80, to=5000, width=9)
        self.spinner_n.delete(0, len(self.spinner_n.get()))
        self.spinner_n.insert(0, '2000')
        self.spinner_n.pack(padx=5, pady=5)
        self.spinner_n.bind('<MouseWheel>', lambda e, spin=self.spinner_n: plus(e, spin))

        self.spinner_s = tk.Spinbox(self.frame_processing_modes, from_=5, to=400, width=9)
        self.spinner_s.delete(0, len(self.spinner_n.get()))
        self.spinner_s.insert(0, '200')
        self.spinner_s.pack(padx=5, pady=5)
        self.spinner_s.bind('<MouseWheel>', lambda e, spin=self.spinner_s: plus(e, spin))

        self.button_new_experiment = tk.Button(self, text="Начать запись нового эксперимента",
                                               command=self.on_click)
        self.button_new_experiment.pack(padx=5, pady=5)
        self.button_view_experiment = tk.Button(self, text="Просмотр экспериментов", command=self.view_button)
        self.button_view_experiment.pack(padx=5, pady=5)

        self.entry_piece.focus()

    def on_click(self):
        material = self.listbox_material.get()
        coating = self.listbox_coating.get()
        tool = self.listbox_tool.get()
        stage = self.listbox_stage.get()

        if (check_float(self.entry_piece.get()) and check_float(self.text_a.get()) and check_float(self.text_b.get())
                and check_float(self.spinner_n.get()) and check_float(self.spinner_s.get())):
            length_piece = float(self.entry_piece.get())
            a = float(self.text_a.get())
            b = float(self.text_b.get())
            n = float(self.spinner_n.get())
            s = float(self.spinner_s.get())
            window = NewExperiment(material, coating, tool, length_piece, a, b, n, s, self.dir_save, stage)
            window.grab_set()
        else:
            messagebox.showerror("Ошибка", "Введите корректные данные")

    def view_button(self):
        window = ViewExperiment(self.dir_save)
        self.wait_window(window)
        window.mainloop()

    def add_type(self, type_):
        add_window = AddConstant(type_, self.file_data)
        add_window.grab_set()


class NewExperiment(tk.Toplevel):

    def __init__(self,
                 material: str,
                 coating: str,
                 tool: str,
                 length_piece: float,
                 a: float,
                 b: float,
                 n: float,
                 s: float,
                 dir_save: str,
                 stage: str):
        super().__init__()
        self.style = ttk.Style(self)
        self.style.configure("LabelLeave.TLabelframe", background="SystemButtonFace")
        self.style.configure("LabelEnter.TLabelframe", background="lightgreen")

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
        self.n = n
        self.s = s
        self.dir_save = dir_save
        self.stage = stage
        self.text_title = (f"Материал: {material}, Покрытие: {coating}, Инструмент: {tool} Этап: {stage}\n"
                           f"Длина заготовки: {length_piece} мм, Сечение(axb): {a}мм x {b}мм\n"
                           f"Режимы резания: {n=}об/мин, {s=} мм/мин")

        self.canvas_point = tk.Canvas(self, width=2000, height=130)
        self.scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas_point.xview,
                                      background='lightblue')
        self.canvas_point.pack(padx=5, pady=5)

        self.scrollbar.config(command=self.canvas_point.xview)
        self.scrollbar.pack(padx=5, pady=5, fill=tk.X)

        self.inner_frame = tk.Frame(self.canvas_point)
        self.canvas_point.create_window((0, 0), window=self.inner_frame, anchor='nw')

        def on_canvas_configure(event):
            self.canvas_point.configure(scrollregion=self.canvas_point.bbox("all"))

        self.inner_frame.bind("<Configure>", on_canvas_configure)
        self.scrollbar.bind('<MouseWheel>', lambda event: on_mouse_wheel_x(event, self.canvas_point))
        self.canvas_point.bind('<MouseWheel>', lambda event: on_mouse_wheel_x(event, self.canvas_point))

        self.frame_point = tk.LabelFrame(self.inner_frame, text="0")
        self.frame_point.grid(row=0, column=0, padx=5, pady=5)

        self.label_title = tk.Label(self, text=self.text_title, font=tk.font.Font(size=12),
                                    )
        self.label_title.pack(padx=5, pady=5)

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.pack(padx=5, pady=5)
        self.button_add_point = tk.Button(self.frame_buttons, text="Добавить точку", command=self.add_point_)
        self.button_add_point.grid(row=0, column=0, padx=5, pady=5)
        self.button_save_table = tk.Button(self.frame_buttons, text="Сохранить", command=self.save_experiment)
        self.button_save_table.grid(row=0, column=1, padx=5, pady=5)

        self.experiment = Experiment(self.material, self.coating, self.tool, self.n, self.s,
                                     self.a, self.b, self.length_piece, self.stage)

    def add_point_(self):
        self.frame_point = ttk.LabelFrame(self.inner_frame, text=f"{self.count_point + 1}", width=10,
                                          style='LabelLeave.TLabelframe')
        self.frame_point.grid(row=0, column=self.count_point + 1, padx=5, pady=5)
        self.frame_point.bind("<Enter>", lambda e, lab=self.frame_point: enter(e, lab))
        self.frame_point.bind("<Leave>", lambda e, lab=self.frame_point: leave(e, lab))
        self.frame_point.bind("<Control-ButtonPress-3>", lambda e, lab=self.frame_point: self.delete_point_(lab))
        self.frame_point.bind('<MouseWheel>', lambda event: on_mouse_wheel_x(event, self.canvas_point))
        self.frame_point.index = self.count_point

        self.new_spin = Spinner(self.frame_point,
                                default=self.list_point[self.count_point - 1][0].get() if self.list_point else '4')
        self.new_spin.pack(padx=5, pady=5)
        self.new_spin.bind('<Return>', lambda e: self.graphik())

        self.new_entry = Entry_wear(self.frame_point, 0.002,
                                    default=self.list_point[self.count_point - 1][
                                        1].get() if self.list_point else '0.05')
        self.new_entry.pack(padx=5, pady=5)
        self.new_entry.bind('<Return>', lambda e: self.graphik())

        self.entry_length_piece = Entry_wear(
            self.frame_point,
            1,
            default=self.list_point[self.count_point - 1][2].get() if self.list_point else str(
                self.experiment.length_piece
            )
        )
        self.entry_length_piece.pack(padx=5, pady=5)
        self.entry_length_piece.bind('<Return>', lambda e: self.graphik())

        self.list_point.append((self.new_spin, self.new_entry, self.entry_length_piece))

        self.graphik()
        self.canvas_point.configure(scrollregion=self.canvas_point.bbox("all"))
        self.count_point += 1

    def graphik(self, event=None):
        self.experiment.table = self.experiment.table.drop(index=list(range(self.count_point + 1)))
        self.experiment.table.loc[0] = [0, 0, 0]
        for point in self.list_point:
            self.experiment.add_point(float(point[0].get()), float(point[1].get()), float(point[2].get()))

        fig, ax = self.experiment.graphik()
        ax.axhline(0.3)
        if self.canvas_graph:
            self.canvas_graph.get_tk_widget().destroy()
        self.canvas_graph = FigureCanvasTkAgg(fig, master=self)
        self.canvas_graph.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas_graph.draw()

        plt.close()

    def delete_point_(self, frame_point: tk.LabelFrame) -> None:
        frame_point.destroy()
        del self.list_point[frame_point.index]

        for index, point in enumerate(self.list_point):
            point[0].master.index = index
            point[0].master['text'] = str(index + 1)

        self.graphik()
        self.count_point -= 1

    def save_experiment(self):
        data = shelve.open(os.path.join(self.dir_save, "experiment.db"))
        key = int(list(data.keys())[-1]) + 1 if list(data.keys()) else 0
        data[str(key)] = self.experiment
        data.close()
        self.destroy()

    def destroy(self):
        if self.canvas_graph:
            self.canvas_graph.get_tk_widget().destroy()
        super().destroy()


class Spinner(tk.Spinbox):
    def __init__(self, master=None, step_: int | float = 1, default: str = "4", **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<MouseWheel>', lambda event, step=step_: plus(event,
                                                                 self,
                                                                 func=master.master.master.master.graphik))
        self.insert(0, default)


class Entry_wear(tk.Entry):

    def __init__(self, master=None, step_: int | float = 1, default='0.05', **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<MouseWheel>',
                  lambda event, step=step_: plus(event, self, step,
                                                 master.master.master.master.graphik))
        self.insert(0, default)


class ViewExperiment(tk.Toplevel):
    def __init__(self, dir_save: str):
        super().__init__()
        self.geometry("1500x700")
        self.state('zoomed')
        self.title("Данные об износе.")
        self.dir_save = dir_save
        self.list_experiment: list[Experiment] = []
        self.select_exp: list[int] = []
        self.canvas_graph = None
        self.filter_material = None
        self.filter_coating = None
        self.filter_tool = None
        self.filter_stage = None

        self.canvas_experiment = tk.Canvas(self, width=600, height=400)
        self.scrollbar_experiment = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas_experiment.yview,
                                                 background="lightgrey")
        self.canvas_experiment.grid(row=0, column=1, rowspan=2)
        self.scrollbar_experiment.config(command=self.canvas_experiment.yview)
        self.scrollbar_experiment.grid(row=0, column=0, padx=5, pady=5, sticky="ns", rowspan=2)
        self.frame_experiment = tk.Frame(self.canvas_experiment)
        self.canvas_experiment.create_window((0, 0), window=self.frame_experiment, anchor='nw')

        def on_canvas_configure(event):
            self.canvas_experiment.configure(scrollregion=self.canvas_experiment.bbox("all"))

        self.frame_experiment.bind("<Configure>", on_canvas_configure)
        self.scrollbar_experiment.bind('<MouseWheel>', lambda event: on_mouse_wheel_y(event, self.canvas_experiment))

        self.combobox_type_table = ttk.Combobox(self,
                                                values=['Путь', 'Время обработки'])
        self.combobox_type_table.grid(row=0, column=2, padx=5, pady=5)
        self.combobox_type_table.current(0)

        def change_type_table(event):
            self.create_full_table(self.combobox_type_table.get())
            self.few_graphik()
            self.create_table_on_frame()

        self.combobox_type_table.bind("<<ComboboxSelected>>", change_type_table)

        self.frame_experiment_graph = tk.Frame(self)
        self.frame_experiment_graph.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.canvas_full_table = tk.Canvas(self,
                                           width=1400, background='lightgrey', height=200)
        self.canvas_full_table.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
        self.scrollbar_full_table = tk.Scrollbar(self,
                                                 orient=tk.HORIZONTAL,
                                                 command=self.canvas_full_table.xview,
                                                 background="grey")
        self.scrollbar_full_table.config(command=self.canvas_full_table.xview)
        self.scrollbar_full_table.grid(row=3, column=1, sticky="ew", columnspan=2)
        self.frame_table = tk.Frame(self.canvas_full_table)
        self.canvas_full_table.create_window((0, 0), window=self.frame_table, anchor='nw')
        self.experiment()

        def on_canvas_full_table_configure(event):
            self.canvas_full_table.configure(scrollregion=self.canvas_full_table.bbox("all"))

        self.frame_table.bind("<Configure>", on_canvas_full_table_configure)
        self.scrollbar_full_table.bind('<MouseWheel>', lambda event: on_mouse_wheel_x(event, self.canvas_full_table))

        self.scrollbar_full_table_y = tk.Scrollbar(self,
                                                   orient=tk.VERTICAL,
                                                   command=self.canvas_full_table.yview,
                                                   background='grey',
                                                   troughcolor='lightblue')
        self.scrollbar_full_table_y.config(command=self.canvas_full_table.yview)
        self.scrollbar_full_table_y.grid(row=2, column=0, sticky="ns")
        self.scrollbar_full_table_y.bind('<MouseWheel>',
                                         lambda event: on_mouse_wheel_y(event, self.canvas_full_table))

    def experiment(self):
        if self.filter_material:
            material = self.filter_material.get()
            if material == 'Титан':
                material = 'ВТ'
            if material == 'Хром-никель':
                material = 'ХН'
            coating = self.filter_coating.get()
            tool = self.filter_tool.get()
            stage = self.filter_stage.get()
            for widget in self.frame_experiment.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.destroy()
            data = shelve.open(os.path.join(self.dir_save, "experiment.db"))
            for key, value in data.items():
                text = (f"{key}: {value.material}; {value.coating}; {value.tool}; "
                        f"{value.n}; {value.s}; {value.a}; {value.b}; {value.length_piece}; {value.stage}")
                if material in text and coating in text and tool in text and stage in text:
                    self.label_experiment = tk.Label(self.frame_experiment, text=text)
                    self.label_experiment.pack(padx=5, pady=5, anchor='w')
                    self.label_experiment.index = key
                    self.label_experiment.bind('<Button-1>', self.select_experiment)
                    self.label_experiment.bind('<Button-3>', self.unselect_experiment)
                    self.label_experiment.bind('<Control-ButtonPress-3>', self.delete_experiment)
                self.list_experiment.append(value)  # type Experiment
            data.close()
        else:
            data = shelve.open(os.path.join(self.dir_save, "experiment.db"))
            for key, value in data.items():
                self.list_experiment.append(value)  # type Experiment
            data.close()
            list_material = ['Титан', 'Хром-никель']
            list_material.extend([experiment.material for experiment in self.list_experiment])
            self.filter_frame = tk.LabelFrame(self.frame_experiment, text="Выберите тип испытаний")
            self.filter_frame.pack(padx=5, pady=5, anchor='nw')
            self.filter_frame.bind('<Button-3>', self.clear_filter)
            self.filter_material = ttk.Combobox(
                self.filter_frame,
                values=list_material
            )
            self.filter_material.grid(row=0, column=0, padx=2, pady=2)
            self.filter_material.bind('<<ComboboxSelected>>', lambda e: self.experiment())
            self.filter_material.bind('<Return>', lambda e: self.experiment())
            list_coating = [experiment.coating for experiment in self.list_experiment]
            self.filter_coating = ttk.Combobox(
                self.filter_frame,
                values=list_coating
            )
            self.filter_coating.grid(row=0, column=1, padx=2, pady=2)
            self.filter_coating.bind('<<ComboboxSelected>>', lambda e: self.experiment())
            self.filter_coating.bind('<Return>', lambda e: self.experiment())
            list_tool = [experiment.tool for experiment in self.list_experiment]
            self.filter_tool = ttk.Combobox(
                self.filter_frame,
                values=list_tool
            )
            self.filter_tool.grid(row=0, column=2, padx=2, pady=2)
            self.filter_tool.bind('<<ComboboxSelected>>', lambda e: self.experiment())
            self.filter_tool.bind('<Return>', lambda e: self.experiment())
            self.filter_stage = ttk.Combobox(
                self.filter_frame,
                values=[experiment.stage for experiment in self.list_experiment]
            )
            self.filter_stage.grid(row=0, column=3, padx=2, pady=2)
            self.filter_stage.bind('<<ComboboxSelected>>', lambda e: self.experiment())
            self.filter_stage.bind('<Return>', lambda e: self.experiment())

            self.button_excel = tk.Button(self.filter_frame, text='Сохранить в Excel',
                                          command=self.to_excel)
            self.button_excel.grid(row=1, column=0, columnspan=4, padx=2, pady=2)

            data = shelve.open(os.path.join(self.dir_save, "experiment.db"))
            for key, value in data.items():
                text = (f"{key}: {value.material}; {value.coating}; {value.tool}; "
                        f"{value.n}; {value.s}; {value.a}; {value.b}; {value.length_piece}; {value.stage}")
                self.label_experiment = tk.Label(self.frame_experiment, text=text)
                self.label_experiment.pack(padx=5, pady=5, anchor='w')
                self.label_experiment.index = key
                self.label_experiment.bind('<Button-1>', self.select_experiment)
                self.label_experiment.bind('<Button-3>', self.unselect_experiment)
                self.label_experiment.bind('<Control-ButtonPress-3>', self.delete_experiment)
                self.list_experiment.append(value)  # type Experiment
            data.close()
        self.select_exp.clear()
        self.create_full_table(self.combobox_type_table.get())
        self.few_graphik()
        # self.create_table_on_frame()

    def create_full_table(self, type_x):
        name_x = 'Величина обработки' if type_x == 'Путь' else 'Время обработки'

        if self.select_exp:
            self.full_table: pd.DataFrame = self.list_experiment[self.select_exp[0]].table[
                [name_x, 'Величина износа']]
            key = self.select_exp[0]
            new_name_column = (f'{key}: {self.list_experiment[self.select_exp[0]].material}; '
                               f'{self.list_experiment[self.select_exp[0]].coating}; '
                               f'{self.list_experiment[self.select_exp[0]].tool};\n'
                               f'{self.list_experiment[self.select_exp[0]].n}; '
                               f'{self.list_experiment[self.select_exp[0]].s}; '
                               f'{self.list_experiment[self.select_exp[0]].length_piece}; ')

            self.full_table.columns = [name_x, new_name_column]
            for index, experiment in enumerate(self.list_experiment):
                if index != self.select_exp[0] and index in self.select_exp:
                    # Слияние таблиц по колонке 'Величина обработки'
                    experiment_data = experiment.table[[name_x, 'Величина износа']]
                    new_experiment_name = (f'{key}: {experiment.material}; {experiment.coating}; {experiment.tool};\n'
                                           f'{experiment.n}; {experiment.s}; {experiment.length_piece}; ')

                    # Переименовываем колонку 'Величина износа'
                    experiment_data = experiment_data.rename(columns={'Величина износа': new_experiment_name})

                    # Слияние с основной таблицей
                    self.full_table = pd.merge(self.full_table, experiment_data,
                                               how='outer', on=name_x,
                                               suffixes=('', f' {new_experiment_name}'),
                                               sort=True)
        else:
            self.full_table = None

    def few_graphik(self):
        if self.select_exp:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 5)
            ax.axhline(y=0.3, color='r', linestyle='-')
            name_x = self.full_table.columns[0]
            for name_column in self.full_table.columns[1:]:
                x = self.full_table[self.full_table[name_column].notna()][name_x].tolist()
                y = self.full_table[self.full_table[name_column].notna()][name_column].tolist()
                ax.plot(x, y, label=f'{name_column}',
                        marker='o')

            ax.set_xlabel(f"{name_x}, мм" if name_x == 'Величина обработки' else f"{name_x}, мин")
            ax.set_ylabel('Величина износа, мм')
            ax.grid()
            ax.legend()

            if self.canvas_graph:
                self.canvas_graph.get_tk_widget().destroy()

            self.canvas_graph = FigureCanvasTkAgg(fig, master=self.frame_experiment_graph)
            self.canvas_graph.get_tk_widget().pack(padx=5, pady=5)
            self.canvas_graph.draw()

            plt.close(fig)
        else:
            if self.canvas_graph:
                self.canvas_graph.get_tk_widget().destroy()
                self.canvas_graph = None

    def create_table_on_frame(self):
        if self.select_exp:
            name_x = self.full_table.columns[0]
            for widget in self.frame_table.winfo_children():
                widget.destroy()

            button_add = tk.Button(self.frame_table, text='Добавить точку', command=self.add_new_point)
            button_add.grid(padx=2, pady=2, column=0, row=0)

            if self.select_exp:
                columns = self.full_table[name_x].tolist()
                names_experiment = [names.replace('Величина износа', '').strip() for names in self.full_table.columns][
                                   1:]
                for index, column in enumerate(columns):
                    if name_x == 'Величина обработки':
                        label = tk.Label(self.frame_table, text=round(float(column)))
                    else:
                        label = tk.Label(self.frame_table, text=round(float(column), 1))
                    label.grid(padx=2, pady=2, column=index + 1, row=0)
                    label.bind('<Control-ButtonPress-3>', self.delete_point)
                for index, name in enumerate(names_experiment):
                    label = tk.Label(self.frame_table, text=name)
                    label.grid(padx=2, pady=2, column=0, row=index + 1)
                    button = tk.Button(self.frame_table, text='Сохранить',
                                       command=lambda i=index: self.save_button(i))
                    button.grid(padx=2, pady=2, column=len(columns) + 1, row=index + 1)

                for index_columns, column in enumerate(columns):
                    for index_names, name in enumerate(names_experiment):
                        entry = Entry_wear(master=self.frame_table, step_=0.002,
                                           default=str(self.full_table.iloc[index_columns, index_names + 1]),
                                           width=6)
                        entry.grid(padx=2, pady=2, column=index_columns + 1, row=index_names + 1)
                        entry.bind('<MouseWheel>', lambda event, step=0.002, ent=entry: plus(event, ent, step,
                                                                                             func=self.change_graphik))
                        entry.bind('<Return>', lambda event, ent=entry: self.change_graphik(event))
        else:
            for widget in self.frame_table.winfo_children():
                widget.destroy()

    def select_experiment(self, event: tk.Event):
        widget: tk.Label = event.widget
        widget.configure(background='lightblue')
        index = int(widget.index)
        if index not in self.select_exp:
            self.select_exp.append(index)
            self.create_full_table(self.combobox_type_table.get())
            self.few_graphik()
            self.create_table_on_frame()

    def unselect_experiment(self, event: tk.Event):
        widget: tk.Label = event.widget
        widget.configure(background='SystemButtonFace')
        index = int(widget.index)
        if index in self.select_exp:
            self.select_exp.remove(index)
            self.create_full_table(self.combobox_type_table.get())
            self.few_graphik()
            self.create_table_on_frame()
        if not self.select_exp:
            if self.canvas_graph:
                self.canvas_graph.get_tk_widget().destroy()
                for widget in self.frame_table.winfo_children():
                    widget.destroy()

    def save_table(self, event: tk.Event):
        entry = event.widget
        column = entry.grid_info()['column']
        row = entry.grid_info()['row']
        self.full_table.iloc[column - 1, row] = float(entry.get())
        self.few_graphik()

    def change_graphik(self, event):
        entry = event.widget
        column = entry.grid_info()['column']
        row = entry.grid_info()['row']
        self.full_table.iloc[column - 1, row] = float(entry.get())
        self.few_graphik()

    def save_button(self, index: int):
        name_x = self.full_table.columns[0]
        key = self.select_exp[index]
        new_table = self.full_table.iloc[:, [0, index + 1]].dropna()
        s = self.list_experiment[index].s
        if name_x == 'Величина обработки':
            new_table['Время обработки'] = new_table['Величина обработки'] / s

        else:
            new_table['Величина обработки'] = new_table['Время обработки'] * s


        table = new_table[['Величина обработки', 'Время обработки', new_table.columns[1]]].reset_index(drop=True)
        table.columns = self.list_experiment[index].table.columns

        self.list_experiment[key].table = table
        data = shelve.open(os.path.join(self.dir_save, "experiment.db"))
        data[str(key)] = self.list_experiment[index]
        data.close()

    def add_new_point(self):
        window = AddPoint()
        self.wait_window(window)
        name_x = self.full_table.columns[0]
        try:
            new_point = [float(window.result)]
            new_point.extend(None for i in range(len(self.select_exp)))
            self.full_table.loc[len(self.full_table)] = new_point
            self.full_table = self.full_table.sort_values(by=name_x, ascending=True)
            self.few_graphik()
            self.create_table_on_frame()
        except AttributeError:
            messagebox.showinfo(title='Ошибка', message='Точка не вписана')

    def delete_point(self, event):
        label: tk.Label = event.widget
        num_record = label.grid_info()['column'] - 1
        self.full_table = self.full_table.drop(self.full_table.index[num_record])
        self.few_graphik()
        self.create_table_on_frame()

    def delete_experiment(self, event):
        widget: tk.Label = event.widget
        index = int(widget.index)
        if index in self.select_exp:
            self.unselect_experiment(event)

        self.list_experiment.pop(index)
        with shelve.open(os.path.join(self.dir_save, "experiment.db")) as data:
            del data[str(index)]

        self.experiment()

    def clear_filter(self, event):
        widget = event.widget
        for widget_children in widget.winfo_children():
            if isinstance(widget_children, ttk.Combobox):
                widget_children.set('')

        self.experiment()

    def to_excel(self):
        if self.select_exp:
            excel_dir = os.path.join(self.dir_save, 'excel')
            os.makedirs(excel_dir, exist_ok=True)
            excel_file = os.path.join(excel_dir, "experiment.xlsx")
            name_sheet = tk.simpledialog.askstring(title='Впишите название листа', prompt='Введите название листа')

            if not name_sheet:
                tk.messagebox.showwarning("Предупреждение", "Имя листа не введено.")
                return

            try:
                if os.path.exists(excel_file):
                    # Если файл существует, добавляем новый лист или заменяем существующий
                    with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        self.full_table.to_excel(writer, sheet_name=name_sheet, index=False)
                else:
                    # Если файла нет, создаем новый
                    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                        self.full_table.to_excel(writer, sheet_name=name_sheet, index=False)
                tk.messagebox.showinfo("Успех", f"Данные успешно сохранены в лист '{name_sheet}'.")
            except Exception as e:
                tk.messagebox.showerror("Ошибка", f"Произошла ошибка при сохранении в Excel: {e}")
        else:
            tk.messagebox.showwarning("Предупреждение", "Нет выбранных экспериментов для сохранения.")

    def to_csv(self):
        if self.select_exp:
            csv_dir = os.path.join(self.dir_save, 'csv')
            os.makedirs(csv_dir, exist_ok=True)
            csv_file = os.path.join(csv_dir, "experiment.csv")


if __name__ == '__main__':
    app = Main()
    app.mainloop()
