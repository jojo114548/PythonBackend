from flask import Flask,request,jsonify,render_template,url_for,redirect,flash,session
import json ,os,uuid,bcrypt

app=Flask(__name__)

app.config['SECRET_KEY'] = "JOJO55555" # Configuração da chave secreta

class Usuario:
    def __init__(self, nome, cpf, email, idade, senha, perfil,id=None):
        # Construtor: cria o objeto já com seus atributos
        self.id = id or str(uuid.uuid4())  # Se não for passado, gera um ID único
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.idade = idade
        self.senha = bcrypt.hashpw(senha.encode('utf-8'),bcrypt.gensalt()).decode("utf-8")
        self.perfil=perfil


    def to_dict(self):
        """
        Transforma o objeto em dicionário.
        Esse método é necessário para salvar no JSON,
        já que JSON trabalha com dicionários/listas.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "idade": self.idade,
            "senha": self.senha,
             "perfil":self.perfil
            
        }


class UsuarioRepository:
    ARQUIVO = "usuarios.json"

    @classmethod #decorator que transforma um método para receber a classe (cls) como primeiro parâmetro, sem instanciar um objeto
    def carregar(cls):
        """Carrega lista de usuários do arquivo JSON (READ)."""
        if os.path.exists(cls.ARQUIVO):
            with open(cls.ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    @classmethod
    def salvar(cls, usuarios):
        """Salva a lista de usuários no arquivo JSON (UPDATE/WRITE)."""
        with open(cls.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4)

    @classmethod
    def adicionar(cls, usuario: Usuario):
        """Adiciona um novo usuário (CREATE)."""
        usuarios = cls.carregar()
        usuarios.append(usuario.to_dict())  # Converte objeto → dicionário
        cls.salvar(usuarios)

    @classmethod
    def deletar(cls, id):
            """Remove um usuário pelo ID (DELETE)."""
            usuarios = cls.carregar()
            filtrados = [u for u in usuarios if u["id"] != id]

            if len(usuarios) == len(filtrados):
                return False  # Nenhum usuário encontrado

            cls.salvar(filtrados)
            return True
    @classmethod
    def atualizar_usuario(cls,id, novos_dados):
      usuarios =cls.carregar()
      for usuario in usuarios:
              if usuario["id"] ==id:
                  usuario.update(novos_dados)  # atualiza os campos
                  cls.salvar(usuarios)
                  return True
      return False
    @classmethod
    def buscar_por_email(cls,email):
        usuarios=cls.carregar()
        for usuario in usuarios:
            if usuario["email"]==email:
                return usuario
        return None

@app.route("/") #caminho
def home():
   return render_template("index.html") 
@app.route("/cadastro-usuarios", methods=["GET"])
def cadastrar_usuario_get():
    return render_template("cadastrar-usuarios.html")

@app.route("/cadastro-usuarios", methods=["POST"])
def cadastrar_usuario_post():

   if request.method == "POST":
        usuario = Usuario(
            nome=request.form.get("nome"),
            cpf=request.form.get("cpf"),
            email=request.form.get("email"),
            idade=request.form.get("idade"),
            senha=request.form.get("senha"),
            perfil=request.form.get("perfil")
        )
        UsuarioRepository.adicionar(usuario)
        mensagem= f"Usuário {usuario.nome} cadastrado com sucesso!"
        return render_template("cadastrar-usuarios.html",mensagem=mensagem)


    
@app.route("/usuarios")
def buscar_usuarios():

     usuarios = UsuarioRepository.carregar()
     if not session:
            return "uSUARIO NÃO FEZ LOGIN" ,400
     
     return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/<id>",methods=["DELETE"])
def excluir_usuario(id):
      
      if not session:
        return "uSUARIO NÃO FEZ LOGIN" ,400
      if session["perfil"]!="admin":
        return "Acesso negado.Area de Administração"
      
      if UsuarioRepository.deletar(id):
            return jsonify({"mensagem": "Usuário deletado com sucesso."}), 200
      return jsonify({"erro": "Usuário não encontrado."}), 404
    

@app.route("/usuarios/json", methods=["GET"])
def buscar_usuarios_json():
    if not session:
        return "uSUARIO NÃO FEZ LOGIN" ,400
    if session["perfil"]!="admin":
        return "Acesso negado.Area de Administração"
    
    return jsonify(UsuarioRepository.carregar())



@app.route('/usuarios/<id>',methods=["PUT"])
def editar_usuario(id):

    if not session:
        return "uSUARIO NÃO FEZ LOGIN" ,400
    if session["perfil"]!="admin":
        return "Acesso negado.Area de Administração"
    novos_dados = request.get_json()
    if UsuarioRepository.atualizar_usuario(id,novos_dados):
        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200
    return jsonify({"erro": "Não foi possível salvar as modificações"}), 404


    
@app.route('/usuarios_nome/',methods=["GET"])
def usuario_nome():
    nome = request.args.get("nome") 
    usuarios =UsuarioRepository.carregar()

    if not session:
        return "uSUARIO NÃO FEZ LOGIN" ,400

    
    return render_template("usuarios_nome.html",nome=nome,usuarios=usuarios)


@app.route("/login")
def login_get():
    return render_template("login.html")

@app.route('/login', methods=["POST"] )   
def login_post():
      

      email = request.form.get("email")
      senha = request.form.get("senha")


      usuario = UsuarioRepository.buscar_por_email(email)

      if usuario and bcrypt.checkpw(senha.encode("utf-8"),usuario["senha"].encode("utf-8")):
          
          session["id_usuario"]=usuario["id"]
          session["perfil"]=usuario["perfil"]

          return f"login realizado com sucesso! Bem vindo(a),{usuario['nome']}."
          
       
      mensagem= f"E-mail ou senha inválidos!"
      return render_template("login.html",mensagem=mensagem),401
      
   
  
      
@app.route("/logout")
def logout():
 if not session:
     return"O usuario não fez login"
 session.clear()   
 return "usuario deslogado"

@app.route("/admin")
def admin_area():
    if "id_usuario" not in session or session.get("perfil") != "admin":
        return redirect(url_for("login_get"))
    return "Bem vindo administrador !"
if __name__=='__main__':#inicia em modo desenvolvedor 
  app.run(host='0.0.0.0',debug=False)
