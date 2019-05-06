import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from productivity_app.lib.menu_generator import generate_menu


def get_menu_options(root):
    return [['File', {'Open': file_open, 'Save': file_save, 'Sep1': None, 'Quit': root.quit}],
            ['About', {'About Author': about_author}],
            ['Help', {'Help': help}]]


def get_pa_menu(root):
    menu = tk.Menu(root)
    root.config(menu=menu)
    for menu_name, options in get_menu_options(root):
        generate_menu(menu, menu_name, **options)
    return menu


def file_new():
    pass


def file_open():
    name = askopenfilename()
    print(name)


def file_save():
    pass


def file_save_as():
    pass
    # asksaveasfilename()


def about_author():
    pass


def help():
    return tk.Message('Help Message')
