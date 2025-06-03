from PyQt6 import QtWidgets, QtCore, QtGui
import pymysql
import os

class EmployeeAccountWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Личный кабинет сотрудника")
        self.resize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d4fc79, stop:1 #96e6a1);
                font-size: 14px;
            }
        """)

        self.central = QtWidgets.QWidget()
        self.setCentralWidget(self.central)
        self.layout = QtWidgets.QVBoxLayout(self.central)

        self.header = QtWidgets.QLabel("👤 Личный кабинет")
        self.header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("font-size: 22px; font-weight: bold; color: #2d3436;")
        self.layout.addWidget(self.header)

        self.profile_frame = QtWidgets.QFrame()
        self.profile_frame.setStyleSheet("background-color: white; border-radius: 15px;")
        self.profile_layout = QtWidgets.QHBoxLayout(self.profile_frame)
        self.layout.addWidget(self.profile_frame)

        self.photo_label = QtWidgets.QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setStyleSheet("border: 1px solid #ccc; border-radius: 10px;")
        self.profile_layout.addWidget(self.photo_label)

        self.upload_photo_btn = QtWidgets.QPushButton("📤 Загрузить фото")
        self.upload_photo_btn.setFixedWidth(150)
        self.upload_photo_btn.clicked.connect(self.upload_photo)
        self.profile_layout.addWidget(self.upload_photo_btn)

        self.info_layout = QtWidgets.QFormLayout()
        self.name_label = QtWidgets.QLabel()
        self.position_label = QtWidgets.QLabel()
        self.passport_label = QtWidgets.QLabel()
        self.passport_btn = QtWidgets.QPushButton("📎 Прикрепить скан паспорта")
        self.passport_btn.clicked.connect(self.upload_passport)
        self.view_passport_btn = QtWidgets.QPushButton("👁 Посмотреть скан паспорта")
        self.view_passport_btn.clicked.connect(self.view_passport)
        self.info_layout.addRow("", self.view_passport_btn)

        self.info_layout.addRow("ФИО:", self.name_label)
        self.info_layout.addRow("Должность:", self.position_label)
        self.info_layout.addRow("Паспорт:", self.passport_label)
        self.info_layout.addRow("", self.passport_btn)
        self.profile_layout.addLayout(self.info_layout)

        self.history_btn = QtWidgets.QPushButton("📜 История проходов")
        self.quit_btn = QtWidgets.QPushButton("🚪 Уволиться")
        for btn in (self.history_btn, self.quit_btn):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #74b9ff;
                    border-radius: 20px;
                    color: white;
                    padding: 10px 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #0984e3;
                }
            """)
        self.quit_btn.setStyleSheet(self.quit_btn.styleSheet() + """
            QPushButton {
                background-color: #d63031;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.history_btn.clicked.connect(self.show_attendance)
        self.quit_btn.clicked.connect(self.quit_employee)
        self.layout.addWidget(self.history_btn)
        self.layout.addWidget(self.quit_btn)

        self.load_data()

    def upload_photo(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать фото", "", "Изображения (*.jpg *.png *.jpeg)")
        if path:
            conn = pymysql.connect(host="localhost", user="root", password="", database="diplom", port=3312)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE employees SET photo_path = %s WHERE id = %s", (path, self.emp_id))
                    conn.commit()
            QtWidgets.QMessageBox.information(self, "Успешно", "Фото обновлено.")
            self.load_data()

    def load_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="diplom", port=3312,
                               cursorclass=pymysql.cursors.DictCursor)
        with conn:
            with conn.cursor() as cursor:
                # Получаем данные сотрудника по user_id
                cursor.execute("SELECT login FROM users WHERE id = %s", (self.user_id,))
                login = cursor.fetchone()["login"]

                cursor.execute("SELECT * FROM employees WHERE full_name = %s", (login,))
                emp = cursor.fetchone()

                if not emp:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Информация не найдена.")
                    return

                self.emp_id = emp["id"]
                self.name_label.setText(emp["full_name"])
                self.position_label.setText(emp["profession"])
                self.passport_label.setText(os.path.basename(emp["passport_scan_path"]) if emp["passport_scan_path"] else "Не загружен")

                if emp["photo_path"] and os.path.exists(emp["photo_path"]):
                    pixmap = QtGui.QPixmap(emp["photo_path"]).scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                    self.photo_label.setPixmap(pixmap)
                else:
                    self.photo_label.setText("Нет фото")
                    self.photo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def view_passport(self):
        try:
            conn = pymysql.connect(host="localhost", user="root", password="", database="diplom", port=3312, cursorclass=pymysql.cursors.DictCursor)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT passport_scan_path FROM employees WHERE id = %s", (self.emp_id,))
                    result = cursor.fetchone()
                    path = result["passport_scan_path"] if result else None

            if not path:
                QtWidgets.QMessageBox.warning(self, "Нет файла", "Скан паспорта не прикреплён.")
                return

            if not os.path.exists(path):
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Файл не найден:\n{path}")
                return

            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")
            print(e)

    def upload_passport(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать скан паспорта", "", "PDF или JPG (*.pdf *.jpg *.png)")
        if path:
            conn = pymysql.connect(host="localhost", user="root", password="", database="diplom", port=3312)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE employees SET passport_scan_path = %s WHERE id = %s", (path, self.emp_id))
                    conn.commit()
            QtWidgets.QMessageBox.information(self, "Успешно", "Файл загружен.")
            self.load_data()

    def show_attendance(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="diplom", port=3312,
                               cursorclass=pymysql.cursors.DictCursor)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT date, status FROM attendance
                    WHERE employee_id = %s ORDER BY date DESC
                """, (self.emp_id,))
                rows = cursor.fetchall()

        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("История проходов")
        dlg.resize(500, 400)
        layout = QtWidgets.QVBoxLayout(dlg)
        table = QtWidgets.QTableWidget(len(rows), 2)
        table.setHorizontalHeaderLabels(["Дата", "Статус"])
        for i, row in enumerate(rows):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row["date"])))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(row["status"]))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        btn = QtWidgets.QPushButton("Закрыть")
        btn.clicked.connect(dlg.close)
        layout.addWidget(btn)
        dlg.exec()

    def quit_employee(self):
        confirm = QtWidgets.QMessageBox.question(
            self, "Уволиться", "Вы уверены, что хотите уволиться?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = pymysql.connect(host="localhost", user="root", password="", database="diplom", port=3312)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE employees SET is_active = 0 WHERE id = %s", (self.emp_id,))
                    cursor.execute("UPDATE users SET role = 5 WHERE id = %s", (self.user_id,))
                    conn.commit()
            QtWidgets.QMessageBox.information(self, "Успешно", "Вы уволены.")
            self.close()
