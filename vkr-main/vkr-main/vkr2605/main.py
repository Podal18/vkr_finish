# main.py
from PyQt6 import QtWidgets
from ui.vhod import Ui_login_widget
from ui.registration_window import Ui_registration_widget
from ui.password_reset_window import Ui_PasswordResetWindow
from ui.foreman_main_window import Ui_ForemanMainWindow
from ui.hr_main_window import Ui_HRMainWindow
from ui.admin_main_window import Ui_AdminMainWindow
from ui.safety_main_window import Ui_SafetyMainWindow
import pymysql
import hashlib

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login_widget()
        self.ui.setupUi(self)
        self.ui.to_register_button.clicked.connect(self.open_registration)
        self.ui.forgot_password_button.clicked.connect(self.open_password_reset)
        self.ui.login_button.clicked.connect(self.show_main_window)

    def open_registration(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
        self.hide()

    def open_password_reset(self):
        self.password_reset_window = PasswordResetWindow()
        self.password_reset_window.show()
        self.hide()

    def show_main_window(self):
        login = self.ui.login_email_input.text()
        password = self.ui.login_password_input.text()  # Исправлено имя поля

        try:
            con = pymysql.connect(host="localhost", user="root", password="",
                                  database="hr_integration", port=3312)
            cur = con.cursor()

            sql = "SELECT password_hash, role_id FROM users WHERE login = %s"
            cur.execute(sql, (login,))
            result = cur.fetchone()

            if not result:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
                return

            stored_hash, role = result  # Распаковываем кортеж

            # Хэшируем введенный пароль
            input_hash = hashlib.sha256(password.encode()).hexdigest()

            if input_hash != stored_hash:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
                return

            # Открываем окно в зависимости от роли
            if role == 1:
                window = HR_Window()
            elif role == 2:
                window = Fore_Window()
            elif role == 3:
                window = Saf_Window()
            elif role == 4:
                window = Adm_Window()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неизвестная роль")
                return

            self.current_window = window  # Сохраняем ссылку
            self.hide()
            self.current_window.show()

            con.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"{e}")
            print(e)


class RegistrationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_registration_widget()
        self.ui.setupUi(self)
        self.ui.back_button.clicked.connect(self.return_to_login)

    def return_to_login(self):
        self.parent_window = LoginWindow()
        self.parent_window.show()
        self.close()


class PasswordResetWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PasswordResetWindow()
        self.ui.setupUi(self)
        self.ui.back_button.clicked.connect(self.return_to_login)

    def return_to_login(self):
        self.parent_window = LoginWindow()
        self.parent_window.show()
        self.close()

class HR_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HRMainWindow()
        self.ui.setupUi(self)
        self.ui.exit_btn.clicked.connect(self.return_to_login)

    def return_to_login(self):
        self.parent_window = LoginWindow()
        self.parent_window.show()
        self.close()

class Fore_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ForemanMainWindow()
        self.ui.setupUi(self)
        self.ui.exit_btn.clicked.connect(self.return_to_login)

    def return_to_login(self):
        self.parent_window = LoginWindow()
        self.parent_window.show()
        self.close()

class Saf_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SafetyMainWindow()
        self.ui.setupUi(self)
        self.ui.exit_btn.clicked.connect(self.return_to_login)

    def return_to_login(self):
        self.parent_window = LoginWindow()
        self.parent_window.show()
        self.close()

class Adm_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminMainWindow()
        self.ui.setupUi(self)
        self.ui.exit_btn.clicked.connect(self.return_to_login)

    def return_to_login(self):
        self.parent_window = LoginWindow()
        self.parent_window.show()
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())