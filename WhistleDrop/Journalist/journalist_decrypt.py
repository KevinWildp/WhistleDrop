from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

# Benutzer nach Basisdateinamen fragen
basisname = input("Bitte gib den Basisdateinamen der Datei ein (z.B. bericht.docx): ").strip()

# Dateipfade dynamisch erstellen
encrypted_file_path = basisname + '.enc'   # Pfad zur verschlüsselten Datei
encrypted_key_path = basisname + '.key'    # Pfad zum verschlüsselten AES-Schlüssel
private_key_path = 'private_key.pem'       # Pfad zum privaten RSA-Schlüssel
output_file_path = 'entschluesselt_' + basisname  # Pfad zur entschlüsselten Zieldatei

print("[+] Entschlüssele AES-Schlüssel...")
# Privaten Schlüssel laden
with open(private_key_path, 'rb') as f:
    private_key = RSA.import_key(f.read())

# RSA-Entschlüsselungsobjekt erstellen
cipher_rsa = PKCS1_OAEP.new(private_key)

# Verschlüsselten AES-Schlüssel laden
with open(encrypted_key_path, 'rb') as f:
    encrypted_aes_key = f.read()

# AES-Schlüssel mit privatem RSA-Schlüssel entschlüsseln
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

print("[+] Entschlüssele die Datei...")
# Verschlüsselte Datei öffnen und notwendige Parameter auslesen
with open(encrypted_file_path, 'rb') as f:
    nonce = f.read(16)     # Nonce für AES-Entschlüsselung
    tag = f.read(16)       # Authentifizierungstag zur Integritätsprüfung
    ciphertext = f.read()  # Verschlüsselter Dateiinhalt

# AES-Entschlüsselungsobjekt erstellen
cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)

# Datei entschlüsseln und Authentizität prüfen
data = cipher_aes.decrypt_and_verify(ciphertext, tag)

print(f"[+] Speichere entschlüsselte Datei als {output_file_path}...")
# Entschlüsselte Datei speichern
with open(output_file_path, 'wb') as f:
    f.write(data)

print("[+] Entschlüsselung abgeschlossen.")