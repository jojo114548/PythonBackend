from flask import Flask, render_template, request, jsonify,flash,redirect
import json
import os
from  models import Usuario,db,Migrate
app = Flask(__name__)

    # Configurações do aplicativo
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Necessário para usar flash messages
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Necessário para usar flash messages
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db)

 
#rotas
@app.route("/")#caminho
@app.route("/formulario")#caminho
def  formulario():#funçao para carregar as informações que vão aparecer na rota ou caminho 
    return render_template("formulario.html")
@app.route("/cadastro-usuario", methods=["POST"])#caminho

def cadastro_usuario():#funçao para carregar as informações que vão aparecer na rota ou caminho

    if request.method == "POST":
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        email = request.form.get('email')
        senha = request.form.get('senha')
    
        usuario=Usuario(
            nome= nome,
            email= email,
            idade=idade,
            senha=senha
            )
            
        db.session.add(usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        
        return redirect("/formulario")#redireciona para a rota formulario

@app.route("/blog")#caminho
def blog():#funçao para carregar as informações que vão aparecer na rota ou caminho 
    return render_template("blog.html")

if __name__ == '__main__': #executa esse codigo abaixo quando estiver executando essa rota
    app.run(debug=True)#rodar o site 


