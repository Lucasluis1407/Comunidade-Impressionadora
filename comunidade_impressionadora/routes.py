from flask import render_template,url_for, request, flash, redirect, abort
from comunidade_impressionadora import app, database, bcrypt, mail, Message
from comunidade_impressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormCriarComentario, FormRecuperarSenha, FormAlterarSenha
from comunidade_impressionadora.models import Usuario, Post, Comentario
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def capa():
    return render_template('capa.html')

@app.route('/home')
@login_required
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/home/contato')
def contato():
    return render_template('contato.html')

@app.route('/home/usuarios')
@login_required
def usuarios():
    listaUsuarios = []

    usuarios = Usuario.query.all()

    for usuario in usuarios:
        listaUsuarios.append(usuario)

    
    return render_template('usuarios.html', listaUsuarios = listaUsuarios)

@app.route('/home/login', methods=['GET', 'POST'])
def login():
    formLogin = FormLogin()
    formCriarConta = FormCriarConta()

    if formLogin.validate_on_submit() and 'botaoSubmitLogin' in request.form:

        usuario = Usuario.query.filter_by(email = formLogin.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario, remember= formLogin.lembrarDados.data)
            # Exibir mensagen de login com sucesso!
            flash(f'Login feito com sucesso no E-mail: {formLogin.email.data}', 'alert-success')

            paramNext = request.args.get('next')

            if paramNext:
                return redirect(paramNext)

            else:
                # Redirecionar para a Homepage
                return redirect(url_for('home'))
        else:
            flash('Falha no Login! E-mail ou senha inválidos', 'alert-danger')


    if formCriarConta.validate_on_submit() and 'botaoSubmitCriarConta' in request.form:
        # Exibir mensagem de que criou a conta com sucesso
        flash(f'Sua conta foi criada com sucesso no E-mail: {formCriarConta.email.data}', 'alert-success')

        # Criação de um Usuario

        senhaCriptografada = bcrypt.generate_password_hash(formCriarConta.senha.data)
        usuario = Usuario(username = formCriarConta.username.data, email = formCriarConta.email.data, senha = senhaCriptografada)

        # Adicionando a sessão no Banco de dados

        database.session.add(usuario)

        # Commitando para o Banco de dados

        database.session.commit()

        # Redirecionar para a Homepage
        return redirect(url_for('home'))

    return render_template('login.html', formLogin = formLogin, formCriarConta = formCriarConta)


@app.route('/home/recuperar_senha', methods=['GET', 'POST'])
def recuperarSenha():
    form = FormRecuperarSenha()
    email = Usuario.query.filter_by(email = form.email.data).first()
    if email and form.validate_on_submit():
        msg = Message( 
                    'Recuperação de senha do APP-WEB da Comunidade Impressionadora', 
                    sender ='lucasluisouza@gmail.com', 
                    recipients = [form.email.data] 
                ) 
        msg.body = 'Entre neste link para alterar sua senha: https://hashtagtreinamentoscomunidade.herokuapp.com/home/alterar_senha'
        mail.send(msg)
        return 'Email enviado, Por favor confira sua caixa de entrada e acesse o link para mudar sua senha de acesso'
    else:
        flash('Este E-mail não está cadastrado', 'alert-danger')
    return render_template('recuperarsenha.html', form =form )


@app.route('/home/alterar_senha', methods=['GET', 'POST'])
def alterarSenha():
    form = FormAlterarSenha()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email = form.email.data).first()
        senhaCriptografada = bcrypt.generate_password_hash(form.senha.data)
        usuario.senha = senhaCriptografada
        database.session.commit()
        flash('Senha Alterada Com Sucesso', 'alert-danger')
        return redirect(url_for('login'))

    return render_template('alterarsenha.html', form = form )


@app.route('/home/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('capa'))



@app.route('/home/perfil')
@login_required
def perfil():
    meus_posts = []
    posts = Post.query.order_by(Post.id.desc())
    for post in posts:
        if current_user == post.autor:
            meus_posts.append(post)

    fotoPerfilAtual = url_for('static', filename='fotos_perfil/{}'.format(current_user.fotoPerfil))
    return render_template('perfil.html', fotoPerfilAtual=fotoPerfilAtual, meus_posts = meus_posts)


def salvarPost(imagem):
    codigo = secrets.token_hex(8)
    nome ,extensao = os.path.splitext(imagem.filename)
    nome_arquivo =  nome + codigo + extensao

    caminho_completo = os.path.join(app.root_path, 'static/fotos_posts', nome_arquivo)

    tamanho = (1000, 1000)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    imagem_reduzida.save(caminho_completo)

    return nome_arquivo



@app.route('/home/post/criar', methods=['GET', 'POST'])
@login_required
def criarPost():
    form = FormCriarPost()
    if form.validate_on_submit():
        if form.foto_post.data:
            
            nome_imagem = salvarPost(form.foto_post.data)
            post = Post(titulo = form.titulo.data, fotoPost = nome_imagem ,corpo = form.corpo.data, autor = current_user)
        else:
            post = Post(titulo = form.titulo.data ,corpo = form.corpo.data, autor = current_user)

        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvarImagem(imagem):
    codigo = secrets.token_hex(8)
    nome ,extensao = os.path.splitext(imagem.filename)
    nome_arquivo =  nome + codigo + extensao

    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    imagem_reduzida.save(caminho_completo)

    return nome_arquivo


def atualizarCursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)

    return ';'.join(lista_cursos)


@app.route('/home/perfil/editar', methods=['GET', 'POST'])
@login_required
def editarPerfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvarImagem(form.foto_perfil.data)
            current_user.fotoPerfil= nome_imagem

        current_user.cursos = atualizarCursos(form)

        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        

    fotoPerfilAtual = url_for('static', filename='fotos_perfil/{}'.format(current_user.fotoPerfil))
    return render_template('editarperfil.html', fotoPerfilAtual=fotoPerfilAtual, form = form)






@app.route('/home/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibirPost(post_id):
    post = Post.query.get(post_id)

    form_coment = FormCriarComentario()
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
            form.foto_post.data = post.fotoPost
        
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            if form.foto_post.data:
                nome_imagem = salvarPost(form.foto_post.data)
                post.fotoPost = nome_imagem

            database.session.commit()
            flash('Post Editado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None

    if form_coment.validate_on_submit():
        comentario = Comentario(corpo = form_coment.corpo.data, autor = current_user)

        database.session.add(comentario)
        database.session.commit()
        flash('Comentario feito com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    
    
    comentarios = Comentario.query.order_by(Comentario.id.desc())
    
    return render_template('post.html', post = post, form = form , form_coment =form_coment , comentarios = comentarios )




    
@app.route('/home/post/comentario/<comentario_id>', methods = ['GET','POST'])
@login_required
def editarComentario(comentario_id):
    comentario = Comentario.query.get(comentario_id)

    if current_user == comentario.autor:
        form_coment = FormCriarComentario()
        if request.method == 'GET':
            form_coment.corpo.data = comentario.corpo
        
        elif form_coment.validate_on_submit():
            comentario.corpo = form_coment.corpo.data

            database.session.commit()
            flash('Comentario Editado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    
    else:
        form_coment = None
        
    return render_template('editarcomentario.html', form_coment =form_coment , comentario = comentario)


@app.route('/home/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluirPost(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    else:
        abort(403)


@app.route('/home/post/comentario/<comentario_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluirComentario(comentario_id):
    comentario = Comentario.query.get(comentario_id)
    if current_user == comentario.autor:
        database.session.delete(comentario)
        database.session.commit()
        flash('Comentario Excluído com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    else:
        abort(403)