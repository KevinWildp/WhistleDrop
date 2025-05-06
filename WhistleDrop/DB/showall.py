import sqlite3

def show_all_public_keys():
    conn = sqlite3.connect("keys.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, server_id, key_value FROM public_keys")
        rows = cursor.fetchall()

        if not rows:
            print("Keine öffentlichen Schlüssel in der Datenbank gefunden.")
            return

        print("Öffentliche Schlüssel in der Datenbank:")
        for row in rows:
            key_id, server_id, key_value = row
            print(f"\nID: {key_id}")
            print(f"Server-ID: {server_id}")
            print(f"Schlüsselanfang: {key_value[:100]}...")

    except sqlite3.OperationalError as e:
        print("Fehler:", e)
        print("Hinweis: Existiert die Tabelle 'public_keys' bereits?")
    finally:
        conn.close()

if __name__ == "__main__":
    show_all_public_keys()
