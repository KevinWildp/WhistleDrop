from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import sqlite3
import os

# Datenbankpfad relativ zum Skriptverzeichnis
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../DB/keys.db"))

# Benutzer nach Basisdateinamen fragen
basisname = input("Bitte gib den Basisdateinamen der Datei ein (z.B. bericht.docx): ").strip()

# Dateipfade dynamisch erstellen
encrypted_file_path = basisname + '.enc'
encrypted_key_path = basisname + '.key'
output_file_path = 'entschluesselt_' + basisname

# Anmeldedaten
journalist_id = input("Journalist-ID: ").strip()
password = input("Passwort: ").strip()

# Privaten Schlüssel aus Datenbank laden
def load_private_key(journalist_id, password):
    import bcrypt
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM journalist_auth WHERE journalist_id = ?", (journalist_id,))
    auth = cursor.fetchone()
    if not auth or not bcrypt.checkpw(password.encode(), auth[0].encode()):
        conn.close()
        raise PermissionError("Authentifizierung fehlgeschlagen.")

    cursor.execute("SELECT key_value FROM private_keys WHERE journalist_id = ?", (journalist_id,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        raise ValueError("Kein privater Schlüssel für diesen Benutzer gefunden.")
    return result[0].encode()

# Privaten Schlüssel nach der Verwendung löschen
def delete_private_key(journalist_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM private_keys WHERE journalist_id = ?", (journalist_id,))
    conn.commit()
    conn.close()
    print("[!] Privater Schlüssel wurde aus der Datenbank gelöscht.")
    ("[+] Entschlüsselung abgeschlossen.")

# Privaten Schlüssel holen
try:
    print("[+] Entschlüssele AES-Schlüssel...")
    private_key_pem = load_private_key(journalist_id, password)
    private_key = RSA.import_key(private_key_pem)

    cipher_rsa = PKCS1_OAEP.new(private_key)

    with open(encrypted_key_path, 'rb') as f:
        encrypted_aes_key = f.read()

    aes_key = cipher_rsa.decrypt(encrypted_aes_key)

    print("[+] Entschlüssele die Datei...")
    with open(encrypted_file_path, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    print(f"[+] Speichere entschlüsselte Datei als {output_file_path}...")
    with open(output_file_path, 'wb') as f:
        f.write(data)

    print("[+] Entschlüsselung abgeschlossen.")
    delete_private_key(journalist_id)

except Exception as e:
    print(" Fehler:", e)

