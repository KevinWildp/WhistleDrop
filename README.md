
# 🕵️ WhistleDrop – Sicherer Upload via Tor

**WhistleDrop** ist eine minimalistische SecureDrop-Alternative, mit der vertrauliche Dokumente über das Tor-Netzwerk hochgeladen werden können.  
Die Dateien werden automatisch AES-verschlüsselt, der Schlüssel asymmetrisch mit RSA verschlüsselt – bereit für den Download durch einen Journalisten.

---

## 📦 Voraussetzungen

- macOS oder Linux
- [Python 3](https://www.python.org/downloads/)
- [Tor](https://www.torproject.org/)
- [PyCryptodome](https://pypi.org/project/pycryptodome/)
- [Tor-Browser](https://www.torproject.org/download/)

---

## 🛠 Installation

### 1. Projekt klonen

```bash
git clone https://github.com/deinbenutzername/whistledrop.git
cd whistledrop
```

### 2. Python-Abhängigkeit installieren

```bash
pip install pycryptodome
```

---

## 🔐 RSA-Schlüssel generieren

```bash
openssl genrsa -out private_key.pem 4096
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

- `private_key.pem`: bleibt beim Journalisten
- `public_key.pem`: wird für den Server gebraucht

→ Kopiere den Inhalt von `public_key.pem` in die Datei `public_keys.txt`

---

## 🧱 Tor Hidden Service einrichten

### 1. Verzeichnisse anlegen

```bash
mkdir -p ~/whistledrop/tor_hidden_service
```

### 2. Temporäre Tor-Konfigurationsdatei erstellen

Datei `torrc-temp`:

```ini
HiddenServiceDir /Users/USERNAME/whistledrop/tor_hidden_service
HiddenServicePort 80 127.0.0.1:5000
```

> ✏️ Ersetze `USERNAME` mit deinem macOS-Benutzernamen.

### 3. Berechtigungen setzen

```bash
chmod 700 ~/whistledrop/tor_hidden_service
```

---

## ▶️ Anwendung starten

### 1. Terminal A – Tor starten

```bash
tor -f torrc-temp
```

Warte ca. 10 Sekunden.

### 2. Terminal B – Flask-Server starten

```bash
python3 whistledrop_server.py
```

---

## 🌐 Zugriff via Tor

```bash
cat ~/whistledrop/tor_hidden_service/hostname
```

→ Diese `.onion`-Adresse im **Tor-Browser** öffnen  
→ Upload-Oberfläche wird angezeigt

---

## 📰 Datei entschlüsseln (Journalist)

```bash
python3 journalist_decrypt.py
```

→ Die verschlüsselte Datei (`.enc`) und der Schlüssel (`.key`) müssen im selben Verzeichnis liegen.  
→ Der Benutzer wird nach dem Dateinamen gefragt.  
→ Die entschlüsselte Datei wird als `entschluesselt_DATEINAME` gespeichert.

---

## 🔒 Sicherheitshinweis

- Die Adresse ist nicht öffentlich auffindbar
- AES-256 + RSA bieten starken Schutz
- Vertraue nur auf manuelle Schlüsselverteilung
- Nutze immer den **Tor-Browser**

---

## 📄 Lizenz

MIT License – für Forschung, Bildung und journalistische Projekte.
