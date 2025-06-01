from PyQt6 import QtWidgets, QtCore, QtGui
import pymysql
import random
import os

class EmployeeCardWindow(QtWidgets.QWidget):
    def __init__(self, current_user_id):
        super().__init__()
        self.current_user_id = current_user_id
        self.setWindowTitle("Сотрудники")
        self.resize(900, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9a9e, stop:1 #fad0c4);
            }
        """)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.sort_box = QtWidgets.QComboBox()
        self.sort_box.addItems(["Сортировать по шансу (по убыванию)", "Сортировать по шансу (по возрастанию)"])
        self.sort_box.currentIndexChanged.connect(self.load_employees)
        self.layout.addWidget(self.sort_box)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.container = QtWidgets.QWidget()
        self.card_layout = QtWidgets.QVBoxLayout(self.container)
        self.card_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.container)
        self.layout.addWidget(self.scroll_area)

        self.back_btn = self.create_button("🔙 Назад", "#b0c4de")
        self.back_btn.clicked.connect(self.close)
        self.layout.addWidget(self.back_btn)

        self.load_employees()

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

    def load_employees(self):
        self.clear_layout(self.card_layout)

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
                cursor.execute("SELECT * FROM employees WHERE is_active = 1")
                employees = cursor.fetchall()

                for emp in employees:
                    emp["fire_chance"] = random.randint(0, 100)

                if self.sort_box.currentIndex() == 0:
                    employees.sort(key=lambda x: x["fire_chance"], reverse=True)
                else:
                    employees.sort(key=lambda x: x["fire_chance"])

                for emp in employees:
                    self.add_employee_card(emp)

    def add_employee_card(self, emp):
        card = QtWidgets.QFrame()
        card.setFixedHeight(150)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                margin: 10px;
            }
        """)
        h_layout = QtWidgets.QHBoxLayout(card)

        photo_label = QtWidgets.QLabel()
        photo_label.setFixedSize(100, 100)
        if emp["photo_path"] and os.path.exists(emp["photo_path"]):
            pixmap = QtGui.QPixmap(emp["photo_path"]).scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            photo_label.setPixmap(pixmap)
        else:
            photo_label.setText("Нет фото")
            photo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(photo_label)

        info_layout = QtWidgets.QVBoxLayout()
        info_layout.addWidget(QtWidgets.QLabel(f"<b>{emp['full_name']}</b>"))
        info_layout.addWidget(QtWidgets.QLabel(f"Должность: {emp['profession']}"))
        info_layout.addWidget(QtWidgets.QLabel(f"Шанс на увольнение: {emp['fire_chance']}%"))
        h_layout.addLayout(info_layout)

        button_layout = QtWidgets.QVBoxLayout()
        fire_btn = self.create_button("Уволить", "#ff4d4f")
        motivate_btn = self.create_button("Мотивировать", "#4CAF50")
        fire_btn.clicked.connect(lambda: self.fire_employee(emp['id']))
        motivate_btn.clicked.connect(lambda: self.motivate_employee(emp['id']))
        button_layout.addWidget(fire_btn)
        button_layout.addWidget(motivate_btn)
        h_layout.addLayout(button_layout)

        self.card_layout.addWidget(card)

    def fire_employee(self, employee_id):
        # Пример простого удаления
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="diplom",
            port=3312
        )
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE employees SET is_active = 0 WHERE id = %s", (employee_id,))
                cursor.execute("INSERT INTO firings (employee_id, reason, fired_by) VALUES (%s, %s, %s)",
                               (employee_id, "Уволен вручную", self.current_user_id))
                conn.commit()
        self.load_employees()

    def motivate_employee(self, employee_id):
        QtWidgets.QMessageBox.information(self, "Мотивация", f"Вы успешно замотивировали сотрудника ID {employee_id}.")

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = EmployeeCardWindow(current_user_id=1)
    ui.show()
    sys.exit(app.exec())
