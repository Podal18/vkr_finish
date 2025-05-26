from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_UserWindow(object):
    def setupUi(self, UserWindow):
        UserWindow.setObjectName("UserWindow")
        UserWindow.resize(1000, 600)
        UserWindow.setWindowTitle("Управление пользователями")
        UserWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        UserWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(UserWindow)
        UserWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #89f7fe, stop:1 #66a6ff);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=UserWindow)
        self.exit_button.setGeometry(QtCore.QRect(960, 10, 30, 30))
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
        self.exit_button.clicked.connect(UserWindow.close)

        # ← Назад
        self.back_button = QtWidgets.QPushButton("←", self.background)
        self.back_button.setGeometry(30, 540, 60, 40)
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
        self.back_button.clicked.connect(UserWindow.close)

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Пользователи системы")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Кнопки действия


        self.edit_user_button = QtWidgets.QPushButton("✏️ Редактировать", self.background)
        self.edit_user_button.setGeometry(340, 500, 160, 50)

        self.delete_user_button = QtWidgets.QPushButton("🗑️ Удалить", self.background)
        self.delete_user_button.setGeometry(700, 500, 160, 50)

        # Таблица пользователей
        self.user_table = QtWidgets.QTableWidget(self.background)
        self.user_table.setGeometry(30, 90, 940, 390)
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ФИО", "Логин", "Роль", "Статус", "Последний вход"])
        self.user_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.user_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.user_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #a0c4ff;
                padding: 4px;
                font-weight: bold;
                border: 1px solid white;
            }
        """)

        self.fade_animation(UserWindow)

    def fade_animation(self, widget):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

from PyQt6 import QtWidgets
from db.db import get_connection

class UserWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self)
        self.setup_connections()
        self.load_users()

    def setup_connections(self):
        self.ui.edit_user_button.clicked.connect(self.load_users)
        self.ui.back_button.clicked.connect(self.close)
        self.ui.delete_user_button.clicked.connect(self.delete_user)

    def load_users(self):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.full_name, u.login, r.name AS role, e.status
                    FROM employees e
                    LEFT JOIN users u ON u.id = e.created_by
                    LEFT JOIN roles r ON u.role_id = r.id
                    group by e.full_name, u.login, r.name, e.status
                """)
                rows = cursor.fetchall()
                self.ui.user_table.setRowCount(0)
                for i, row in enumerate(rows):
                    self.ui.user_table.insertRow(i)
                    self.ui.user_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row["full_name"])))
                    self.ui.user_table.setItem(i, 1, QtWidgets.QTableWidgetItem(row["login"]))
                    self.ui.user_table.setItem(i, 2, QtWidgets.QTableWidgetItem(row["role"] or ""))
                    self.ui.user_table.setItem(i, 3, QtWidgets.QTableWidgetItem("Активен"))
        finally:
            connection.close()

    def delete_user(self):
        selected = self.ui.user_table.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Выберите пользователя для удаления.")
            return

        user_id = self.ui.user_table.item(selected, 0).text()
        login = self.ui.user_table.item(selected, 1).text()

        confirm = QtWidgets.QMessageBox.question(
            self, "Подтверждение",
            f"Удалить пользователя {login}?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Готово", "Пользователь удалён.")
                self.load_users()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
                print(e)
            finally:
                connection.close()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UserWindow()
    window.show()
    sys.exit(app.exec())