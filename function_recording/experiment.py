import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Experiment:

    def __init__(self, material, coating, tool, n, s, a, b, length_piece):
        self.material = material
        self.coating = coating
        self.tool = tool
        self.n = n
        self.s = s
        self.a = a
        self.b = b
        self.length_piece = length_piece
        self.table = pd.DataFrame(
            {"Величина обработки": [0],
             "Время обработки": [0],
             "Величина износа": [0]}
        )

    def add_point(self, n_step, wear):
        length_processing = self.length_piece * n_step
        time_processing = length_processing * self.s
        self.table.loc[len(self.table)] = [length_processing, time_processing, wear]

    def save_table(self, path: str) -> bool:
        pass

    def change_point(self, index, n_step, wear):
        length_processing = self.length_piece * n_step
        time_processing = length_processing * self.s
        self.table.loc[index] = [length_processing, time_processing, wear]

    def delete_point(self, index):
        self.table.drop(index, inplace=True)
        self.table.reset_index(drop=True, inplace=True)

    def graphik(self):
        x = self.table["Величина обработки"]
        y = self.table["Величина износа"]
        fig, ax = plt.subplots()
        ax.plot(x, y, marker="o")
        # Добавление номеров точек рядом с каждой
        for i, (x_val, y_val) in enumerate(zip(x, y), start=0):
            ax.text(x_val, y_val, str(i), fontsize=12, ha='right', va='bottom')  # Номер точки

        ax.grid()
        ax.set_xlabel("Величина обработки")
        ax.set_ylabel("Величина износа")
        return fig, ax


if __name__ == '__main__':
    experiment = Experiment(
        material="Сталь",
        coating="Никель",
        tool="Кулачковый",
        n=100,
        s=10,
        a=10,
        b=10,
        length_piece=100
    )
    experiment.add_point(n_step=4, wear=0.4)
    experiment.add_point(n_step=8, wear=0.4)
    experiment.add_point(n_step=16, wear=0.4)
    experiment.change_point(index=2, n_step=8, wear=0.9)
    experiment.delete_point(index=2)
    print(experiment.table)
    experiment.graphik()
    plt.show()
