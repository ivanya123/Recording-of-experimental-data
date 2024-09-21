import tkinter as tk
import tkinter.ttk as ttk


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
