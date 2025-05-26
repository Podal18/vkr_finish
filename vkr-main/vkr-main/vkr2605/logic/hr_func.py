from PyQt6 import QtWidgets
from db.db import get_connection

def get_dashboard_stats():
    """Возвращает статистику для дашборда"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Активные сотрудники
            cursor.execute("SELECT COUNT(*) AS count FROM employees WHERE status = 'active'")
            employee_count = cursor.fetchone()["count"]

            # Просроченные документы
            cursor.execute("SELECT COUNT(*) AS count FROM documents WHERE expiry_date < NOW()")
            expired_documents = cursor.fetchone()["count"]

            # Все проекты (статус не предусмотрен в схеме)
            cursor.execute("SELECT COUNT(*) AS count FROM projects")
            active_projects = cursor.fetchone()["count"]

            # Нарушения из таблицы discipline
            cursor.execute("SELECT COUNT(*) AS count FROM discipline")
            violations = cursor.fetchone()["count"]

            return {
                "employee_count": employee_count,
                "expired_documents": expired_documents,
                "active_projects": active_projects,
                "violations": violations
            }
    finally:
        connection.close()


def load_projects(ui):
    """Загружает список объектов (проектов)"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, address FROM projects")
            projects = cursor.fetchall()

            ui.object_table.setRowCount(0)
            for row_idx, project in enumerate(projects):
                ui.object_table.insertRow(row_idx)
                ui.object_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(project["name"]))
                ui.object_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(project["address"]))
    finally:
        connection.close()


def load_logs(ui):
    """Загружает журнал действий"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    l.log_date,
                    u.login,
                    l.action,
                    e.full_name as employee
                FROM logs l
                LEFT JOIN users u ON l.user_id = u.id
                LEFT JOIN employees e ON l.employee_id = e.id
                ORDER BY l.log_date DESC
            """)
            logs = cursor.fetchall()

            ui.log_table.setRowCount(0)
            for row_idx, log in enumerate(logs):
                ui.log_table.insertRow(row_idx)
                ui.log_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(log["log_date"].strftime("%d.%m.%Y %H:%M")))
                ui.log_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(log["login"] or "Система"))
                ui.log_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(log["action"]))
                ui.log_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(log["employee"] or "-"))
    finally:
        connection.close()


def load_users(ui):
    """Загружает пользователей системы"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.login,
                    r.name as role
                FROM users u
                LEFT JOIN roles r ON u.role_id = r.id
            """)
            users = cursor.fetchall()

            ui.user_table.setRowCount(0)
            for row_idx, user in enumerate(users):
                ui.user_table.insertRow(row_idx)
                ui.user_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(user["login"]))
                ui.user_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(user["role"]))
                ui.user_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(
                    user["last_login"].strftime("%d.%m.%Y %H:%M") if user["last_login"] else "-"
                ))
    finally:
        connection.close()