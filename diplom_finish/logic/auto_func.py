from db.db import get_connection
from utils.logger import log_action

def authenticate_user(login, password):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.id AS user_id,
                    u.role,
                    e.full_name
                FROM users u
                LEFT JOIN employees e ON u.id = e.id
                WHERE u.login = %s AND u.password_hash = %s
            """, (login, password))
            user = cursor.fetchone()

            if user:
                print("[DEBUG] user =", user)
                log_action(
                    user_id=user["user_id"],
                    action="Вход",
                    description=f"Пользователь {user['full_name'] or 'Без ФИО'} вошёл в систему"
                )
                return {
                    "id": user["user_id"],
                    "role": user["role"],
                    "full_name": user["full_name"] or "Пользователь"
                }

            return None
    finally:
        connection.close()

def reset_password(login, new_password):
    """
    Сброс пароля по логину.
    Возвращает (True, сообщение) при успехе, иначе (False, сообщение).
    """

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE login = %s", (login,))
            user_id = cursor.fetchone()["id"]
            log_action(user_id=user_id, action="Сброс пароля", description=f"Пользователь {login} сбросил пароль")

            if not user_id:
                return False, "Пользователь не найден"

            cursor.execute("""
                UPDATE users 
                SET password_hash = %s 
                WHERE login = %s
            """, (new_password, login))
            connection.commit()
            return True, "Пароль успешно изменён"
    except Exception as e:
        connection.rollback()
        return False, f"Ошибка: {str(e)}"
    finally:
        connection.close()


def register_user(login, password, role_id, full_name):
    """
    Регистрирует нового пользователя и создаёт сотрудника с ФИО (если это сотрудник).
    Возвращает True, если успешно, иначе False.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Проверка логина
            cursor.execute("SELECT id FROM users WHERE login = %s", (login,))
            if cursor.fetchone():
                return False

            # Вставка пользователя
            cursor.execute("""
                INSERT INTO users (login, password_hash, role)
                VALUES (%s, %s, %s)
            """, (login, password, role_id))
            user_id = cursor.lastrowid

            # Добавление в employees — только если роль связана с персоналом
            if role_id in ("employee", "hr"):
                cursor.execute("""
                    INSERT INTO employees (id, full_name)
                    VALUES (%s, %s)
                """, (user_id, full_name))

            log_action(user_id=user_id, action="Регистрация",
                       description=f"Зарегистрирован новый пользователь {login} с ролью {role_id}")

            connection.commit()
            return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        connection.close()
