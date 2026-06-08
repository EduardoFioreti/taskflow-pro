from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id       = db.Column(db.Integer, primary_key=True)
    nome     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    senha    = db.Column(db.String(200), nullable=False)  # hash bcrypt
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    tarefas  = db.relationship("Task", backref="usuario", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Task(db.Model):
    __tablename__ = "tasks"

    id          = db.Column(db.Integer, primary_key=True)
    titulo      = db.Column(db.String(200), nullable=False)
    descricao   = db.Column(db.Text, nullable=True)
    prioridade  = db.Column(db.String(10), nullable=False, default="media")  # baixa | media | alta
    status      = db.Column(db.String(20), nullable=False, default="pendente")  # pendente | em_andamento | concluida
    categoria   = db.Column(db.String(30), nullable=False, default="geral")  # geral | pessoal | trabalho | estudos
    prazo       = db.Column(db.Date, nullable=True)  # opcional
    criado_em   = db.Column(db.DateTime, default=datetime.utcnow)

    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.titulo}>"