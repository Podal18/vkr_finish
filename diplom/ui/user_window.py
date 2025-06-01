from PyQt6 import QtCore, QtWidgets
from db.db import get_connection


class EmployeeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сотрудники")
        self.resize(1000, 600)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9a9e, stop:1 #fad0c4);
                border-radius: 10px;
            }
        """)

        self.title_label = QtWidgets.QLabel("Список сотрудников", self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        self.back_button = QtWidgets.QPushButton("← Назад", self.background)
        self.back_button.setGeometry(30, 540, 100, 40)
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
        self.back_button.clicked.connect(self.close)

        # Таблица
        self.table = QtWidgets.QTableWidget(self.background)
        self.table.setGeometry(30, 80, 940, 440)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ФИО", "Должность", "Дата рождения", "Статус"])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #fcb1b6;
                padding: 4px;
                font-weight: bold;
                border: 1px solid white;
            }
        """)

        self.load_employees()

    def load_employees(self):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT full_name, profession, birth_date, is_active FROM employees")
                employees = cursor.fetchall()
                self.table.setRowCount(len(employees))
                for row, emp in enumerate(employees):
                    self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(emp["full_name"]))
                    self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(emp["profession"] or "—"))
                    self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(emp["birth_date"].strftime("%d.%m.%Y")))
                    status_text = "Активен" if emp["is_active"] else "Неактивен"
                    self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(status_text))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()


# Тестовое открытие
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = EmployeeWindow()
    win.show()
    sys.exit(app.exec())
