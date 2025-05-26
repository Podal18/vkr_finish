from db.db import get_connection
from PyQt6 import QtWidgets
import datetime

def get_all_employees():
    """
    Возвращает список всех сотрудников с указанием названия профессии.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.full_name,
                    e.birth_date,
                    p.name AS profession,
                    e.status
                FROM employees e
                LEFT JOIN professions p ON e.profession_id = p.id
            """)
            return cursor.fetchall()
    finally:
        connection.close()


def get_all_professions():
    """
    Возвращает список всех профессий.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM professions")
            return cursor.fetchall()
    finally:
        connection.close()


def add_employee(full_name, birth_date, profession_id, created_by):
    """
    Добавляет нового сотрудника.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO employees (full_name, birth_date, profession_id, status, created_by)
                VALUES (%s, %s, %s, 'active', %s)
            """, (full_name, birth_date, profession_id, created_by))
    finally:
        connection.close()


def get_employee_by_id(emp_id):
    """
    Возвращает одного сотрудника по его ID.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, full_name, birth_date, profession_id
                FROM employees
                WHERE id = %s
            """, (emp_id,))
            return cursor.fetchone()
    finally:
        connection.close()


def update_employee(emp_id, full_name, birth_date, profession_id):
    """
    Обновляет данные сотрудника.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE employees
                SET full_name = %s,
                    birth_date = %s,
                    profession_id = %s
                WHERE id = %s
            """, (full_name, birth_date, profession_id, emp_id))
    finally:
        connection.close()


def fire_employee(emp_id):
    """
    Меняет статус сотрудника на 'inactive' (уволен).
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE employees
                SET status = 'inactive'
                WHERE id = %s
            """, (emp_id,))
    finally:
        connection.close()


def load_employee_profile(ui, employee_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Основная информация
            cursor.execute("""
                SELECT e.full_name, e.birth_date, p.name, e.status
                FROM employees e
                JOIN professions p ON e.profession_id = p.id
                WHERE e.id = %s
            """, (employee_id,))
            row = cursor.fetchone()

            if not row:
                QtWidgets.QMessageBox.warning(None, "Ошибка", "Сотрудник не найден.")
                return

            # Заполнение основной информации
            ui.name_value.setText(row["full_name"])
            ui.birth_value.setText(row["birth_date"].strftime("%d.%m.%Y"))
            ui.profession_value.setText(row["name"])
            ui.status_value.setText("Активен" if row["status"] == "active" else "Неактивен")

            # Документы
            documents = get_employee_documents(employee_id)
            ui.docs_table.setRowCount(0)
            for row_idx, doc in enumerate(documents):
                status = "Активен" if doc["expiry_date"] > datetime.date.today() else "Просрочен"
                ui.docs_table.insertRow(row_idx)
                ui.docs_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(doc["doc_type"]))
                ui.docs_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(doc["expiry_date"].strftime("%d.%m.%Y")))
                ui.docs_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(status))

            # Проекты
            projects = get_employee_projects(employee_id)
            ui.project_list.clear()
            for project in projects:
                text = f"{project['name']}\n{project['address']}\n"
                text += f"Назначен: {project['start_date'].strftime('%d.%m.%Y')}"
                if project['end_date']:
                    text += f" - {project['end_date'].strftime('%d.%m.%Y')}"
                item = QtWidgets.QListWidgetItem(text)
                ui.project_list.addItem(item)

            # Нарушения
            violations = get_employee_violations(employee_id)
            ui.violations_table.setRowCount(0)
            for row_idx, violation in enumerate(violations):
                ui.violations_table.insertRow(row_idx)
                ui.violations_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(
                    violation["violation_date"].strftime("%d.%m.%Y")))
                ui.violations_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(violation["description"]))
                ui.violations_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(violation["comments"]))

    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Ошибка", f"Ошибка загрузки данных: {str(e)}")
    finally:
        connection.close()

def get_employee_documents(employee_id):
    """Получает документы сотрудника"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT doc_type, doc_number, expiry_date 
                FROM documents 
                WHERE employee_id = %s
            """, (employee_id,))
            return cursor.fetchall()
    finally:
        connection.close()

def get_employee_projects(employee_id):
    """Получает проекты сотрудника с датами"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.name, 
                    p.address,
                    a.start_date,
                    a.end_date
                FROM assignments a
                JOIN projects p ON a.project_id = p.id
                WHERE a.employee_id = %s
            """, (employee_id,))
            return cursor.fetchall()
    finally:
        connection.close()

def get_employee_violations(employee_id):
    """Получает нарушения сотрудника"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    violation_type as description,
                    violation_date,
                    comments
                FROM discipline 
                WHERE employee_id = %s
            """, (employee_id,))
            return cursor.fetchall()
    finally:
        connection.close()

