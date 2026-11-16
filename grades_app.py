import sys
import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QLabel,
    QFileDialog, QMessageBox
)

class GradesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grades Editor")
        self.resize(600, 700)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""
        self.header = ""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        self.btn_load = QPushButton("Load Grades File")
        self.btn_load.clicked.connect(self.load_file)
        top_layout.addWidget(self.btn_load)

        self.btn_about = QPushButton("About")
        self.btn_about.clicked.connect(self.show_about)
        top_layout.addWidget(self.btn_about)
        main_layout.addLayout(top_layout)

        bonus_layout = QHBoxLayout()
        self.lbl_bonus = QLabel("Bonus Points (Press Enter):")
        self.spin_bonus = QSpinBox()
        self.spin_bonus.setRange(-100, 100)
        self.spin_bonus.editingFinished.connect(self.apply_bonus)
        bonus_layout.addWidget(self.lbl_bonus)
        bonus_layout.addWidget(self.spin_bonus)
        main_layout.addLayout(bonus_layout)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        self.btn_update = QPushButton("Update File")
        self.btn_update.clicked.connect(self.update_file)
        main_layout.addWidget(self.btn_update)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Grades CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        self.selected_file = file_path
        self.student_ids.clear()
        self.original_grades.clear()
        self.corrected_grades.clear()

        f = open(self.selected_file, "r", encoding="utf-8-sig")
        lines = f.readlines()
        f.close()

        self.header = lines[0].strip()
        for line in lines[1:]:
            clean_line = line.strip()
            if clean_line != "":
                parts = clean_line.split(",")
                self.student_ids.append(parts[0])
                grade = float(parts[1])
                self.original_grades.append(grade)
                self.corrected_grades.append(grade)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(len(self.student_ids))
        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.student_ids[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))
    
    def apply_bonus(self):
        bonus = self.spin_bonus.value()
        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade
        self.update_table()

    def update_file(self):
        if not self.selected_file:
            return

        f = open(self.selected_file, "w", encoding="utf-8-sig")
        f.write(self.header + "\n")
        for i in range(len(self.student_ids)):
            f.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")
        f.close()

        if sys.platform.startswith("win"):
            os.startfile(self.selected_file)
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", self.selected_file])
        else:
            subprocess.call(["xdg-open", self.selected_file])

    def show_about(self):
        QMessageBox.about(self, "About", "Grades Editor App\nGitHub: https://github.com/sharabi-stud/Exercise4")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists("style.qss"):
        f = open("style.qss", "r")
        app.setStyleSheet(f.read())
        f.close()
    window = GradesWindow()
    window.show()
    sys.exit(app.exec())
