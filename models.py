from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True, choices=['admin', 'user'])
    created_at = DateTimeField(default=datetime.utcnow)

class Project(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
