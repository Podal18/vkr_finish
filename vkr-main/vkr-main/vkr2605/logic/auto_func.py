from db.db import get_connection
import hashlib


def authenticate_user(login, password):
    """
    Аутентификация пользователя по логину и хэш-паролю.
    Возвращает словарь с user_id, full_name, role, если успешно, иначе None.
    """
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.id AS user_id,
                    e.status,
                    r.name AS role,
                    e.full_name
                FROM users u
                LEFT JOIN roles r ON u.role_id = r.id
                LEFT JOIN employees e ON u.id = e.created_by
                WHERE u.login = %s AND u.password_hash = %s
            """, (login, password_hash))
            user = cursor.fetchone()

            if user and user["status"] == "active":
                return {
                    "id": user["user_id"],
                    "role": user["role"],
                    "full_name": user["full_name"]
                }
            return None
    finally:
        connection.close()


def reset_password(login, new_password):
    """
    Сброс пароля по логину.
    Возвращает (True, сообщение) при успехе, иначе (False, сообщение).
    """
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE login = %s", (login,))
            if not cursor.fetchone():
                return False, "Пользователь не найден"

            cursor.execute("""
                UPDATE users 
                SET password_hash = %s 
                WHERE login = %s
            """, (password_hash, login))
            connection.commit()
            return True, "Пароль успешно изменён"
    except Exception as e:
        connection.rollback()
        return False, f"Ошибка: {str(e)}"
    finally:
        connection.close()


def register_user(login, password, role_name, full_name):
    """
    Регистрирует нового пользователя и добавляет сотрудника с ФИО.
    Возвращает True, если успешно, иначе False.
    """
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Проверка логина
            cursor.execute("SELECT id FROM users WHERE login = %s", (login,))
            if cursor.fetchone():
                return False

            # Получение role_id
            cursor.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
            role = cursor.fetchone()
            if not role:
                return False
            role_id = role["id"]

            # Вставка пользователя
            cursor.execute("""
                INSERT INTO users (login, password_hash, role_id)
                VALUES (%s, %s, %s)
            """, (login, password_hash, role_id))
            user_id = cursor.lastrowid

            # Создание сотрудника (только full_name + created_by)
            cursor.execute("""
                INSERT INTO employees (full_name, created_by)
                VALUES (%s, %s)
            """, (full_name, user_id))

            connection.commit()
            return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        connection.close()
