from PyQt6 import QtWidgets, QtCore, QtGui
import pymysql


class CandidateWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Кандидат: вакансии")
        self.resize(900, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
            }
        """)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Заголовок
        title_label = QtWidgets.QLabel("Доступные вакансии")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(title_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Область с карточками вакансий
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.container = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.container_layout.setSpacing(15)
        self.scroll_area.setWidget(self.container)

        self.layout.addWidget(self.scroll_area)

        # Кнопка обновления
        self.refresh_btn = QtWidgets.QPushButton("Обновить список")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_vacancies)
        self.layout.addWidget(self.refresh_btn)

        self.load_vacancies()

    def load_vacancies(self):
        # Очищаем предыдущие карточки
        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        conn = pymysql.connect(
            host="localhost", user="root", password="", database="diplom",
            port=3312, cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, city, salary, employment_type, required_experience FROM vacancies WHERE is_active = 1")
                vacancies = cursor.fetchall()

                if not vacancies:
                    empty_label = QtWidgets.QLabel("На данный момент нет доступных вакансий")
                    empty_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
                    empty_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.container_layout.addWidget(empty_label)
                    return

                for vac in vacancies:
                    self.add_vacancy_card(vac)

    def add_vacancy_card(self, vacancy):
        card = QtWidgets.QFrame()
        card.setFixedHeight(150)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                margin: 10px;
                padding: 15px;
            }
        """)
        h_layout = QtWidgets.QHBoxLayout(card)

        # Информация о вакансии
        info_layout = QtWidgets.QVBoxLayout()

        # Название
        title = QtWidgets.QLabel(vacancy["title"])
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        info_layout.addWidget(title)

        # Город
        city_label = QtWidgets.QLabel(f"Город: {vacancy['city'] if vacancy['city'] else 'Не указан'}")
        city_label.setStyleSheet("font-size: 14px; color: #34495e;")
        info_layout.addWidget(city_label)

        # Зарплата
        salary = vacancy['salary'] if vacancy['salary'] is not None else "Не указана"
        salary_label = QtWidgets.QLabel(f"Зарплата: {salary}")
        salary_label.setStyleSheet("font-size: 14px; color: #34495e;")
        info_layout.addWidget(salary_label)

        # Тип занятости
        employment_type = vacancy['employment_type'] if vacancy['employment_type'] else "Не указан"
        type_label = QtWidgets.QLabel(f"Тип: {employment_type}")
        type_label.setStyleSheet("font-size: 14px; color: #34495e;")
        info_layout.addWidget(type_label)

        # Опыт
        experience = vacancy['required_experience'] if vacancy['required_experience'] is not None else "Не указан"
        exp_label = QtWidgets.QLabel(f"Опыт: {experience} лет")
        exp_label.setStyleSheet("font-size: 14px; color: #34495e;")
        info_layout.addWidget(exp_label)

        h_layout.addLayout(info_layout, 70)  # 70% ширины

        # Кнопка отклика
        button_layout = QtWidgets.QVBoxLayout()
        apply_btn = QtWidgets.QPushButton("Откликнуться")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        apply_btn.clicked.connect(lambda _, v=vacancy["id"]: self.open_resume_form(v))
        button_layout.addWidget(apply_btn)

        h_layout.addLayout(button_layout, 30)  # 30% ширины

        self.container_layout.addWidget(card)

    def open_resume_form(self, vacancy_id):
        self.resume_dialog = ResumeFormDialog(self.user_id, vacancy_id)
        self.resume_dialog.exec()


class ResumeFormDialog(QtWidgets.QDialog):
    def __init__(self, user_id, vacancy_id):
        super().__init__()
        self.user_id = user_id
        self.vacancy_id = vacancy_id
        self.setWindowTitle("Отклик на вакансию")
        self.resize(500, 400)
        self.setStyleSheet("background-color: #f8f9fa;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QtWidgets.QLabel("Заполните данные для отклика")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9;")
        layout.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Форма
        form_layout = QtWidgets.QFormLayout()
        form_layout.setVerticalSpacing(10)

        self.name_input = QtWidgets.QLineEdit()
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setRange(16, 70)
        self.exp_input = QtWidgets.QSpinBox()
        self.exp_input.setRange(0, 50)
        self.resume_text = QtWidgets.QTextEdit()

        form_layout.addRow("ФИО:", self.name_input)
        form_layout.addRow("Возраст:", self.age_input)
        form_layout.addRow("Опыт (лет):", self.exp_input)
        form_layout.addRow("Резюме:", self.resume_text)

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QtWidgets.QHBoxLayout()

        submit_btn = QtWidgets.QPushButton("Отправить")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        submit_btn.clicked.connect(self.submit)

        cancel_btn = QtWidgets.QPushButton("Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(submit_btn)
        layout.addLayout(btn_layout)

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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = CandidateWindow(user_id=1)
    ui.show()
    sys.exit(app.exec())
