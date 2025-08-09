from flask import Flask, render_template

app = Flask(__name__)

#rotas
@app.route("/")#caminho
@app.route("/formulario")#caminho
def  formulario():#funçao para carregar as informações que vão aparecer na rota ou caminho 
    return render_template("formulario.html")
@app.route("/blog")#caminho
def blog():#funçao para carregar as informações que vão aparecer na rota ou caminho 
    return render_template("blog.html")

if __name__ == '__main__': #executa esse codigo abaixo quando estiver executando essa rota
    app.run(debug=True)#rodar o site 