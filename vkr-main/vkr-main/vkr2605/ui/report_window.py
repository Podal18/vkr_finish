from PyQt6 import QtCore, QtGui, QtWidgets
from db.db import get_connection
import csv
from PyQt6 import QtWidgets
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtCore import Qt, QMarginsF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Ui_ReportWindow(object):
    def setupUi(self, ReportWindow):
        ReportWindow.setObjectName("ReportWindow")
        ReportWindow.resize(1000, 600)
        ReportWindow.setWindowTitle("Отчёты")
        ReportWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        ReportWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(ReportWindow)
        ReportWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fbc2eb, stop:1 #a6c1ee);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=ReportWindow)
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
        self.exit_button.clicked.connect(ReportWindow.close)

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
        self.back_button.clicked.connect(ReportWindow.close)

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Аналитика и отчёты")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Панель фильтров
        self.filter_frame = QtWidgets.QFrame(self.background)
        self.filter_frame.setGeometry(30, 70, 940, 60)
        self.filter_frame.setStyleSheet("background-color: rgba(255,255,255,0.9); border-radius: 10px;")

        self.report_type_combo = QtWidgets.QComboBox(self.filter_frame)
        self.report_type_combo.setGeometry(20, 10, 200, 40)
        self.report_type_combo.addItems([
            "Выберите тип отчёта", "По профессиям", "По объектам", "Истекающие документы", "Нарушения"
        ])

        self.period_combo = QtWidgets.QComboBox(self.filter_frame)
        self.period_combo.setGeometry(240, 10, 200, 40)
        self.period_combo.addItems(["Все даты", "За месяц", "За квартал", "За год"])

        self.generate_button = QtWidgets.QPushButton("📊 Построить", self.filter_frame)
        self.generate_button.setGeometry(460, 10, 140, 40)

        self.export_button = QtWidgets.QPushButton("⬇️ Экспорт", self.filter_frame)
        self.export_button.setGeometry(620, 10, 120, 40)

        for btn in [self.generate_button, self.export_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #a6c1ee;
                    color: white;
                    border-radius: 20px;
                    font-size: 15px;
                }
                QPushButton:hover {
                    background-color: #8aa8e3;
                }
            """)

        # Область отчёта (заглушка)
        self.report_area = QtWidgets.QFrame(self.background)
        self.report_area.setGeometry(30, 150, 940, 370)
        self.report_area.setStyleSheet("background-color: white; border-radius: 10px;")
        self.report_placeholder = QtWidgets.QLabel("Здесь будет отображаться отчёт...", self.report_area)
        self.report_placeholder.setGeometry(0, 0, 940, 370)
        self.report_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.report_placeholder.setStyleSheet("font-size: 16px; color: #888;")


class ReportWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ReportWindow()
        self.ui.setupUi(self)
        self.setup_connections()

    def setup_connections(self):
        """Подключение сигналов"""
        self.ui.generate_button.clicked.connect(self.generate_report)
        self.ui.export_button.clicked.connect(self.export_report)
        self.ui.back_button.clicked.connect(self.close)

    def generate_report(self):
        """Формирование отчёта"""
        report_type = self.ui.report_type_combo.currentText()
        period = self.ui.period_combo.currentText()

        try:
            if report_type == "По профессиям":
                data = self.load_professions_report()
            elif report_type == "По объектам":
                data = self.load_projects_report()
            elif report_type == "Истекающие документы":
                data = self.load_expiring_documents(period)
            elif report_type == "Нарушения":
                data = self.load_violations_report(period)
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите тип отчёта")
                return

            self.display_report(data, report_type)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка формирования отчёта: {str(e)}")

    # Методы загрузки данных из БД остаются без изменений
    def load_professions_report(self):
        """Отчёт по профессиям"""
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.name AS profession, COUNT(e.id) AS count 
                    FROM professions p
                    LEFT JOIN employees e ON p.id = e.profession_id
                    GROUP BY p.name
                """)
                result = cursor.fetchall()
                print("Данные из БД (профессии):", result)  # Логирование
                return result
        finally:
            connection.close()

    def load_projects_report(self):
        """Отчёт по объектам"""
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT pr.name AS project, COUNT(a.employee_id) AS employees 
                    FROM projects pr
                    LEFT JOIN assignments a ON pr.id = a.project_id
                    GROUP BY pr.name
                """)
                return cursor.fetchall()
        finally:
            connection.close()

    def load_expiring_documents(self, period):
        """Документы с истекающим сроком"""
        connection = get_connection()
        try:
            query = """
                SELECT e.full_name, d.doc_type, d.expiry_date 
                FROM documents d
                JOIN employees e ON d.employee_id = e.id
                WHERE d.expiry_date BETWEEN CURDATE() AND """

            if period == "За месяц":
                query += "DATE_ADD(CURDATE(), INTERVAL 1 MONTH)"
            elif period == "За квартал":
                query += "DATE_ADD(CURDATE(), INTERVAL 3 MONTH)"
            elif period == "За год":
                query += "DATE_ADD(CURDATE(), INTERVAL 1 YEAR)"
            else:  # Все даты
                query += "'9999-12-31'"

            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()

    def load_violations_report(self, period):
        """Отчёт по нарушениям"""
        connection = get_connection()
        try:
            period_filter = ""
            if period == "За месяц":
                period_filter = "AND violation_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
            elif period == "За квартал":
                period_filter = "AND violation_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)"
            elif period == "За год":
                period_filter = "AND violation_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)"

            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT e.full_name, d.violation_type, d.violation_date, d.comments 
                    FROM discipline d
                    JOIN employees e ON d.employee_id = e.id
                    WHERE 1=1 {period_filter}
                """)
                return cursor.fetchall()
        finally:
            connection.close()

    def display_report(self, data, report_type):
        """Отображение данных в таблице и графике"""
        try:
            # Очистка предыдущих виджетов
            for child in self.ui.report_area.children():
                if isinstance(child, QtWidgets.QWidget):
                    child.deleteLater()

            if not data:  # Добавляем проверку на пустые данные
                raise ValueError("Нет данных для отображения")

            # Создаём контейнер
            container = QtWidgets.QWidget(self.ui.report_area)
            container.setGeometry(10, 10, 920, 350)
            layout = QtWidgets.QVBoxLayout(container)

            # Таблица
            table = QtWidgets.QTableWidget()
            self._setup_table(table, data, report_type)
            layout.addWidget(table)

            # График
            figure = Figure(figsize=(8, 4))
            canvas = FigureCanvas(figure)
            layout.addWidget(canvas)
            self._generate_chart(figure, data, report_type)

            container.show()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка отображения: {str(e)}")

    def _setup_table(self, table, data, report_type):
        """Настройка таблицы с правильными ключами"""
        try:
            table.setStyleSheet("font-size: 14px;")

            # Определение соответствий заголовков и ключей
            column_map = {
                "По профессиям": [
                    ("Профессия", "profession"),
                    ("Количество сотрудников", "count")
                ],
                "По объектам": [
                    ("Объект", "project"),
                    ("Количество сотрудников", "employees")
                ],
                "Истекающие документы": [
                    ("Сотрудник", "full_name"),
                    ("Тип документа", "doc_type"),
                    ("Срок действия", "expiry_date")
                ],
                "Нарушения": [
                    ("Сотрудник", "full_name"),
                    ("Тип нарушения", "violation_type"),
                    ("Дата", "violation_date"),
                    ("Комментарий", "comments")
                ]
            }

            # Получаем маппинг для текущего типа отчёта
            columns = column_map.get(report_type, [])
            headers = [col[0] for col in columns]
            keys = [col[1] for col in columns]

            # Настройка таблицы
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(data))

            # Заполнение данных
            for row_idx, row in enumerate(data):
                for col_idx, key in enumerate(keys):
                    value = str(row.get(key, 'ERROR'))
                    table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(value))

            table.resizeColumnsToContents()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка создания таблицы: {str(e)}")
            print("Ошибка данных:", data)  # Логирование сырых данных

    def _generate_chart(self, figure, data, report_type):
        """Генерация графиков"""
        figure.clear()
        ax = figure.add_subplot(111)

        if report_type == "По профессиям":
            professions = [row['profession'] for row in data]
            counts = [row['count'] for row in data]
            ax.bar(professions, counts)
            ax.set_title('Распределение по профессиям')
            ax.set_ylabel('Количество сотрудников')

        elif report_type == "По объектам":
            projects = [row['project'] for row in data]
            counts = [row['employees'] for row in data]
            ax.bar(projects, counts, color='orange')
            ax.set_title('Сотрудники на объектах')
            ax.set_ylabel('Количество')

        elif report_type == "Истекающие документы":
            dates = [row['expiry_date'].strftime('%d.%m.%Y') for row in data]
            ax.plot(dates, marker='o')
            ax.set_title('Сроки действия документов')
            ax.tick_params(axis='x', rotation=45)

        elif report_type == "Нарушения":
            violations = {}
            for row in data:
                violations[row['violation_type']] = violations.get(row['violation_type'], 0) + 1

            ax.pie(
                violations.values(),
                labels=violations.keys(),
                autopct='%1.1f%%',
                startangle=90
            )
            ax.set_title('Распределение нарушений')

        figure.tight_layout()

    def export_report(self):
        """Экспорт с улучшенной обработкой ошибок"""
        try:
            # Поиск контейнера
            container = self.ui.report_area.findChild(QtWidgets.QWidget)
            if not container:
                raise ValueError("Отчёт не сгенерирован")

            # Поиск таблицы
            table = container.findChild(QtWidgets.QTableWidget)
            if not table:
                raise ValueError("Таблица не найдена")

            if table.rowCount() == 0:
                raise ValueError("Таблица пуста")

            # Диалог сохранения
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Экспорт", "", "CSV Files (*.csv)")

            if not filename:
                return

            # Экспорт
            with open(filename, 'w', encoding='utf-8-sig', newline='') as f:  # Исправлена кодировка
                writer = csv.writer(f, delimiter=';')

                # Заголовки
                headers = [table.horizontalHeaderItem(i).text()
                           for i in range(table.columnCount())]
                writer.writerow(headers)

                # Данные
                print(f"Количество строк: {table.rowCount()}")
                for row in range(table.rowCount()):
                    row_data = []
                    for col in range(table.columnCount()):
                        item = table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
                    print(f"Строка {row}: {row_data}")


            QtWidgets.QMessageBox.information(self, "Успех", "Экспорт завершён")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка экспорта", f"{str(e)}")

    def _export_to_csv(self, table, filename):
        """Экспорт в CSV"""
        with open(filename, 'w', encoding='utf-8-sig', newline='') as file:  # Исправлено
            writer = csv.writer(file, delimiter=';')

            # Заголовки
            headers = [table.horizontalHeaderItem(i).text()
                       for i in range(table.columnCount())]
            writer.writerow(headers)

            # Данные
            for row in range(table.rowCount()):
                row_data = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

# Пример запуска
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ReportWindow()
    window.show()
    sys.exit(app.exec())
