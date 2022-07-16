from comunidade_impressionadora import database, loginManager
from datetime import datetime
from flask_login import UserMixin


@loginManager.user_loader
def loadUsuario(idUsuario):
    return Usuario.query.get(int(idUsuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    senha = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    fotoPerfil = database.Column(database.String, default='default.jpg')
    post = database.relationship('Post', backref='autor', lazy=True)
    comentario = database.relationship('Comentario', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não informado')

    def contarPosts(self):
        return len(self.post)




class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    fotoPost = database.Column(database.String)
    corpo = database.Column(database.Text, nullable=False)
    dataCriacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    idUsuario = database.Column(database.Integer,  database.ForeignKey('usuario.id'), nullable=False)



class Comentario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    corpo = database.Column(database.Text, nullable=False)
    idUsuario = database.Column(database.Integer,  database.ForeignKey('usuario.id'), nullable=False)
    dataCriacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)