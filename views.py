from teste import app,render_template

#rotas
@app.route("/formulario.html")#caminho
def home():#funçao para carregar as informações que vão aparecer na rota ou caminho 
    return render_template("formulario.html")

#rotas
@app.route("/blog.html")#caminho
def blog():#funçao para carregar as informações que vão aparecer na rota ou caminho 
    return render_template("blog.html")