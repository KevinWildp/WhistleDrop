# WhistleDrop

**WhistleDrop** ist eine minimalistische SecureDrop-Alternative, mit der vertrauliche Dokumente über das Tor-Netzwerk hochgeladen werden können.  
Die Dateien werden automatisch AES-verschlüsselt, der Schlüssel asymmetrisch mit RSA verschlüsselt – bereit für den Download durch einen Journalisten.

---

##  Voraussetzungen

- macOS oder Linux
- [Python 3](https://www.python.org/downloads/)
- [Tor](https://www.torproject.org/)
- [PyCryptodome](https://pypi.org/project/pycryptodome/)
- [Tor-Browser](https://www.torproject.org/download/)

---

## 🛠 Installation

### Python-Abhängigkeit installieren

pip install pycryptodome

### RSA-Schlüssel generieren (einmalig)
openssl genrsa -out private_key.pem 4096
openssl rsa -in private_key.pem -pubout -out public_key.pem

### Tor Hidden Service einrichten
1. Verzeichnis anlegen
   mkdir -p ~/whistledrop/tor_hidden_service

2. Temporäre Tor-Konfigurationsdatei erstellen
   HiddenServiceDir /Users/USERNAME/whistledrop/tor_hidden_service
   HiddenServicePort 80 127.0.0.1:5000

3. Berechtigungen setzen
   chmod 700 ~/whistledrop/tor_hidden_service

### Anwendung starten
