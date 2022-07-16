from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade_impressionadora.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacaoSenha = PasswordField('Confirmaçao da Senha', validators=[DataRequired(), EqualTo('senha')])
    botaoSubmitCriarConta = SubmitField('Criar Conta')


    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça Login para continuar.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrarDados = BooleanField('Lembrar Dados de Acesso')
    botaoSubmitLogin = SubmitField('Fazer Login')



class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg','png','jpeg'])])

    curso_python = BooleanField('Python Impressionador')
    curso_excel = BooleanField('Excel Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_cd = BooleanField('Ciencia de Dados Impressionador')

    botaoSubmitEditarPerfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email = email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado com outro Usuário. Cadastre-se com outro e-mail.')




class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2,140)])
    foto_post = FileField('Adicione uma foto ao post', validators=[FileAllowed(['jpg','png','jpeg'])])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botaoSubmitCriarPost = SubmitField('Criar Post')



class FormCriarComentario(FlaskForm):
    corpo = TextAreaField('Escreva seu comentario aqui', validators=[DataRequired()])
    botaoSubmitCriarComentario = SubmitField('Criar Comentario')

class FormRecuperarSenha(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    botaoSubmitEnviarEmail = SubmitField('Recupearar Senha')


class FormAlterarSenha(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botaoSubmitAlterarSenha = SubmitField('Alterar Senha')