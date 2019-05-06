import plotly.plotly as py
from plotly.offline import download_plotlyjs, plot, iplot
import cufflinks as cf
import tkinter as tk
import platform
from productivity_app.components import menu
if 'Windows' in platform.platform():
    from win32api import GetSystemMetrics


def main():
    root = tk.Tk()
    print(GetSystemMetrics(0))
    root.geometry(newGeometry='{width}x{height}'.format(width=int(GetSystemMetrics(0) / 2),
                                                        height=int(GetSystemMetrics(1) / 2)))
    root.title('Generic Productivity Tracker')
    root.config(menu=menu.get_pa_menu(root))

    root.mainloop()


if __name__ == '__main__':
    main()
