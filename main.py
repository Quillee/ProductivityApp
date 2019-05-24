import plotly.plotly as py
from plotly.offline import download_plotlyjs, plot, iplot
import cufflinks as cf
import sys
from PyQt5.QtWidgets import QApplication, QWidget
import platform
if 'Windows' in platform.platform():
    from win32api import GetSystemMetrics


def main():
    root = QApplication([])
    window = QWidget()
    window.setGeometry(50, 50, 500, 300)
    window.show()

    sys.exit(root.exec_())


if __name__ == '__main__':
    main()
