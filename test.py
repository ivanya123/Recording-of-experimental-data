from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")


def dismiss(window):
    window.grab_release()
    window.destroy()


def click():
    window = Toplevel()
    window.title("Новое окно")
    window.geometry("250x200")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))  # перехватываем нажатие на крестик
    close_button = ttk.Button(window, text="Закрыть окно", command=lambda: dismiss(window))
    close_button.pack(anchor="center", expand=1)
    window.grab_set()  # захватываем пользовательский ввод


open_button = ttk.Button(text="Создать окно", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()