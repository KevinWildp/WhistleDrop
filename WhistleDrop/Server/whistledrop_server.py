
from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

UPLOAD_FOLDER = 'uploads'
KEY_FOLDER = 'keys'
ENCRYPTED_FOLDER = 'encrypted'
PUBLIC_KEYS_DB = 'public_keys.txt'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER
app.config['KEY_FOLDER'] = KEY_FOLDER

for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, KEY_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def load_public_key():
    with open("public_key.pem", "r") as f:
        public_key_pem = f.read()

    try:
        public_key = RSA.import_key(public_key_pem.encode())

        if not public_key.has_private():
            return public_key
        else:
            raise ValueError("Die Datei enthält einen privaten Schlüssel, ein öffentlicher Schlüssel wird erwartet.")
    except ValueError as e:
        raise ValueError("Ungültiges RSA-Schlüsselformat. Erwartet wird ein PEM-formatierter öffentlicher Schlüssel "
                         "(z. B. BEGIN PUBLIC KEY). Falls ein SSH-Schlüssel verwendet wurde, bitte vorher konvertieren. "
                         f"Fehler: {str(e)}")

def encrypt_file(file_path, encrypted_file_path, public_key):
    aes_key = get_random_bytes(32)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)
    with open(encrypted_file_path, 'wb') as f:
        f.write(cipher_aes.nonce)
        f.write(tag)
        f.write(ciphertext)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    encrypted_key_path = os.path.join(app.config['KEY_FOLDER'], os.path.basename(file_path) + '.key')
    with open(encrypted_key_path, 'wb') as f:
        f.write(encrypted_aes_key)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Keine Datei hochgeladen.', 400
        file = request.files['file']
        if file.filename == '':
            return 'Keine Datei ausgewählt.', 400
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            public_key = load_public_key()
            encrypted_file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename + '.enc')
            encrypt_file(file_path, encrypted_file_path, public_key)
            os.remove(file_path)
            return f'Datei {filename} wurde sicher verschlüsselt gespeichert.'
    return '''
    <!doctype html>
    <title>WhistleDrop Upload</title>
    <h1>WhistleDrop: Datei hochladen</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
