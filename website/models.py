from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class EditedNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    edited_content = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    original_note = db.relationship('Note', backref='edited_versions')