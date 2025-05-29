from PyQt6 import QtCore, QtWidgets
from logic.auto_func import register_user

class Ui_registration_widget(object):
    def setupUi(self, registration_widget, parent_stack=None, parent_window=None):
        self.parent_stack = parent_stack
        self.parent_window = parent_window
        registration_widget.setObjectName("registration_widget")
        registration_widget.resize(400, 500)
        registration_widget.setWindowTitle("Регистрация")
        #registration_widget.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        #registration_widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.background = QtWidgets.QFrame(parent=registration_widget)
        self.background.setGeometry(QtCore.QRect(0, 0, 400, 500))
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
                border-radius: 0px;
            }
        """)

        self.label = QtWidgets.QLabel(parent=registration_widget)
        self.label.setGeometry(QtCore.QRect(110, 30, 180, 50))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setText("Регистрация")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        self.login_input = QtWidgets.QLineEdit(parent=registration_widget)
        self.login_input.setGeometry(QtCore.QRect(100, 90, 200, 45))
        self.login_input.setPlaceholderText("Логин")

        self.password_input = QtWidgets.QLineEdit(parent=registration_widget)
        self.password_input.setGeometry(QtCore.QRect(100, 150, 200, 45))
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.fullname_input = QtWidgets.QLineEdit(parent=registration_widget)
        self.fullname_input.setGeometry(QtCore.QRect(100, 210, 200, 45))
        self.fullname_input.setPlaceholderText("ФИО")

        self.role_combo = QtWidgets.QComboBox(parent=registration_widget)
        self.role_combo.setGeometry(QtCore.QRect(100, 270, 200, 45))
        self.role_combo.addItems(["HR", "Foreman", "SafetyEngineer", "Admin"])

        self.register_button = QtWidgets.QPushButton("Зарегистрироваться", parent=registration_widget)
        self.register_button.setGeometry(QtCore.QRect(120, 340, 160, 50))
        self.register_button.clicked.connect(self.try_register)

        self.back_button = QtWidgets.QPushButton("← Назад", parent=registration_widget)
        self.back_button.setGeometry(QtCore.QRect(120, 410, 160, 40))
        self.back_button.clicked.connect(self.return_to_login)

        self.exit_button = QtWidgets.QPushButton("✕", parent=registration_widget)
        self.exit_button.setGeometry(QtCore.QRect(360, 10, 30, 30))
        self.exit_button.clicked.connect(QtWidgets.QApplication.quit)

        registration_widget.setStyleSheet("""
            QLineEdit, QComboBox {
                border: 2px solid #b0d4ff;
                border-radius: 22px;
                background-color: white;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                border-radius: 25px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
                color: white;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #8bb8f5;
            }
        """)

        QtCore.QMetaObject.connectSlotsByName(registration_widget)


    def try_register(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        full_name = self.fullname_input.text().strip()
        role = self.role_combo.currentText()

        if not login or not password or not full_name:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Заполните все поля.")
            return

        success = register_user(login, password, role, full_name)
        if success:
            QtWidgets.QMessageBox.information(None, "Успех", "Пользователь зарегистрирован.")
            if self.parent_stack:
                self.parent_stack.setCurrentIndex(0)  # Вернуться в авторизацию
        else:
            QtWidgets.QMessageBox.critical(None, "Ошибка", "Логин занят или роль недопустима.")

    def return_to_login(self):
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(0)  # Авторизация




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_registration_widget()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())

