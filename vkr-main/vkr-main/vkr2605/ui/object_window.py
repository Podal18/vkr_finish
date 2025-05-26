from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ObjectWindow(object):
    def setupUi(self, ObjectWindow):
        ObjectWindow.setObjectName("ObjectWindow")
        ObjectWindow.resize(1000, 600)
        ObjectWindow.setWindowTitle("Объекты")
        ObjectWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        ObjectWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(ObjectWindow)
        ObjectWindow.setCentralWidget(self.centralwidget)

        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
                border-radius: 10px;
            }
        """)

        # ✕ Кнопка
        self.exit_button = QtWidgets.QPushButton(parent=ObjectWindow)
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
        self.exit_button.clicked.connect(ObjectWindow.close)

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.background)
        self.title_label.setGeometry(30, 20, 600, 40)
        self.title_label.setText("Список объектов")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Панель фильтров
        self.filter_frame = QtWidgets.QFrame(self.background)
        self.filter_frame.setGeometry(30, 70, 940, 60)
        self.filter_frame.setStyleSheet("background-color: rgba(255,255,255,0.9); border-radius: 10px;")

        self.search_input = QtWidgets.QLineEdit(self.filter_frame)
        self.search_input.setPlaceholderText("Поиск по названию или адресу")
        self.search_input.setGeometry(20, 10, 250, 40)

        self.search_button = QtWidgets.QPushButton("🔍 Найти", self.filter_frame)
        self.search_button.setGeometry(290, 10, 100, 40)

        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #a1c4fd;
                color: white;
                border-radius: 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #7da2f2;
            }
        """)

        # Таблица объектов
        self.object_table = QtWidgets.QTableWidget(self.background)
        self.object_table.setGeometry(30, 150, 940, 330)
        self.object_table.setColumnCount(4)
        self.object_table.setHorizontalHeaderLabels(["Название", "Адрес", "Прораб", "Сотрудники"])
        self.object_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.object_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.object_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #b0d4ff;
                padding: 4px;
                font-weight: bold;
                border: 1px solid white;
            }
        """)

        # Кнопки
        self.add_button = QtWidgets.QPushButton("➕ Добавить", self.background)
        self.add_button.setGeometry(100, 500, 160, 50)

        self.edit_button = QtWidgets.QPushButton("✏️ Изменить", self.background)
        self.edit_button.setGeometry(290, 500, 160, 50)

        self.delete_button = QtWidgets.QPushButton("🗑️ Удалить", self.background)
        self.delete_button.setGeometry(480, 500, 160, 50)

        self.view_staff_button = QtWidgets.QPushButton("👷‍♂️ Сотрудники объекта", self.background)
        self.view_staff_button.setGeometry(670, 500, 200, 50)

        for btn in [self.add_button, self.edit_button, self.delete_button, self.view_staff_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #a1c4fd;
                    color: white;
                    border-radius: 20px;
                    font-size: 15px;
                }
                QPushButton:hover {
                    background-color: #7da2f2;
                }
            """)


from PyQt6 import QtWidgets
from ui.add_edit_object import AddEditObjectWindow
from db.db import get_connection
from ui.object_profile import Ui_ObjectProfileWindow

def add_object(self):
    self.add_window = AddEditObjectWindow(mode="add")
    self.load_foremen(self.add_window.ui.foreman_combo)
    self.add_window.ui.save_button.clicked.disconnect()
    self.add_window.ui.save_button.clicked.connect(lambda: self.save_new_object(self.add_window))
    self.add_window.show()


class ObjectWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ObjectWindow()
        self.ui.setupUi(self)
        self.setup_connections()
        self.load_objects()
        self.setup_table()

    def setup_connections(self):
        """Подключение сигналов"""
        self.ui.search_button.clicked.connect(self.apply_filters)
        self.ui.search_input.textChanged.connect(self.apply_filters)
        self.ui.add_button.clicked.connect(self.add_object)
        self.ui.edit_button.clicked.connect(self.edit_object)
        self.ui.delete_button.clicked.connect(self.delete_object)
        self.ui.view_staff_button.clicked.connect(self.view_staff)

    def setup_table(self):
        """Настройка таблицы"""
        self.ui.object_table.setColumnWidth(0, 200)  # Название
        self.ui.object_table.setColumnWidth(1, 250)  # Адрес
        self.ui.object_table.setColumnWidth(2, 150)  # Прораб
        self.ui.object_table.setColumnWidth(3, 100)  # Сотрудники

    def load_objects(self):
        """Загрузка объектов из БД"""
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                    p.id,
                    p.name,
                    p.address,
                    u.login as foreman,
                    COUNT(a.id) as staff_count
                FROM projects p
                left JOIN assignments a ON p.id = a.project_id
                left JOIN employees e ON e.id = a.employee_id 
                left JOIN users u ON e.created_by = u.id
                GROUP BY p.id, p.name, p.address, u.login
                """)
                self.all_objects = cursor.fetchall()
                self.apply_filters()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()

    def apply_filters(self):
        """Применение фильтров"""
        search_text = self.ui.search_input.text().lower()
        filtered = [obj for obj in self.all_objects
                   if search_text in obj["name"].lower()
                   or search_text in obj["address"].lower()]
        self.update_table(filtered)

    def update_table(self, objects):
        """Обновление таблицы"""
        self.ui.object_table.setRowCount(0)
        for row_idx, obj in enumerate(objects):
            self.ui.object_table.insertRow(row_idx)
            self.ui.object_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(obj["name"]))
            self.ui.object_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(obj["address"]))
            self.ui.object_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(obj["foreman"] or "-"))
            self.ui.object_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(obj["staff_count"])))

    # Заглушки для обработчиков
    def add_object(self):
        self.add_window = AddEditObjectWindow(mode="add")
        self.load_foremen(self.add_window.ui.foreman_combo)
        self.add_window.ui.save_button.clicked.disconnect()
        self.add_window.ui.save_button.clicked.connect(lambda: self.save_new_object(self.add_window))
        self.add_window.show()

    def save_new_object(self, window):
        name = window.ui.name_input.text()
        address = window.ui.address_input.text()
        foreman_login = window.ui.foreman_combo.currentText()

        if not name or not foreman_login:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE login=%s", (foreman_login,))
                foreman_id = cursor.fetchone()["id"]

                cursor.execute("INSERT INTO projects (name, address) VALUES (%s, %s)", (name, address))
                project_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO assignments (employee_id, project_id)
                    SELECT e.id, %s FROM employees e WHERE e.created_by = %s
                """, (project_id, foreman_id))

            connection.commit()
            window.close()
            QtWidgets.QMessageBox.information(self, "Успешно", "Данные добавлены")
            self.load_objects()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось добавить объект: {str(e)}")
        finally:
            connection.close()

    def edit_object(self):
        selected = self.ui.object_table.currentRow()
        if selected == -1:
            QtWidgets.QMessageBox.warning(self, "Выбор", "Выберите объект для редактирования")
            return

        obj = self.all_objects[selected]
        self.edit_window = AddEditObjectWindow(mode="edit")
        self.load_foremen(self.edit_window.ui.foreman_combo)

        # Установим текущие значения
        self.edit_window.ui.name_input.setText(obj["name"])
        self.edit_window.ui.address_input.setText(obj["address"])
        idx = self.edit_window.ui.foreman_combo.findText(obj["foreman"])
        if idx >= 0:
            self.edit_window.ui.foreman_combo.setCurrentIndex(idx)

        self.edit_window.ui.save_button.clicked.disconnect()
        self.edit_window.ui.save_button.clicked.connect(lambda: self.update_object(obj["id"], self.edit_window))
        self.edit_window.show()

    def update_object(self, project_id, window):
        name = window.ui.name_input.text()
        address = window.ui.address_input.text()
        foreman_login = window.ui.foreman_combo.currentText()

        if not name or not foreman_login:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE login=%s", (foreman_login,))
                foreman_id = cursor.fetchone()["id"]

                cursor.execute("UPDATE projects SET name=%s, address=%s WHERE id=%s", (name, address, project_id))

                # Обновить создателя для всех сотрудников объекта (грубое приближение)
                cursor.execute("""
                    UPDATE employees e
                    JOIN assignments a ON e.id = a.employee_id
                    SET e.created_by = %s
                    WHERE a.project_id = %s
                """, (foreman_id, project_id))

            connection.commit()
            window.close()
            self.load_objects()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось обновить объект: {str(e)}")
        finally:
            connection.close()

    def delete_object(self):
        selected = self.ui.object_table.currentRow()
        if selected == -1:
            QtWidgets.QMessageBox.warning(self, "Выбор", "Выберите объект для удаления")
            return

        obj = self.all_objects[selected]
        confirm = QtWidgets.QMessageBox.question(
            self, "Подтвердите", f"Удалить объект '{obj['name']}'?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM assignments WHERE project_id=%s", (obj["id"],))
                    cursor.execute("DELETE FROM projects WHERE id=%s", (obj["id"],))
                connection.commit()
                self.load_objects()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {str(e)}")
            finally:
                connection.close()

    def view_staff(self):
        selected = self.ui.object_table.currentRow()
        if selected == -1:
            QtWidgets.QMessageBox.warning(self, "Выбор", "Выберите объект для просмотра")
            return

        obj = self.all_objects[selected]
        self.profile_window = QtWidgets.QMainWindow()
        self.profile_ui = Ui_ObjectProfileWindow()
        self.profile_ui.setupUi(self.profile_window)

        self.profile_ui.name_value.setText(obj["name"])
        self.profile_ui.address_value.setText(obj["address"])
        self.profile_ui.foreman_value.setText(obj["foreman"])

        self.load_staff_table(obj["id"])
        self.profile_ui.back_button.clicked.connect(self.profile_window.close)
        self.profile_window.show()

    def load_staff_table(self, project_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.full_name, 
                        p.name AS profession, 
                        CASE 
                            WHEN EXISTS (
                                SELECT 1 
                                FROM discipline d 
                                WHERE d.employee_id = e.id 
                                    AND d.violation_date > DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                            ) THEN 'Нет'  # Скобка закрыта
                            ELSE 'Да' 
                        END AS allowed
                    FROM assignments a
                    JOIN employees e ON e.id = a.employee_id
                    LEFT JOIN professions p ON p.id = e.profession_id
                    WHERE a.project_id = %s
                    GROUP BY e.id, e.full_name, p.name
                """, (project_id,))  # Параметр передается кортежем
                staff = cursor.fetchall()

            table = self.profile_ui.staff_table
            table.setRowCount(0)
            for row_idx, emp in enumerate(staff):
                table.insertRow(row_idx)
                table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(emp["full_name"]))
                table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(emp["profession"] or "-"))
                table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(emp["allowed"]))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить сотрудников: {str(e)}")
            print(e)
        finally:
            connection.close()

    def load_foremen(self, combo_box):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT login FROM users WHERE role_id = (
                        SELECT id FROM roles WHERE name = 'Foreman'
                    )
                """)
                foremen = cursor.fetchall()
                combo_box.clear()
                combo_box.addItems([f["login"] for f in foremen])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить прорабов: {str(e)}")
        finally:
            connection.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ObjectWindow()
    window.show()
    sys.exit(app.exec())
