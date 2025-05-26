from PyQt6 import QtCore, QtGui, QtWidgets
from db.db import get_connection
from datetime import datetime



class Ui_DocumentWindow(object):
    def setupUi(self, DocumentWindow):
        DocumentWindow.setObjectName("DocumentWindow")
        DocumentWindow.resize(1000, 600)
        DocumentWindow.setWindowTitle("Документы")
        DocumentWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        DocumentWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(DocumentWindow)
        DocumentWindow.setCentralWidget(self.centralwidget)

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
        self.exit_button = QtWidgets.QPushButton(parent=DocumentWindow)
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
        self.exit_button.clicked.connect(DocumentWindow.close)

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

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Контроль документов сотрудников")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Панель фильтрации
        self.filter_frame = QtWidgets.QFrame(self.background)
        self.filter_frame.setGeometry(30, 70, 940, 60)
        self.filter_frame.setStyleSheet("background-color: rgba(255,255,255,0.9); border-radius: 10px;")

        self.search_input = QtWidgets.QLineEdit(self.filter_frame)
        self.search_input.setPlaceholderText("Поиск по ФИО")
        self.search_input.setGeometry(20, 10, 250, 40)

        self.doc_type_combo = QtWidgets.QComboBox(self.filter_frame)
        self.doc_type_combo.setGeometry(290, 10, 180, 40)
        self.doc_type_combo.addItems(["Все типы", "Медсправка", "Допуск", "Удостоверение"])

        self.date_filter_combo = QtWidgets.QComboBox(self.filter_frame)
        self.date_filter_combo.setGeometry(490, 10, 180, 40)
        self.date_filter_combo.addItems(["Все", "Истекает через 30 дней", "Просроченные"])

        self.search_button = QtWidgets.QPushButton("🔍 Найти", self.filter_frame)
        self.search_button.setGeometry(690, 10, 100, 40)

        for widget in [self.search_button]:
            widget.setStyleSheet("""
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

        # Таблица документов
        self.doc_table = QtWidgets.QTableWidget(self.background)
        self.doc_table.setGeometry(30, 150, 940, 360)
        self.doc_table.setColumnCount(5)
        self.doc_table.setHorizontalHeaderLabels(["ФИО", "Тип документа", "Номер", "Срок действия", "Статус"])
        self.doc_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.doc_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.doc_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #b9fbc0;
                padding: 4px;
                font-weight: bold;
                border: 1px solid white;
            }
        """)

class DocumentWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DocumentWindow()
        self.ui.setupUi(self)
        self.setup_connections()
        self.load_documents()
        self.setup_table()

    def setup_connections(self):
        """Подключение сигналов"""
        self.ui.search_button.clicked.connect(self.apply_filters)
        self.ui.doc_type_combo.currentIndexChanged.connect(self.apply_filters)
        self.ui.date_filter_combo.currentIndexChanged.connect(self.apply_filters)
        self.ui.search_input.textChanged.connect(self.apply_filters)

    def setup_table(self):
        """Настройка таблицы"""
        self.ui.doc_table.setColumnWidth(0, 200)  # ФИО
        self.ui.doc_table.setColumnWidth(1, 150)  # Тип
        self.ui.doc_table.setColumnWidth(2, 120)  # Номер
        self.ui.doc_table.setColumnWidth(3, 120)  # Срок
        self.ui.doc_table.setColumnWidth(4, 100)  # Статус

    def load_documents(self):
        """Базовая загрузка документов"""
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.full_name,
                        d.doc_type,
                        d.doc_number,
                        d.expiry_date
                    FROM documents d
                    JOIN employees e ON d.employee_id = e.id
                """)
                self.all_documents = cursor.fetchall()
                self.apply_filters()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()

    def apply_filters(self):
        """Применение фильтров"""
        search_text = self.ui.search_input.text().lower()
        doc_type = self.ui.doc_type_combo.currentText()
        date_filter = self.ui.date_filter_combo.currentText()

        filtered = []
        today = datetime.today().date()

        for doc in self.all_documents:
            # Фильтр по тексту
            if search_text not in doc["full_name"].lower():
                continue

            # Фильтр по типу документа
            if doc_type != "Все типы" and doc_type not in doc["doc_type"]:
                continue

            # Фильтр по сроку
            expiry_date = doc["expiry_date"]
            status = "Активен" if expiry_date > today else "Просрочен"

            if date_filter == "Истекает через 30 дней":
                delta = (expiry_date - today).days
                if not (0 < delta <= 30):
                    continue
            elif date_filter == "Просроченные" and status != "Просрочен":
                continue

            filtered.append(doc)

        self.update_table(filtered)

    def update_table(self, documents):
        """Обновление таблицы"""
        self.ui.doc_table.setRowCount(0)

        for row_idx, doc in enumerate(documents):
            self.ui.doc_table.insertRow(row_idx)

            # Расчет статуса
            expiry_date = doc["expiry_date"]
            status = "Активен" if expiry_date > datetime.today().date() else "Просрочен"

            # Заполнение данных
            self.ui.doc_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(doc["full_name"]))
            self.ui.doc_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(doc["doc_type"]))
            self.ui.doc_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(doc["doc_number"]))
            self.ui.doc_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(expiry_date.strftime("%d.%m.%Y")))

            # Окрашивание статуса
            status_item = QtWidgets.QTableWidgetItem(status)
            status_item.setForeground(QtGui.QColor("green") if status == "Активен" else QtGui.QColor("red"))
            self.ui.doc_table.setItem(row_idx, 4, status_item)


# Пример использования
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = DocumentWindow()
    window.show()
    sys.exit(app.exec())





# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_DocumentWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
