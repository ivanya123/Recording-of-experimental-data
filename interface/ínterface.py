from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os
import shelve
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
import matplotlib.pyplot as plt
import pandas as pd

from data_constant import *
from function_recording.function import *
from function_recording.experiment import Experiment


def first_start():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            file_path = json.load(f)
            return file_path['path'], file_path['save']
    else:
        file_path = {'path': filedialog.askopenfilename(title='Выберать файл констант'),
                     'save': filedialog.askdirectory(title="Выберать папку для сохранения данных")}
        with open('config.json', 'w') as f:
            json.dump(file_path, f)
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

        self.frame_stage = tk.LabelFrame(self, text="Этап")
        self.frame_stage.pack(padx=5, pady=5)
        self.listbox_stage = ttk.Combobox(self.frame_stage, values=self.list_stage)
        self.listbox_stage.set(self.list_stage[5])
        self.listbox_stage.grid(row=0, column=0, padx=5, pady=5)
        self.stage_add = tk.Button(self.frame_stage, text="Добавить этап")
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
        window.grab_set()


class NewExperiment(tk.Toplevel):

    def add_point_(self):
        self.frame_point = tk.LabelFrame(self.inner_frame, text=f"{self.count_point + 1}", width=10)
        self.frame_point.grid(row=0, column=self.count_point + 1, padx=5, pady=5)
        self.frame_point.bind("<Enter>", lambda e, lab=self.frame_point: enter(e, lab))
        self.frame_point.bind("<Leave>", lambda e, lab=self.frame_point: leave(e, lab))
        self.frame_point.bind("<Control-ButtonPress-3>", lambda e, lab=self.frame_point: self.delete_point_(lab))
        self.frame_point.bind('<MouseWheel>', lambda event: on_mouse_wheel(event, self.canvas_point))
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

        self.list_point.append((self.new_spin, self.new_entry))

        self.graphik()
        self.canvas_point.configure(scrollregion=self.canvas_point.bbox("all"))
        self.count_point += 1

    def graphik(self):
        self.experiment.table = self.experiment.table.drop(index=list(range(self.count_point + 1)))
        self.experiment.table.loc[0] = [0, 0, 0]
        for point in self.list_point:
            self.experiment.add_point(float(point[0].get()), float(point[1].get()))

        fig, ax = self.experiment.graphik()
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

        self.canvas_point = tk.Canvas(self, width=1000, height=100)
        self.scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas_point.xview)
        self.canvas_point.pack(padx=5, pady=5)

        self.scrollbar.config(command=self.canvas_point.xview)
        self.scrollbar.pack(padx=5, pady=5, fill=tk.X)

        self.inner_frame = tk.Frame(self.canvas_point)
        self.canvas_point.create_window((0, 0), window=self.inner_frame, anchor='nw')

        def on_canvas_configure(event):
            self.canvas_point.configure(scrollregion=self.canvas_point.bbox("all"))

        self.inner_frame.bind("<Configure>", on_canvas_configure)
        self.scrollbar.bind('<MouseWheel>', lambda event: on_mouse_wheel(event, self.canvas_point))
        self.canvas_point.bind('<MouseWheel>', lambda event: on_mouse_wheel(event, self.canvas_point))

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
        self.bind('<MouseWheel>', lambda event, step=step_: plus(event, self, func=master.master.master.master.graphik))
        self.insert(0, default)


class Entry_wear(tk.Entry):

    def __init__(self, master=None, step_: int | float = 1, default='0.05', **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<MouseWheel>',
                  lambda event, step=step_: plus(event, self, step, master.master.master.master.graphik))
        self.insert(0, default)


class ViewExperiment(tk.Toplevel):
    def __init__(self, dir_save: str):
        super().__init__()
        self.geometry("1500x700")
        self.title("Данные об износе.")
        self.dir_save = dir_save
        self.list_experiment: list[Experiment] = []
        self.canvas_graph = None

        self.frame_experiment = tk.Frame(self)
        self.frame_experiment.grid(row=0, column=0, padx=5, pady=5)
        self.listbox_experiment = tk.Listbox(self.frame_experiment, selectmode=tk.EXTENDED)
        self.listbox_experiment.pack(padx=5, pady=5)
        self.listbox_experiment.bind("<<ListboxSelect>>", lambda event: self.few_graphik())
        self.experiment()

        self.canvas_experiment = tk.Frame(self)
        self.canvas_experiment.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.frame_table = tk.Frame(self)
        self.frame_table.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

    def experiment(self):
        data = shelve.open(os.path.join(self.dir_save, "experiment.db"))
        max_len = 0
        for key, value in data.items():
            text = (f"{key}: {value.material}; {value.coating}; {value.tool}; "
                    f"{value.n}; {value.s}; {value.a}; {value.b}; {value.length_piece}; {value.stage}")
            self.listbox_experiment.insert(tk.END, text)
            max_len = max(max_len, len(text))
            self.list_experiment.append(value)  # type Experiment
        data.close()
        self.listbox_experiment.config(width=max_len)

    def few_graphik(self):
        selected_experiment = self.listbox_experiment.curselection()
        for widget in self.frame_table.winfo_children():
            widget.destroy()

        if selected_experiment:

            fig, ax = plt.subplots()

            ax.axhline(y=0.3, color='r', linestyle='-')
            self.full_table = self.list_experiment[selected_experiment[0]].table[['Величина обработки', 'Величина износа']]


            for index, experiment in enumerate(self.list_experiment):
                if index in selected_experiment:
                    x = experiment.table['Величина обработки']
                    y = experiment.table['Величина износа']
                    ax.plot(x, y, label=f"{experiment.material}; {experiment.coating}; {experiment.tool}",
                            marker='o')
                    if index != selected_experiment[0]:
                        self.full_table = pd.merge(self.full_table, experiment.table[['Величина обработки', 'Величина износа']],
                                              how='outer', on='Величина обработки',
                                              suffixes=(
                                                  '',
                                                  f' {experiment.material}; {experiment.coating}; {experiment.tool}'),
                                              sort=True)

            if selected_experiment:
                columns = self.full_table['Величина обработки'].tolist()
                names_experiment = [names.replace('Величина износа', '').strip() for names in self.full_table.columns][1:]
                names_experiment[0] = (f'{self.list_experiment[selected_experiment[0]].material}; '
                                       f'{self.list_experiment[selected_experiment[0]].coating}; '
                                       f'{self.list_experiment[selected_experiment[0]].tool};')

                for index, column in enumerate(columns):
                    label = tk.Label(self.frame_table, text=int(column))
                    label.grid(padx=2, pady=2, column=index + 1, row=0)
                for index, name in enumerate(names_experiment):
                    label = tk.Label(self.frame_table, text=name)
                    label.grid(padx=2, pady=2, column=0, row=index + 1)

                for index_columns, column in enumerate(columns):
                    for index_names, name in enumerate(names_experiment):
                        entry = Entry_wear(master=self.frame_table, step_=0.002,
                                           default=str(self.full_table.iloc[index_columns, index_names + 1]),
                                           width=6)
                        entry.grid(padx=2, pady=2, column=index_columns + 1, row=index_names + 1)
                        entry.bind('<MouseWheel>', lambda event, step=0.002, ent=entry: plus(event, ent, step,
                                                                                             self.change_graphik(event)))

            ax.set_xlabel('Величина обработки')
            ax.set_ylabel('Величина износа')
            ax.grid()
            ax.legend()

            if self.canvas_graph:
                self.canvas_graph.get_tk_widget().destroy()

            self.canvas_graph = FigureCanvasTkAgg(fig, master=self.canvas_experiment)
            self.canvas_graph.get_tk_widget().pack(padx=5, pady=5)
            self.canvas_graph.draw()

            plt.close(fig)  # type:

    def change_graphik(self, event):
        entry = event.widget
        column = entry.grid_info()['column']
        row = entry.grid_info()['row']
        self.full_table.iloc[column - 1, row - 1] = float(entry.get())
        self.few_graphik()






if __name__ == '__main__':
    app = Main()
    app.mainloop()
