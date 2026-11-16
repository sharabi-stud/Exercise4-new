import sys
import os
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class IceCreamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Sales Analysis")
        self.resize(800, 600)

        self.temperatures = []
        self.revenues = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        self.btn_load = QPushButton("Load Data File")
        self.btn_load.clicked.connect(self.load_file)
        top_layout.addWidget(self.btn_load)

        self.btn_about = QPushButton("About")
        self.btn_about.clicked.connect(self.show_about)
        top_layout.addWidget(self.btn_about)
        main_layout.addLayout(top_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)

        self.plot_graph()

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Ice Cream CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        self.temperatures.clear()
        self.revenues.clear()

        f = open(file_path, "r", encoding="utf-8-sig")
        lines = f.readlines()
        f.close()

        for line in lines[1:]:
            clean_line = line.strip()
            if clean_line != "":
                parts = clean_line.split(",")
                self.temperatures.append(float(parts[0]))
                self.revenues.append(float(parts[1]))

        self.plot_graph()

    def plot_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if len(self.temperatures) > 0 and len(self.revenues) > 0:
            ax.scatter(self.temperatures, self.revenues, s=1)

            x = np.array(self.temperatures)
            y = np.array(self.revenues)
            m, b = np.polyfit(x, y, 1)
            ax.plot(x, m * x + b, color="red", label=f"y = {m:.2f}x + {b:.2f}")
            ax.legend()

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title("Ice Cream Revenue vs Temperature")
        ax.set_xlabel("Temperature")
        ax.set_ylabel("Revenue")

        self.canvas.draw()

    def show_about(self):
        QMessageBox.about(self, "About", "Ice Cream Revenue Analysis\nGitHub: https://github.com/sharabi-stud/Exercise4-new")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists("style.qss"):
        f = open("style.qss", "r")
        app.setStyleSheet(f.read())
        f.close()
    window = IceCreamWindow()
    window.show()
    sys.exit(app.exec())