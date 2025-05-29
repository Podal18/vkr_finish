from PyQt6 import QtCore, QtWidgets
from logic.employee_func import get_all_employees
from logic.employee_func import add_employee, load_employee_profile, get_all_professions
from ui.add_edit_employee import Ui_AddEditEmployeeWindow
from logic import employee_func
from ui.employee_profile import Ui_EmployeeProfileWindow


class Ui_EmployeeWindow(object):
    def setupUi(self, EmployeeWindow):
        EmployeeWindow.setObjectName("EmployeeWindow")
        EmployeeWindow.resize(1000, 600)
        EmployeeWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        EmployeeWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(EmployeeWindow)
        EmployeeWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fdfbfb, stop:1 #ebedee);
                border-radius: 10px;
            }
        """)

        self.exit_button = QtWidgets.QPushButton(parent=EmployeeWindow)
        self.exit_button.setGeometry(QtCore.QRect(960, 10, 30, 30))
        self.exit_button.setText("✕")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                font-size: 18px;
                color: #444;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.exit_button.clicked.connect(EmployeeWindow.close)

        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Сотрудники")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        self.employee_table = QtWidgets.QTableWidget(self.background)
        self.employee_table.setGeometry(30, 80, 940, 380)
        self.employee_table.setColumnCount(6)
        self.employee_table.setHorizontalHeaderLabels([
            "ФИО", "Профессия", "Объект", "Статус", "Документы", "Действия"
        ])
        self.employee_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.employee_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.employee_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #c0c0ff;
                padding: 4px;
                font-weight: bold;
                border: 1px solid white;
            }
        """)
        self.employee_table.setColumnCount(7)
        self.employee_table.setHorizontalHeaderLabels([
            "ID", "ФИО", "Профессия", "Объект", "Статус", "Документы", "Действия"
        ])
        self.employee_table.setColumnHidden(0, True)

        # Кнопки
        self.add_button = QtWidgets.QPushButton("➕ Добавить", self.background)
        self.add_button.setGeometry(100, 480, 160, 50)
        self.add_button.clicked.connect(self.open_add_employee_window)

        self.edit_button = QtWidgets.QPushButton("✏️ Изменить", self.background)
        self.edit_button.setGeometry(280, 480, 160, 50)
        self.edit_button.clicked.connect(self.open_edit_employee_window)

        self.fire_button = QtWidgets.QPushButton("🟥 Уволить", self.background)
        self.fire_button.setGeometry(460, 480, 160, 50)
        self.fire_button.clicked.connect(self.fire_employee)

        self.profile_button = QtWidgets.QPushButton("📄 Профиль", self.background)
        self.profile_button.setGeometry(640, 480, 160, 50)
        self.profile_button.clicked.connect(self.open_profile)

        for btn in [self.add_button, self.edit_button, self.fire_button, self.profile_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #c0c0ff;
                    color: white;
                    border-radius: 20px;
                    font-size: 15px;
                }
                QPushButton:hover {
                    background-color: #9999ff;
                }
            """)

        self.load_employees()  # ← загружаем сотрудников из БД

    def load_employees(self):
        employees = get_all_employees()
        self.employee_table.setRowCount(0)

        for row_idx, emp in enumerate(employees):
            self.employee_table.insertRow(row_idx)
            self.employee_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(emp["id"])))
            self.employee_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(emp["full_name"]))
            self.employee_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(emp["profession"]))
            self.employee_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem("-"))  # объект
            self.employee_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(emp["status"]))
            self.employee_table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem("Документы"))
            self.employee_table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem("..."))



    def open_add_employee_window(self):
        self.add_window = QtWidgets.QMainWindow()
        self.add_ui = Ui_AddEditEmployeeWindow()
        self.add_ui.setupUi(self.add_window, mode="add")

        try:
            self.add_ui.save_button.clicked.disconnect()
        except TypeError:
            pass  # Игнорируем ошибку, если сигнал не был подключен

            # Загружаем профессии и заполняем комбобокс
        self.add_ui.profession_map = {}


        self.add_ui.save_button.clicked.connect(self.save_new_employee)

        self.add_window.show()

    def save_new_employee(self):
        full_name = self.add_ui.fullname_input.text()
        birth_date = self.add_ui.birthdate_input.date().toString("yyyy-MM-dd")
        profession = self.add_ui.profession_combo.currentText()

        if not full_name or not profession:
            QtWidgets.QMessageBox.warning(self.add_window, "Ошибка", "Заполните все поля.")
            return
        profession_id = self.add_ui.profession_map.get(profession)


        add_employee(full_name, birth_date, profession_id, 1)
        QtWidgets.QMessageBox.information(self.add_window, "Готово", "Сотрудник добавлен.")
        self.add_window.close()
        self.load_employees()

    def open_edit_employee_window(self):
        selected = self.employee_table.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Выберите сотрудника для редактирования.")
            return

        emp_id = int(self.employee_table.item(selected, 0).text())

        self.edit_window = QtWidgets.QMainWindow()
        self.edit_ui = Ui_AddEditEmployeeWindow()
        self.edit_ui.setupUi(self.edit_window, mode="edit", employee_id=emp_id)
        self.edit_ui.save_button.clicked.connect(self.load_employees)
        self.edit_window.show()

    def fire_employee(self):
        selected = self.employee_table.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите сотрудника для увольнения.")
            return
        emp_id = self.employee_table.item(selected, 0).text()
        confirm = QtWidgets.QMessageBox.question(None, "Подтверждение", "Уволить выбранного сотрудника?",
                                                 QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            success = employee_func.fire_employee(emp_id)
            self.load_employees()
            QtWidgets.QMessageBox.critical(None, "Успешно", "Сотрудник уволен.")

    def open_profile(self):
        selected = self.employee_table.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите сотрудника для просмотра профиля.")
            return

        emp_id = self.employee_table.item(selected, 0).text()

        self.profile_window = QtWidgets.QMainWindow()
        self.profile_ui = Ui_EmployeeProfileWindow()
        self.profile_ui.setupUi(self.profile_window)
        load_employee_profile(self.profile_ui, emp_id)
        self.profile_window.show()

class EmployeeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EmployeeWindow()
        self.ui.setupUi(self)
        self.ui.load_employees()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_EmployeeWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
