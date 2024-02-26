from db.db_connection import db
from datetime import datetime
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def get_email(self):
        return self.email

    def get_id(self):
        # In SQLAlchemy, primary key field is automatically named `id`
        return self.id

    def __init__(self, email, password, age, gender, created_at):
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.created_at = created_at

class MzRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    voice_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, nullable=True)
    rta = db.Column(db.TIMESTAMP, nullable=True) # 완료시간
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, user_id, age, gender, voice_url, status, eta, created_at):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.voice_url = voice_url
        self.status = status
        self.eta = eta
        self.created_at = created_at

class MzResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mz_request_id = db.Column(db.Integer, db.ForeignKey('mz_request.id'), nullable=False)
    condition_image_url = db.Column(db.String(255), nullable=True)
    condition_gif_url = db.Column(db.String(255), nullable=True)
    voice_image_url = db.Column(db.String(255), nullable=True)
    voice_gif_url = db.Column(db.String(255), nullable=True)
    condition_image_rating = db.Column(db.Integer, nullable=True)
    condition_gif_rating = db.Column(db.Integer, nullable=True)
    voice_image_rating = db.Column(db.Integer, nullable=True)
    voice_gif_rating = db.Column(db.Integer, nullable=True)
    condition_image_score = db.Column(db.Float, nullable=True)
    condition_gif_score = db.Column(db.Float, nullable=True)
    voice_image_score = db.Column(db.Float, nullable=True)
    voice_gif_score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, mz_request_id, created_at):
        self.mz_request_id = mz_request_id
        self.created_at = created_at
