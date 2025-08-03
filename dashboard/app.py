from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from pymongo import MongoClient
from config import MONGO_URI

app = Flask(__name__)
admin = Admin(app, name="Admin Dashboard", template_mode="bootstrap3")

client = MongoClient(MONGO_URI)
db = client.botdb

admin.add_view(ModelView(db.users, "Users"))
admin.add_view(ModelView(db.files, "Conversions"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
  
