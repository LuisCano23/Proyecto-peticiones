from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), unique=True, nullable=False)
    soy_de_consolidacion = db.Column(db.Integer, default=0)  
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Discipulo(db.Model):
    __tablename__ = 'discipulo'
    
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), unique=True, nullable=False)
    
    lider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    genero = db.Column(db.String(10), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    lider = db.relationship('User', backref=db.backref('discipulos', lazy=True))

class Peticiones(db.Model):
    __tablename__ = 'peticiones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    peticion = db.Column(db.String(500), nullable=False)
    invasion = db.Column(db.Integer, default=0)