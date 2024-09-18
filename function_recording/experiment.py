import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

class Experiment:

    def __init__(self, material, coating, tool, n, s, a, b, length_piece, stage):
        self.material = material
        self.coating = coating
        self.tool = tool
        self.n = n
        self.s = s
        self.a = a
        self.b = b
        self.length_piece = length_piece
        self.stage = stage
        self.table = pd.DataFrame(
            {"Величина обработки": [0],
             "Время обработки": [0],
             "Величина износа": [0]}
        )

    def add_point(self, n_step, wear, length_piece):
        length_processing = length_piece * n_step
        time_processing = length_processing / self.s
        self.table.loc[len(self.table)] = [length_processing, time_processing, wear]

    def save_to_csv(self, base_dir='data'):
        """
        Сохраняет таблицу эксперимента в CSV-файл по заданному пути.
        Имя файла включает информацию о оборотах шпинделя (n) и подаче (s).
        Первые строки файла содержат информацию об эксперименте (все атрибуты класса без таблицы).
        """
        # Формируем путь к директории на основе атрибутов эксперимента
        dir_path = os.path.join(
            base_dir,
            str(self.stage),
            str(self.material),
            str(self.tool),
            str(self.coating)
        )

        # Создаем директории, если они не существуют
        os.makedirs(dir_path, exist_ok=True)

        # Формируем имя файла, включая обороты шпинделя (n) и подачу (s)
        file_name = f"experiment_n={self.n}_s={self.s}.csv"

        # Полный путь к файлу
        file_path = os.path.join(dir_path, file_name)

        # Подготовка информации об эксперименте (исключая 'table') для записи в файл
        experiment_info = {
            'Материал': self.material,
            'Покрытие': self.coating,
            'Инструмент': self.tool,
            'Этап': self.stage,
            'Длина заготовки': self.length_piece,
            'a': self.a,
            'b': self.b,
            'Обороты шпинделя (n)': self.n,
            'Подача (s)': self.s,
            # Добавьте другие атрибуты по необходимости
        }

        try:
            # Открываем файл и записываем информацию об эксперименте
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Записываем атрибуты эксперимента в формате ключ-значение
                for key, value in experiment_info.items():
                    writer.writerow([key, value])

                # Пустая строка для разделения информации об эксперименте и данных таблицы
                writer.writerow([])

            # Теперь добавляем данные таблицы в файл, используя pandas
            with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
                self.table.to_csv(csvfile, index=False)

            print(f"Данные эксперимента сохранены в {file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")



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
        length_piece=100,
        stage=1
    )
    experiment.add_point(n_step=4, wear=0.4, length_piece=321)
    experiment.add_point(n_step=8, wear=0.4, length_piece=321)
    experiment.add_point(n_step=16, wear=0.4, length_piece=321)

    print(experiment.table)
    experiment.graphik()
    plt.show()
