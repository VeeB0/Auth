import sqlite3


# Функция создания базы данных, если ее нет
def create_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY NOT NULL,
            password TEXT,
            restrict_password INTEGER DEFAULT 1,
            block_user INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0
        );
    """)
    connection.commit()
    connection.close()


# Функция проверки логина и пароля на соответсвие критериям
# True, если логин больше 4 символов и пароль имеет цифры и арифметические знаки, а так же
# если буквы написаны латиницей, False - в противном случае.
def check_login_and_password(username, password):
    # login_valid = len(username) >= 4
    login_valid = True

    password_valid = any(char.isdigit() for char in password) \
                     and any(char in "-/+*" for char in password)

    return login_valid and password_valid


# Функция проверки наличия прав администратора у пользователя
# True, если у пользователя есть права администратора, False - в противном случае.
def is_admin(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT is_admin FROM users WHERE username = ?
    """, (username,))
    is_admin1 = cursor.fetchone()[0]
    connection.close()
    return is_admin1 == 1


def is_blocked(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT block_user FROM users WHERE username = ?
    """, (username,))
    block_user1 = cursor.fetchone()[0]
    connection.close()
    return block_user1 == 1


# Функция проверки существования пользователя
# True, если пользователь существует, False - в противном случае.
def is_user_exists(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    # Получить значение restrict_password для пользователя
    cursor.execute("""
        SELECT COUNT(*) FROM users WHERE username = ?
    """, (username,))
    count = cursor.fetchone()[0]
    connection.close()
    return count > 0


# Функция проверки правильности пароля
# True, если пароль совпал, False - в противном случае.
def is_password_correct(username, password):
    password = encrypt(password)
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Получить значение password для пользователя
    cursor.execute("""
        SELECT password FROM users WHERE username = ?
    """, (username,))

    stored_password = cursor.fetchone()[0]
    connection.close()

    return password == stored_password


# Функция изменения пароля
# True, если пароль успешно изменен, False - в противном случае.
def change_password(username, new_password):
    new_password = encrypt(new_password)
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users SET password = ? WHERE username = ?
    """, (new_password, username))
    connection.commit()
    connection.close()
    return True


# Функция регистрации нового пользователя
def register_user(username, password):
    password = encrypt(password)
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """, (username, password))
    connection.commit()
    connection.close()
    return True


# Функция проверки ограничения на пароль у пользователя
# True, если есть ограничение, False - в противном случае.
def is_password_restrict(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT restrict_password FROM users WHERE username = ?
    """, (username,))
    stored_restrict = cursor.fetchone()[0]
    connection.close()
    return 1 == stored_restrict


# Функция создания нового пользователя админом
# True, если пользователь успешно добавлен, False - в противном случае.
def add_new_user(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO users (username)
        VALUES (?)
    """, (username,))
    connection.commit()
    connection.close()


# Функция получения списка пользователей из базы данных
def get_users():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username, block_user, restrict_password
        FROM users
        WHERE is_admin != 1
    """)
    return cursor.fetchall()


def block_user(all_users):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    for username in all_users:
        cursor.execute("""
                    UPDATE users SET block_user = 1 WHERE username = ?
                """, (username,))
    connection.commit()
    connection.close()


def unblock_user(all_users):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    for username in all_users:
        cursor.execute("""
                    UPDATE users SET block_user = 0 WHERE username = ?
                """, (username,))
    connection.commit()
    connection.close()


def restrictionOn_user(all_users):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    for username in all_users:
        cursor.execute("""
                    UPDATE users SET restrict_password = 1 WHERE username = ?
                """, (username,))
    connection.commit()
    connection.close()


def restrictionOff_user(all_users):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    for username in all_users:
        cursor.execute("""
                    UPDATE users SET restrict_password = 0 WHERE username = ?
                """, (username,))
    connection.commit()
    connection.close()


def encrypt(password, text="123456", block_size=1):
    password_bytes = text.encode("utf-8")
    a = password_bytes[0]
    c = password_bytes[1]
    g0 = password_bytes[2]

    gamma = [g0]
    for i in range(1, len(password) // block_size + 1):
        gamma.append((a * gamma[-1] + c) % 256)

    text_bytes = password.encode("utf-8")
    hashed_bytes = [t ^ g for t, g in zip(text_bytes, gamma)]

    return bytes(hashed_bytes)



def decrypt(cipher_text, shift=3):
    plain_text = ""
    for char in cipher_text:
        byte = ord(char)
        new_byte = byte - shift
        # Переход к концу алфавита/цифр при отрицательном значении
        if new_byte < 0:
            new_byte += 256
        plain_text += chr(new_byte)
    return plain_text
