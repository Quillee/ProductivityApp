import tkinter as tk


def generate_menu(root, cascade_name, **menu_options):
    """Generates a menu that then uses the root parameter as it's master.
        root should always be another Menu object, should not be the actual root of the application
    """
    menu = tk.Menu(root)
    root.add_cascade(label=cascade_name, menu=menu)
    #@TEMP: Let's see if we can not do this root.config(menu) #@Unpure: Uh-oh do we want to modify root in this function?????
    for key, lam in menu_options.items():
        if lam is None:
            menu.add_separator()
            continue
        menu.add_command(label=key, command=lam)
    return menu
