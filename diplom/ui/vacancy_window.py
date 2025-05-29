from PyQt6 import QtWidgets, QtCore, QtGui
import pymysql

class VacancyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вакансии")
        self.resize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9a9e, stop:1 #fad0c4);
            }
        """)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container = QtWidgets.QWidget()
        self.vacancy_layout = QtWidgets.QVBoxLayout(self.container)
        self.vacancy_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.container)

        self.layout.addWidget(self.scroll_area)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.add_btn = self.create_button("➕ Добавить вакансию", "#fcb1b6")
        self.delete_btn = self.create_button("🗑 Удалить вакансию", "#f4978e")
        self.back_btn = self.create_button("🔙 Назад", "#b0c4de")
        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addWidget(self.back_btn)
        self.layout.addLayout(self.button_layout)

        self.load_vacancies()

    def create_button(self, text, color):
        btn = QtWidgets.QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: #ff6f61;
            }}
        """)
        return btn

    def load_vacancies(self):
        self.clear_layout(self.vacancy_layout)
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="diplom",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            port=3312
        )

        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title FROM vacancies WHERE is_active = 1")
                vacancies = cursor.fetchall()
                for v in vacancies:
                    cursor.execute("SELECT COUNT(*) AS count FROM applications WHERE vacancy_id = %s", (v['id'],))
                    count = cursor.fetchone()["count"]
                    self.add_vacancy_card(v["id"], v["title"], count)

    def add_vacancy_card(self, vacancy_id, title, application_count):
        card = QtWidgets.QFrame()
        card.setFixedHeight(80)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                margin: 5px;
            }
        """)
        h_layout = QtWidgets.QHBoxLayout(card)

        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        h_layout.addWidget(title_label)

        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        h_layout.addItem(spacer)

        badge = QtWidgets.QLabel(str(application_count))
        badge.setFixedSize(30, 30)
        badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet("""
            background-color: #ff4d4f;
            color: white;
            border-radius: 15px;
            font-weight: bold;
        """)
        h_layout.addWidget(badge)

        card.mousePressEvent = lambda event: self.open_candidates(vacancy_id)
        self.vacancy_layout.addWidget(card)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def open_candidates(self, vacancy_id):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = VacancyWindow()
    ui.show()
    sys.exit(app.exec())