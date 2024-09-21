import shelve

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv


class Experiment:
    """
    Инициализирует новый эксперимент с заданными параметрами.

    :param material: Материал заготовки.
    :param coating: Покрытие инструмента.
    :param tool: Тип инструмента.
    :param n: Обороты шпинделя (n).
    :param s: Подача (s) в мм/мин.
    :param a: Размер сечения a в мм.
    :param b: Размер сечения b в мм.
    :param length_piece: Длина заготовки в мм.
    :param stage: Этап эксперимента.
    """
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
        """
        Добавляет новую точку данных в таблицу эксперимента.

        :param n_step: Номер шага или количество проходов.
        :param wear: Величина износа инструмента на данном шаге (в мм).
        :param length_piece: Длина заготовки для данного шага (в мм).
        """
        length_processing = length_piece * n_step
        time_processing = length_processing / self.s
        self.table.loc[len(self.table)] = [length_processing, time_processing, wear]

    def save_to_csv(self, base_dir='data'):
        """
        Сохраняет данные эксперимента в CSV-файл.

        Файл будет содержать информацию об эксперименте и таблицу данных.
        Имя файла формируется на основе оборотов шпинделя (n) и подачи (s).
        Файл сохраняется в директорию, сформированную на основе атрибутов эксперимента.

        :param base_dir: Базовая директория для сохранения данных. По умолчанию 'data'.
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
        """
        Строит график зависимости величины износа от величины обработки.

        :return: Кортеж (fig, ax), где fig — объект Figure, ax — объект Axes.
        """
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

    @property
    def L(self):
        """
        Вычисляет величину обработки L, при которой величина износа достигает 0.3 мм.

        Если величина износа в последней точке превышает 0.3 мм, выполняется линейная интерполяция между
        последними двумя точками для определения точного значения L при износе 0.3 мм.

        :return: Величина обработки L при износе 0.3 мм. Если износ меньше 0.3 мм, возвращает None.
        """
        if self.table["Величина износа"].iloc[-1] > 0.3:
            x0, y0 = self.table["Величина обработки"].iloc[-2], self.table["Величина износа"].iloc[-2]
            x1, y1 = self.table["Величина обработки"].iloc[-1], self.table["Величина износа"].iloc[-1]
            y2 = 0.3
            x2 = x0 + (x1 - x0) * (y2 - y0) / (y1 - y0)
            return x2
        else:
            return None

    @property
    def T(self):
        """
        Вычисляет время обработки T, при котором величина износа достигает 0.3 мм.

        :return: Время обработки T при износе 0.3 мм. Если износ меньше 0.3 мм, возвращает None.
        """
        return self.L / self.s


if __name__ == '__main__':
    data = shelve.open(r'C:\Users\aples\PycharmProjects\Recording-of-experimental-data\data\experiment.db')

    print(data['1'].T)
    print(data['1'].L)
    data['1'].graphik()
    plt.show()
