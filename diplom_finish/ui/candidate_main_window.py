from PyQt6 import QtWidgets, QtCore
import pymysql

class CandidateWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Кандидат: вакансии")
        self.resize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c2e9fb, stop:1 #a1c4fd);
            }
        """)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.vacancy_list = QtWidgets.QListWidget()
        self.vacancy_list.itemDoubleClicked.connect(self.open_resume_form)
        self.layout.addWidget(QtWidgets.QLabel("📋 Доступные вакансии (двойной клик для отклика):"))
        self.layout.addWidget(self.vacancy_list)

        self.my_apps_btn = QtWidgets.QPushButton("📄 Мои отклики")
        self.my_apps_btn.clicked.connect(self.show_applications)
        self.layout.addWidget(self.my_apps_btn)

        self.load_vacancies()

    def load_vacancies(self):
        self.vacancy_list.clear()
        conn = pymysql.connect(
            host="localhost", user="root", password="", database="diplom",
            port=3312, cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title, city FROM vacancies WHERE is_active = 1")
                for row in cursor.fetchall():
                    item = QtWidgets.QListWidgetItem(f"{row['title']} ({row['city']})")
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, row["id"])
                    self.vacancy_list.addItem(item)

    def open_resume_form(self, item):
        vac_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self.resume_dialog = ResumeFormDialog(self.user_id, vac_id)
        self.resume_dialog.exec()

    def show_applications(self):
        self.app_window = ApplicationsWindow(self.user_id)
        self.app_window.show()

class ResumeFormDialog(QtWidgets.QDialog):
    def __init__(self, user_id, vacancy_id):
        super().__init__()
        self.user_id = user_id
        self.vacancy_id = vacancy_id
        self.setWindowTitle("Отклик на вакансию")
        self.resize(400, 300)

        layout = QtWidgets.QFormLayout(self)

        self.name_input = QtWidgets.QLineEdit()
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setRange(16, 70)
        self.exp_input = QtWidgets.QSpinBox()
        self.exp_input.setRange(0, 50)
        self.resume_text = QtWidgets.QTextEdit()

        layout.addRow("ФИО:", self.name_input)
        layout.addRow("Возраст:", self.age_input)
        layout.addRow("Опыт (лет):", self.exp_input)
        layout.addRow("О себе:", self.resume_text)

        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.submit)
        btn_box.rejected.connect(self.reject)
        layout.addRow(btn_box)

    def submit(self):
        full_name = self.name_input.text().strip()
        age = self.age_input.value()
        experience = self.exp_input.value()
        resume = self.resume_text.toPlainText()

        if not full_name or not resume:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        conn = pymysql.connect(
            host="localhost", user="root", password="", database="diplom",
            port=3312, cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO applications (user_id, full_name, age, experience, vacancy_id, resume_text, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'new')
                """, (self.user_id, full_name, age, experience, self.vacancy_id, resume))
                conn.commit()

        QtWidgets.QMessageBox.information(self, "Успешно", "Отклик отправлен.")
        self.accept()

class ApplicationsWindow(QtWidgets.QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Мои отклики")
        self.resize(600, 400)
        self.setStyleSheet("background-color: #fefefe;")

        layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)
        self.load_applications()

    def load_applications(self):
        conn = pymysql.connect(
            host="localhost", user="root", password="", database="diplom",
            port=3312, cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT v.title, a.status, a.reviewed_at
                    FROM applications a
                    JOIN vacancies v ON a.vacancy_id = v.id
                    WHERE a.user_id = %s
                """, (self.user_id,))
                rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Вакансия", "Статус", "Дата ответа"])
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(row["title"]))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(row["status"]))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row["reviewed_at"] or "—")))
        self.table.resizeColumnsToContents()


