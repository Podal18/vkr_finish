# main.py
from PyQt6 import QtWidgets
from ui.vhod import Ui_login_widget
from ui.registration_window import Ui_registration_widget
from ui.password_reset_window import Ui_PasswordResetWindow
from ui.admin_main_window import Ui_AdminMainWindow
from ui.hr_main_window import HRMainWindow
import pymysql

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
        login = self.ui.login_email_input.text().strip()
        password = self.ui.login_password_input.text().strip()

        try:
            con = pymysql.connect(host="localhost", user="root", password="",
                                  database="diplom", port=3312)
            cur = con.cursor()
            cur.execute("SELECT id, password_hash, role FROM users WHERE login = %s", (login,))
            result = cur.fetchone()

            if not result:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
                return

            user_id, stored_hash, role = result

            if password != stored_hash:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
                return

            # Логирование входа
            from utils.logger import log_action
            log_action(user_id=user_id, action="Вход", description=f"Пользователь с ID {user_id} вошёл в систему")

            # Открытие окна по роли
            if role == 3:  # HR
                self.current_window = HRMainWindow(user_id=user_id)
            elif role == 1:  # Admin
                self.current_window = Adm_Window()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неизвестная роль")
                return

            self.current_window.show()
            self.hide()
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
