from PyQt6 import QtWidgets, QtCore, QtGui
import pymysql
import os
from datetime import datetime, timedelta
from ui.fire_dialog import FireDialog, Ui_ReportWindow  # Убедись, что файл fire_dialog.py находится в ui/

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
        self.sort_box.currentIndexChanged.connect(self.load_employees_from_db)
        self.layout.addWidget(self.sort_box)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.container = QtWidgets.QWidget()
        self.card_layout = QtWidgets.QVBoxLayout(self.container)
        self.card_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.container)
        self.layout.addWidget(self.scroll_area)

        self.back_btn = self.create_button("\ud83d\udd19 Назад", "#b0c4de")
        self.back_btn.clicked.connect(self.close)
        self.layout.addWidget(self.back_btn)

        self.load_employees_from_db()

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

    def load_employees_from_db(self):
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
                    emp["fire_chance"] = self.calculate_fire_chance(cursor, emp["id"])

                if self.sort_box.currentIndex() == 0:
                    employees.sort(key=lambda x: x["fire_chance"], reverse=True)
                else:
                    employees.sort(key=lambda x: x["fire_chance"])

                self.all_employees = employees
                self.render_employees()

    def render_employees(self):
        self.clear_layout(self.card_layout)
        for emp in self.all_employees:
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
        fire_btn.clicked.connect(lambda: self.fire_employee_dialog(emp))
        motivate_btn.clicked.connect(lambda: self.open_motivation(emp['id'], emp['full_name']))
        button_layout.addWidget(fire_btn)
        button_layout.addWidget(motivate_btn)
        h_layout.addLayout(button_layout)

        self.card_layout.addWidget(card)

    def fire_employee_dialog(self, emp):
        self.fire_dialog = FireDialog(self.current_user_id)
        self.fire_dialog.show()

    def commit_firing(self, employee_id, reason):
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
                               (employee_id, reason, self.current_user_id))
                conn.commit()

        QtWidgets.QMessageBox.information(self, "Успешно", "Сотрудник уволен.")
        self.load_employees_from_db()

    def calculate_fire_chance(self, cursor, emp_id):
        cursor.execute("SELECT status FROM attendance WHERE employee_id = %s", (emp_id,))
        attendance = cursor.fetchall()
        absents = sum(1 for a in attendance if a["status"] == "absent")
        lates = sum(1 for a in attendance if a["status"] == "late")
        score = absents * 10 + lates * 5

        ninety_days_ago = datetime.now() - timedelta(days=90)
        cursor.execute("""
            SELECT COUNT(*) AS cnt FROM motivation_actions
            WHERE employee_id = %s AND created_at >= %s
        """, (emp_id, ninety_days_ago))
        if cursor.fetchone()["cnt"] == 0:
            score += 15

        cursor.execute("""
            SELECT COUNT(*) AS cnt FROM motivation_actions
            WHERE employee_id = %s AND action_type = 'promotion'
        """, (emp_id,))
        if cursor.fetchone()["cnt"] == 0:
            score += 10

        return min(100, score)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def open_motivation(self, emp_id, emp_name):
        from ui.motivation_window import MotivationWindow
        self.motivation_win = MotivationWindow(emp_id, emp_name, self.current_user_id)
        self.motivation_win.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = EmployeeCardWindow(current_user_id=1)
    ui.show()
    sys.exit(app.exec())
