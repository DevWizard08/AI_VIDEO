from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User:
    collection = None  # set in app.py

    @staticmethod
    def create(email=None, password=None, phone=None):
        if not ((email and password) or phone):
            raise ValueError("Must provide email+password or phone")

        doc = {"created_at": datetime.utcnow()}
        if email:
            doc["email"] = email.lower()
            doc["password_hash"] = bcrypt.generate_password_hash(password).decode()
        if phone:
            doc["phone"] = phone

        return User.collection.insert_one(doc).inserted_id

    @staticmethod
    def find_by_email(email):
        return User.collection.find_one({"email": email.lower()})

    @staticmethod
    def find_by_phone(phone):
        return User.collection.find_one({"phone": phone})

    @staticmethod
    def check_password(user_doc, password):
        return bcrypt.check_password_hash(user_doc["password_hash"], password)