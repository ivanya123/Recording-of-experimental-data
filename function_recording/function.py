import tkinter as tk



def check_float(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False


def plus(event, spinbox, step=1, func=None):
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


def on_mouse_wheel(event, canvas):
    if event.delta:
        canvas.xview_scroll(-1 * int(event.delta / 120), "units")
    else:
        if event.num == 4:
            canvas.xview_scroll(-1, "units")
        elif event.num == 5:
            canvas.xview_scroll(1, "units")


def enter(event: str, label: tk.LabelFrame) -> None:
    scroll_pos = label.master.master.xview()

    label.config(bg="lightblue")
    label.update_idletasks()
    label.master.master.xview_moveto(scroll_pos[0])

def leave(event: str, label: tk.LabelFrame) -> None:
    scroll_pos = label.master.master.xview()

    label.config(bg="SystemButtonFace")
    label.update_idletasks()
    label.master.master.xview_moveto(scroll_pos[0])


def interpolate_data(data_frame):
    """Интерполирует пропущенные значения в DataFrame."""
    return data_frame.interpolate(method='linear', limit_direction='forward', axis=0)