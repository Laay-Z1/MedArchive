import hashlib
import hmac
import os

from database.db import get_connection

ITERATIONS = 310_000


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def register_user(login: str, password: str, full_name: str):
    login = login.strip()
    full_name = full_name.strip()

    if not login or not password or not full_name:
        raise ValueError("Заполните ФИО, логин и пароль.")
    if len(password) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов.")

    with get_connection() as connection:
        connection.execute(
            "INSERT INTO Users (login, password_hash, full_name) VALUES (?, ?, ?)",
            (login, _hash_password(password), full_name),
        )


def authenticate_user(login: str, password: str):
    with get_connection() as connection:
        user = connection.execute(
            "SELECT user_id, login, password_hash, full_name "
            "FROM Users WHERE login = ?",
            (login.strip(),),
        ).fetchone()

    if user is None or not _verify_password(password, user["password_hash"]):
        return None

    return {
        "user_id": user["user_id"],
        "login": user["login"],
        "full_name": user["full_name"],
    }
