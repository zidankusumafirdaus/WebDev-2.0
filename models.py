import sqlite3
from werkzeug.security import generate_password_hash
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

class User:
    def __init__(self, id, username, password, email, role):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    @classmethod
    def get(cls, username=None, email=None):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        if username and email:
            interaksi.execute("SELECT * FROM users WHERE username=? AND email=?", (username, email))
        elif username:
            interaksi.execute("SELECT * FROM users WHERE username=?", (username,))
        elif email:
            interaksi.execute("SELECT * FROM users WHERE email=?", (email,))
        else:
            return None
        row = interaksi.fetchone()
        if row:
            return cls(*row)
        return None
    

    @classmethod
    def create(cls, username, password, email):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        hashed_password = generate_password_hash(password)
        interaksi.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        koneksi.commit()
        koneksi.close()

class Admin:
    def __init__(self, id, username, password, email,):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


    @classmethod
    def getadmin(cls, username=None, email=None):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        if username and email:
            interaksi.execute("SELECT * FROM admin WHERE username=? AND email=?", (username, email))
        elif username:
            interaksi.execute("SELECT * FROM admin WHERE username=?", (username,))
        elif email:
            interaksi.execute("SELECT * FROM admin WHERE email=?", (email,))
        else:
            return None
        row = interaksi.fetchone()
        if row:
            return cls(*row)
        return None
    

    @classmethod
    def create(cls, username, password, email):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        hashed_password = generate_password_hash(password)
        interaksi.execute("INSERT INTO admin (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        koneksi.commit()
        koneksi.close()

def create_tables():
    koneksi = sqlite3.connect(Config.DATABASE)
    interaksi = koneksi.cursor()

    interaksi.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    koneksi.commit()
    koneksi.close()

def initialize_superuser():
    koneksi = sqlite3.connect(Config.DATABASE)
    interaksi = koneksi.cursor()

    superuser_username = os.getenv("SUPERUSER_USERNAME")
    superuser_password = os.getenv("SUPERUSER_PASSWORD")
    superuser_email = os.getenv("SUPERUSER_EMAIL")

    # print(f"SUPERUSER_USERNAME: {superuser_username}")
    # print(f"SUPERUSER_PASSWORD: {superuser_password}")
    # print(f"SUPERUSER_EMAIL: {superuser_email}")
# cek ajaa
    if not (superuser_username and superuser_password and superuser_email):
        print("Superuser credentials are missing or incomplete in .env")
        koneksi.close()
        return

    hashed_password = generate_password_hash(superuser_password)

    interaksi.execute("SELECT * FROM users WHERE username=?", (superuser_username,))
    existing_superuser = interaksi.fetchone()

    if not existing_superuser:
        interaksi.execute("""
            INSERT INTO users (username, password, email, role)
            VALUES (?, ?, ?, 'superuser')
        """, (superuser_username, hashed_password, superuser_email))
        koneksi.commit()
        print("Superuser berhasil dibuat.")
    else:
        print("Superuser sudah ada.")

    koneksi.close()