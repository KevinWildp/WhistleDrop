import sqlite3
import bcrypt
import os

DB_NAME = "keys.db"


# === DB INIT ===

def init_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)  # frische DB für Testzwecke
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE journalist_auth
                   (
                       journalist_id TEXT PRIMARY KEY,
                       password_hash TEXT NOT NULL
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE private_keys
                   (
                       id            INTEGER PRIMARY KEY AUTOINCREMENT,
                       journalist_id TEXT NOT NULL,
                       key_value     TEXT NOT NULL,
                       FOREIGN KEY (journalist_id) REFERENCES journalist_auth (journalist_id)
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE public_keys
                   (
                       id        INTEGER PRIMARY KEY AUTOINCREMENT,
                       server_id TEXT NOT NULL,
                       key_value TEXT NOT NULL
                   )
                   """)

    conn.commit()
    conn.close()


# === REGISTRIERUNG ===

def register_journalist(journalist_id, plain_password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM journalist_auth WHERE journalist_id = ?", (journalist_id,))
    if cursor.fetchone():
        print(f" Journalist '{journalist_id}' existiert bereits.")
        conn.close()
        return

    password_hash = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())

    cursor.execute("INSERT INTO journalist_auth (journalist_id, password_hash) VALUES (?, ?)",
                   (journalist_id, password_hash.decode()))

    conn.commit()
    conn.close()
    print(f" Journalist '{journalist_id}' registriert.")


# === AUTH ===

def authenticate_journalist(journalist_id, plain_password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM journalist_auth WHERE journalist_id = ?", (journalist_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False

    stored_hash = result[0].encode()
    return bcrypt.checkpw(plain_password.encode(), stored_hash)


# === SCHLÜSSEL SPEICHERN ===

def insert_private_key(journalist_id, filepath):
    with open(filepath, "r") as f:
        key_data = f.read()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO private_keys (journalist_id, key_value) VALUES (?, ?)",
                   (journalist_id, key_data))

    conn.commit()
    conn.close()
    print(" Privater Schlüssel eingefügt.")


def insert_public_key(server_id, filepath):
    with open(filepath, "r") as f:
        key_data = f.read()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO public_keys (server_id, key_value) VALUES (?, ?)",
                   (server_id, key_data))

    conn.commit()
    conn.close()
    print(" Öffentlicher Schlüssel eingefügt.")


# === SCHLÜSSEL LADEN ===

def get_private_key(journalist_id, plain_password):
    if not authenticate_journalist(journalist_id, plain_password):
        raise PermissionError(" Authentifizierung fehlgeschlagen.")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT key_value FROM private_keys WHERE journalist_id = ?", (journalist_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        raise ValueError(" Kein privater Schlüssel gefunden.")

    return result[0]


def get_public_key(server_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT key_value FROM public_keys WHERE server_id = ?", (server_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        raise ValueError(" Kein öffentlicher Schlüssel gefunden.")

    return result[0]


# === TESTLAUF ===

if __name__ == "__main__":
    init_db()

    # Registrierung und Schlüsselinsertion
    register_journalist("wike1017", "geheim123")

    # ====================================================================
    insert_private_key("wike1017", "private_key.pem")
    insert_public_key("srv001", "public_key.pem")
    # ====================================================================
    insert_private_key("wike1017", "private_key_2.pem")
    insert_public_key("srv002", "public_key_2.pem")
    # ====================================================================
    insert_private_key("wike1017", "private_key_3.pem")
    insert_public_key("srv003", "public_key_3.pem")
    # ====================================================================
    insert_private_key("wike1017", "private_key_4.pem")
    insert_public_key("srv004", "public_key_4.pem")
    # ====================================================================
    insert_private_key("wike1017", "private_key_5.pem")
    insert_public_key("srv005", "public_key_5.pem")

    # Test: Schlüssel laden
    try:
        priv = get_private_key("wike1017", "geheim123")
        print("\n Privater Schlüssel geladen:\n", priv)
    except Exception as e:
        print("Fehler beim Laden des privaten Schlüssels:", e)

    try:
        pub = get_public_key("srv001")
        print("\n Öffentlicher Schlüssel geladen:\n", pub)
    except Exception as e:
        print("Fehler beim Laden des öffentlichen Schlüssels:", e)
