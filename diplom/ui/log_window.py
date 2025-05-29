from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LogWindow(object):
    def setupUi(self, LogWindow):
        LogWindow.setObjectName("LogWindow")
        LogWindow.resize(1000, 600)
        LogWindow.setWindowTitle("Журнал действий")
        LogWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        LogWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(LogWindow)
        LogWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d4fc79, stop:1 #96e6a1);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=LogWindow)
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
        self.exit_button.clicked.connect(LogWindow.close)

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
        self.back_button.clicked.connect(LogWindow.close)

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Журнал действий пользователей")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Панель фильтрации
        self.filter_frame = QtWidgets.QFrame(self.background)
        self.filter_frame.setGeometry(30, 70, 940, 60)
        self.filter_frame.setStyleSheet("background-color: rgba(255,255,255,0.9); border-radius: 10px;")

        self.user_input = QtWidgets.QLineEdit(self.filter_frame)
        self.user_input.setPlaceholderText("Поиск по ФИО / логину")
        self.user_input.setGeometry(20, 10, 250, 40)

        self.action_combo = QtWidgets.QComboBox(self.filter_frame)
        self.action_combo.setGeometry(290, 10, 200, 40)
        self.action_combo.addItems(["Все действия", "Вход", "Добавление", "Редактирование", "Удаление"])

        self.search_button = QtWidgets.QPushButton("🔍 Найти", self.filter_frame)
        self.search_button.setGeometry(510, 10, 100, 40)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #96e6a1;
                color: white;
                border-radius: 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #7ddf94;
            }
        """)

        # Таблица логов
        self.log_table = QtWidgets.QTableWidget(self.background)
        self.log_table.setGeometry(30, 150, 940, 360)
        self.log_table.setColumnCount(4)
        self.log_table.setHorizontalHeaderLabels(["Дата", "Пользователь", "Действие", "Описание"])
        self.log_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.log_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.log_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #b0f2c2;
                padding: 4px;
                font-weight: bold;
                border: 1px solid white;
            }
        """)


from PyQt6 import QtCore, QtWidgets
from db.db import get_connection


class LogWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LogWindow()
        self.ui.setupUi(self)
        self.setup_connections()
        self.load_logs()
        self.setup_table()

    def setup_connections(self):
        """Подключение сигналов"""
        self.ui.search_button.clicked.connect(self.apply_filters)
        self.ui.user_input.textChanged.connect(self.apply_filters)
        self.ui.action_combo.currentIndexChanged.connect(self.apply_filters)

    def setup_table(self):
        """Настройка таблицы"""
        self.ui.log_table.setColumnWidth(0, 150)  # Дата
        self.ui.log_table.setColumnWidth(1, 200)  # Пользователь
        self.ui.log_table.setColumnWidth(2, 150)  # Действие
        self.ui.log_table.setColumnWidth(3, 400)  # Описание

    def load_logs(self):
        """Загрузка логов из БД"""
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        l.log_date,
                        u.login,
                        l.action,
                        e.full_name as employee_name
                    FROM logs l
                    LEFT JOIN users u ON l.user_id = u.id
                    LEFT JOIN employees e ON l.employee_id = e.id
                    ORDER BY l.log_date DESC
                """)
                self.all_logs = cursor.fetchall()
                self.apply_filters()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()

    def apply_filters(self):
        """Применение фильтров"""
        search_text = self.ui.user_input.text().lower()
        action_filter = self.ui.action_combo.currentText()

        filtered = []

        for log in self.all_logs:
            # Фильтр по тексту
            if search_text:
                if (search_text not in log["login"].lower() and
                        search_text not in (log["employee_name"] or "").lower()):
                    continue

            # Фильтр по действию
            if action_filter != "Все действия":
                if action_filter not in log["action"]:
                    continue

            filtered.append(log)

        self.update_table(filtered)

    def update_table(self, logs):
        """Обновление таблицы"""
        self.ui.log_table.setRowCount(0)

        for row_idx, log in enumerate(logs):
            self.ui.log_table.insertRow(row_idx)

            # Форматирование даты
            log_date = log["log_date"].strftime("%d.%m.%Y %H:%M")

            # Формирование описания
            description = log["action"]
            if log["employee_name"]:
                description += f" ({log['employee_name']})"

            self.ui.log_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(log_date))
            self.ui.log_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(log["login"] or "Система"))
            self.ui.log_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(log["action"]))
            self.ui.log_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(description))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = LogWindow()
    window.show()
    sys.exit(app.exec())



