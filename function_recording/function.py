def check_float(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False


def plus(event, spinbox, step=1, func = None):
    if check_float(spinbox.get()):
        if event.delta < 0:
            num = float(spinbox.get())
            spinbox.delete(0, len(spinbox.get()))
            spinbox.insert(0, round((num - step), 3))
        else:
            num = float(spinbox.get())
            spinbox.delete(0, len(spinbox.get()))
            spinbox.insert(0, round((num + step), 3))

    if func is not None:
        func()

def on_mouse_wheel(event, canvas):
    if event.delta:
        canvas.xview_scroll(-1 * int(event.delta / 120), "units")
    else:
        if event.num == 4:
            canvas.xview_scroll(-1, "units")
        elif event.num == 5:
            canvas.xview_scroll(1, "units")


