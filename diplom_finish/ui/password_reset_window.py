from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PasswordResetWindow(object):
    def setupUi(self, PasswordResetWindow, parent_stack=None, parent_window=None):
        self.parent_stack = parent_stack
        self.parent_window = parent_window
        PasswordResetWindow.setObjectName("PasswordResetWindow")
        PasswordResetWindow.resize(500, 400)
        PasswordResetWindow.setWindowTitle("Сброс пароля")
        #PasswordResetWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        #PasswordResetWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(PasswordResetWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 500, 400))

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 500, 400)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fbc2eb, stop:1 #a6c1ee);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=PasswordResetWindow)
        self.exit_button.setGeometry(QtCore.QRect(460, 10, 30, 30))
        self.exit_button.setText("✕")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                font-size: 18px;
                color: white;
            }
            QPushButton:hover {
                color: #ffdddd;
            }
        """)
        self.exit_button.clicked.connect(PasswordResetWindow.close)

        # ← Назад
        self.back_button = QtWidgets.QPushButton("←", parent=PasswordResetWindow)
        self.back_button.setGeometry(30, 340, 60, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                font-size: 14px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.back_button.clicked.connect(self.back_to_login)

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 440, 40)
        self.title_label.setText("Сброс пароля пользователя")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        # Поиск пользователя
        self.login_input = QtWidgets.QLineEdit(self.background)
        self.login_input.setGeometry(50, 90, 400, 40)
        self.login_input.setPlaceholderText("Введите логин пользователя")
        self.login_input.setStyleSheet(self.input_style())

        # Новый пароль
        self.new_password_input = QtWidgets.QLineEdit(self.background)
        self.new_password_input.setGeometry(50, 150, 400, 40)
        self.new_password_input.setPlaceholderText("Новый пароль")
        self.new_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.new_password_input.setStyleSheet(self.input_style())

        # Подтверждение
        self.confirm_password_input = QtWidgets.QLineEdit(self.background)
        self.confirm_password_input.setGeometry(50, 210, 400, 40)
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet(self.input_style())

        # Кнопка сброса
        self.reset_button = QtWidgets.QPushButton("🔁 Сбросить пароль", self.background)
        self.reset_button.setGeometry(150, 280, 200, 50)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #a6c1ee;
                color: white;
                font-size: 15px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #8aa8e3;
            }
        """)
        self.reset_button.clicked.connect(lambda: self.handle_password_reset(PasswordResetWindow))


    def handle_password_reset(self, window):
        from logic.auto_func import reset_password

        login = self.login_input.text().strip()
        new_pass = self.new_password_input.text()
        confirm_pass = self.confirm_password_input.text()

        if not login or not new_pass or not confirm_pass:
            QtWidgets.QMessageBox.warning(window, "Ошибка", "Все поля должны быть заполнены")
            return

        if new_pass != confirm_pass:
            QtWidgets.QMessageBox.warning(window, "Ошибка", "Пароли не совпадают")
            return

        success, message = reset_password(login, new_pass)
        if success:
            QtWidgets.QMessageBox.information(window, "Успех", message)

        else:
            QtWidgets.QMessageBox.critical(window, "Ошибка", message)

    def input_style(self):
        return """
            QLineEdit {
                border: 2px solid #d9d9f3;
                border-radius: 20px;
                background-color: white;
                padding: 10px;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #a6c1ee;
            }
        """

    def back_to_login(self):
        if self.parent_window:
            self.parent_window.resize_for(0)
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(0)


# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_PasswordResetWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
