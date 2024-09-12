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
            spinbox.insert(0, round((num - step), 2))
        else:
            num = float(spinbox.get())
            spinbox.delete(0, len(spinbox.get()))
            spinbox.insert(0, round((num + step), 2))

    if func is not None:
        func()


