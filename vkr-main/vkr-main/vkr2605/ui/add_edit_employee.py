from PyQt6 import QtCore, QtWidgets
from logic.employee_func import (
    add_employee,
    get_all_professions,
    get_employee_by_id,
    update_employee
)

class Ui_AddEditEmployeeWindow(object):
    def setupUi(self, AddEditEmployeeWindow, mode="add", created_by_id=None, employee_id=None):
        self.mode = mode
        self.created_by_id = created_by_id
        self.employee_id = employee_id
        self.profession_map = {}  # {название: id}

        AddEditEmployeeWindow.setObjectName("AddEditEmployeeWindow")
        AddEditEmployeeWindow.resize(500, 450)
        AddEditEmployeeWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        AddEditEmployeeWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(AddEditEmployeeWindow)
        AddEditEmployeeWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 500, 450)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
                border-radius: 10px;
            }
        """)

        # ✕ и ← Назад
        self.exit_button = QtWidgets.QPushButton(parent=AddEditEmployeeWindow)
        self.exit_button.setGeometry(QtCore.QRect(460, 10, 30, 30))
        self.exit_button.setText("✕")
        self.exit_button.clicked.connect(AddEditEmployeeWindow.close)

        self.back_button = QtWidgets.QPushButton("← Назад", self.background)
        self.back_button.setGeometry(30, 390, 120, 40)
        self.back_button.clicked.connect(AddEditEmployeeWindow.close)

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 440, 40)
        self.title_label.setText("Добавить сотрудника" if mode == "add" else "Редактировать сотрудника")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        # Поля ввода
        self.fullname_input = self.create_input("ФИО", 90)

        self.birthdate_input = QtWidgets.QDateEdit(self.background)
        self.birthdate_input.setGeometry(50, 150, 400, 40)
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setStyleSheet(self.input_style())

        self.profession_combo = QtWidgets.QComboBox(self.background)
        self.profession_combo.setGeometry(50, 210, 400, 40)
        self.profession_combo.setStyleSheet(self.input_style())
        self.load_professions()

        self.save_button = QtWidgets.QPushButton("💾 Сохранить", self.background)
        self.save_button.setGeometry(180, 300, 150, 50)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #7da2f2;
                color: white;
                border-radius: 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #5c8ee6;
            }
        """)
        self.save_button.clicked.connect(lambda: self.save(AddEditEmployeeWindow))

        # Если редактирование — загрузить данные
        if self.mode == "edit" and self.employee_id:
            self.load_employee_data()

    def create_input(self, placeholder, y):
        input_field = QtWidgets.QLineEdit(self.background)
        input_field.setGeometry(50, y, 400, 40)
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(self.input_style())
        return input_field

    def input_style(self):
        return """
            QLineEdit, QComboBox, QDateEdit {
                border: 2px solid #b0d4ff;
                border-radius: 20px;
                background-color: white;
                padding: 10px;
                font-size: 15px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #7da2f2;
            }
        """

    def load_professions(self):
        professions = get_all_professions()
        self.profession_combo.clear()
        for prof in professions:
            name = prof["name"]
            pid = prof["id"]
            self.profession_combo.addItem(name)
            self.profession_map[name] = pid

    def load_employee_data(self):
        data = get_employee_by_id(self.employee_id)
        if not data:
            QtWidgets.QMessageBox.critical(None, "Ошибка", "Сотрудник не найден.")
            return

        self.fullname_input.setText(data["full_name"])
        self.birthdate_input.setDate(QtCore.QDate.fromString(str(data["birth_date"]), "yyyy-MM-dd"))

        for name, pid in self.profession_map.items():
            if pid == data["profession_id"]:
                index = self.profession_combo.findText(name)
                if index >= 0:
                    self.profession_combo.setCurrentIndex(index)

    def save(self, window):
        full_name = self.fullname_input.text()
        birth_date = self.birthdate_input.date().toString("yyyy-MM-dd")
        profession_name = self.profession_combo.currentText()

        if not full_name or not profession_name:
            QtWidgets.QMessageBox.warning(window, "Ошибка", "Заполните все поля.")
            return

        profession_id = self.profession_map.get(profession_name)

        if self.mode == "add":
            add_employee(full_name, birth_date, profession_id, self.created_by_id)
            QtWidgets.QMessageBox.information(window, "Готово", "Сотрудник добавлен.")
        else:
            update_employee(self.employee_id, full_name, birth_date, profession_id)
            QtWidgets.QMessageBox.information(window, "Готово", "Данные сотрудника обновлены.")

        window.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_AddEditEmployeeWindow()
    ui.setupUi(window, mode="add")
    window.show()
    sys.exit(app.exec())