import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd


def check_float(string: str):
    """
    Проверяет, можно ли преобразовать строку в число с плавающей запятой.

    :param string: Строка для проверки.
    :return: True, если строку можно преобразовать в float, иначе False.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def plus(event, spinbox, step=1, func=None):
    """
    Обрабатывает событие прокрутки мыши для изменения значения в Spinbox или Entry.

    Увеличивает или уменьшает текущее значение в spinbox на заданный шаг при прокрутке колесика мыши.
    При необходимости вызывает дополнительную функцию обновления.

    :param event: Событие прокрутки мыши.
    :param spinbox: Виджет Spinbox или Entry, значение которого нужно изменить.
    :param step: Шаг изменения значения (по умолчанию 1).
    :param func: Дополнительная функция для вызова после изменения значения.
    """
    if check_float(spinbox.get()):
        num = float(spinbox.get())
        if event.delta < 0:
            num = round((num - step), 3)
        else:
            num = round((num + step), 3)

        spinbox.delete(0, tk.END)
        spinbox.insert(0, num)

        # Вызов функции обновления
        if func is not None:
            func(event)


def on_mouse_wheel_x(event, canvas):
    """
    Обрабатывает горизонтальную прокрутку колесиком мыши для Canvas.

    Позволяет прокручивать содержимое Canvas по горизонтали при использовании колесика мыши.

    :param event: Событие прокрутки мыши.
    :param canvas: Виджет Canvas для прокрутки.
    """
    if event.delta:
        canvas.xview_scroll(-1 * int(event.delta / 120), "units")
    else:
        if event.num == 4:
            canvas.xview_scroll(-1, "units")
        elif event.num == 5:
            canvas.xview_scroll(1, "units")


def on_mouse_wheel_y(event, canvas):
    """
    Обрабатывает вертикальную прокрутку колесиком мыши для Canvas.

    Позволяет прокручивать содержимое Canvas по вертикали при использовании колесика мыши.

    :param event: Событие прокрутки мыши.
    :param canvas: Виджет Canvas для прокрутки.
    """
    if event.delta:
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")


def enter(event: str, label: ttk.LabelFrame) -> None:
    """
   Изменяет стиль LabelFrame при наведении курсора мыши.

   Позволяет реализовать эффект наведения, изменяя стиль виджета при событии Enter.

   :param event: Событие наведения мыши.
   :param label: Виджет LabelFrame, стиль которого нужно изменить.
   """
    label.config(style='LabelEnter.TLabelframe')


def leave(event: str, label: ttk.LabelFrame) -> None:
    """
    Восстанавливает стиль LabelFrame при уходе курсора мыши.

    Позволяет вернуть исходный стиль виджета при событии Leave.

    :param event: Событие ухода курсора мыши.
    :param label: Виджет LabelFrame, стиль которого нужно восстановить.
    """
    label.config(style='LabelLeave.TLabelframe')


def interpolate_data(data_frame):
    """
    Интерполирует пропущенные значения в DataFrame методом линейной интерполяции.

    Полезно для заполнения отсутствующих данных в экспериментальных наборах данных.

    :param data_frame: pandas DataFrame для интерполяции.
    :return: DataFrame с интерполированными значениями.
    """
    return data_frame.interpolate(method='linear', limit_direction='forward', axis=0)


def get_coating_from_string(string: str) -> str:
    """
    Извлекает название покрытия из строки, разделенной точкой с запятой.

    Предполагается, что покрытие является вторым элементом после разделения.

    :param string: Строка, содержащая информацию с разделителями ';'.
    :return: Название покрытия, извлеченное из строки.
    """
    return string.split(';')[1].strip()


class cache_decor:

    def __init__(self, func):
        self.func = func
        self.param = {}

    def __call__(self, dataframe):
        key = (dataframe.columns[0], dataframe.columns[1])
        if key in self.param:
            return self.param[key]
        else:
            result = self.func(dataframe)
            self.param[key] = result
            return result

    def clear_cache(self, dataframe: pd.DataFrame):
        key = (dataframe.columns[0], dataframe.columns[1])
        self.param.pop(key, None)




@cache_decor
def get_durability_from_dataframe(dataframe: pd.DataFrame) -> float | None:
    """
    Вычисляет величину обработки L, при которой величина износа достигает 0.3 мм.

    Если величина износа в последней точке превышает 0.3 мм, выполняется линейная интерполяция между
    последними двумя точками для определения точного значения L при износе 0.3 мм.

    :return: Величина обработки L при износе 0.3 мм. Если износ меньше 0.3 мм, возвращает None.
    """
    if dataframe[dataframe.columns[1]].iloc[-1] >= 0.3:
        y1 = dataframe[dataframe[dataframe.columns[1]] > 0.3].iloc[0, 1]
        x1 = dataframe[dataframe[dataframe.columns[1]] > 0.3].iloc[0, 0]
        index = dataframe[dataframe[dataframe.columns[1]] > 0.3].index[0]
        x0, y0 = dataframe[dataframe.columns[0]].iloc[index - 1], dataframe[dataframe.columns[1]].iloc[index - 1]
        y2 = 0.3
        x2 = x0 + (x1 - x0) * (y2 - y0) / (y1 - y0)

        return x2
    else:
        return None


def delete_cache(dataframe: pd.DataFrame):
    key = (dataframe.columns[0], dataframe.columns[1])
    get_durability_from_dataframe.param.pop(key, None)
