from flask import Flask,request,jsonify,render_template,url_for,redirect,flash
import json ,os,uuid

app=Flask(__name__)

app.config['SECRET_KEY'] = "JOJO55555" # Configuração da chave secreta
def carregar_usuarios():
    try:#Permite que o programa continue a executar mesmo quando ocorrem erros, evitando interrupções inesperadas
     if os.path.exists("usuarios.json"):
       with open("usuarios.json","r",encoding="utf-8") as arquivo:#lendo
         return json.load(arquivo)
     else:
       return [] #vazio se não existir o arquivo
    except:
      return [] #retorna vazio se der erro
    

def salvar_usuario(usuario):
  
  usuarios=carregar_usuarios()

  try:
    #adicionar novo usuario
    usuarios.append(usuario)

    with open("usuarios.json","w",encoding="utf-8") as arquivo:#criando
      json.dump(usuarios, arquivo,indent=4)

      return True #retorna true se deu tudo certo ao salvar 
  except:
     return False #se der erro ao salvar 
  
def deletar_usuario(id):
    usuarios=carregar_usuarios()

    usuarios_filtrados=[usuario for usuario in usuarios if usuario.get("id")!=id]
  
    if len(usuarios)==len(usuarios_filtrados):
      return False
    try:
      with open("usuarios.json","w",encoding="utf-8") as arquivo:
        json.dump(usuarios_filtrados, arquivo,indent=4)
        return True
    except:
         return False
def atualizar_usuario(id, novos_dados):
  usuarios=carregar_usuarios()
  atualizado=False

  for usuario in usuarios:
          if usuario["id"] == id:
              usuario.update(novos_dados)  # atualiza os campos
              atualizado = True
              break

  else:
        return False
  try:
    with open("usuarios.json","w",encoding="utf-8") as arquivo:
      json.dump(usuarios, arquivo,indent=4)
    return True
  except:
    return False 

@app.route("/") #caminho
def home():
   return render_template("login.html") 

@app.route("/cadastrar-usuarios", methods=["POST","GET"])
def cadastro():
   return render_template("cadastrar-usuarios.html") 

@app.route("/cadastro-usuarios", methods=["POST","GET"])
def cadastrar_usuario():

    #recuperando os dados digitados
    nome=request.form.get("nome")
    email=request.form.get("email")
    cpf=request.form.get("cpf")
    senha=request.form.get("senha")
    idade=request.form.get("idade")
    #dicionario
    usuario={
      "id":str(uuid.uuid4()),
      "nome":nome,
      "cpf":cpf,
      "email":email,
      "idade":idade,
      "senha":senha    
      }
    #adicionando o usuario na função salvar usuario e assim salvando no arquivo json 
    status=salvar_usuario(usuario)

    if status:
      return  redirect(url_for('cadastro',alerta="Usuário cadastrado com sucesso!"))

    
@app.route("/usuarios")
def buscar_usuarios():

    usuarios=carregar_usuarios()
    return render_template("usuarios.html", usuarios=usuarios,status=None)

@app.route("/usuarios/<id>",methods=["DELETE"])
def excluir_usuario(id):
   sucesso=deletar_usuario(id)
   if sucesso:
     return jsonify({"message": "Usuario deletado com sucesso"}), 200
   else:
      return jsonify({"message": "Erro ao deletar usuario"}), 400
   

@app.route("/usuarios/json", methods=["GET"])
def buscar_usuarios_json():
    
    usuarios = carregar_usuarios()
    return jsonify(usuarios)

@app.route('/usuarios/<id>',methods=["PUT"])
def editar_usuario(id):
    novos_dados = request.json  # recebe os novos dados do usuário em JSON
    sucesso = atualizar_usuario(id, novos_dados)

    if sucesso:
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao atualizar usuário"}), 400
    
@app.route('/usuarios_nome/',methods=["GET"])
def usuario_nome():
    nome = request.args.get("nome") 
    usuarios = carregar_usuarios()

    return render_template("usuarios_nome.html",nome=nome,usuarios=usuarios)

@app.route('/login')
def pagina_login():
    return render_template("login.html")

@app.route('/acessando/', methods=["POST","GET"] )   
def  acesso_cliente():
      email = request.form.get("email")
      senha = request.form.get("senha")
      usuarios = carregar_usuarios()
      cont=0
      for usuario in usuarios:
          cont+=1
          if  email==usuario['email']  and senha==usuario['senha'] :
              return redirect(url_for('buscar_usuarios'))
          
          elif email==usuario['email']  and senha!=usuario['senha'] or email!=usuario['email']  and senha==usuario['senha']:
              flash("Usuário ou senha inválidos","error")
              return render_template("login.html" )
      
      return render_template("login.html" )       

if __name__=='__main__':#inicia em modo desenvolvedor 
  app.run(debug=True)