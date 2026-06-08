from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, User, Task
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "taskflow-secret-2024")

# PostgreSQL em produção, SQLite local
database_url = os.environ.get("DATABASE_URL", "sqlite:///taskflow.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Cria as tabelas no banco na primeira execução
with app.app_context():
    db.create_all()


# --- Decorator: protege rotas que exigem login ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# --- Injeta contador de alertas em todos os templates ---
@app.context_processor
def inject_alertas():
    if "user_id" in session:
        hoje = datetime.today().date()
        total_alertas = Task.query.filter(
            Task.user_id == session["user_id"],
            Task.prazo != None,
            Task.prazo <= hoje,
            Task.status != "concluida"
        ).count()
        return {"total_alertas": total_alertas}
    return {"total_alertas": 0}


# --- Login ---
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = User.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session["user_id"] = usuario.id
            session["user_nome"] = usuario.nome
            return redirect(url_for("dashboard"))
        else:
            flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html")


# --- Cadastro ---
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nome  = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "warning")
            return render_template("cadastro.html")

        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "danger")
            return render_template("cadastro.html")

        novo_usuario = User(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha)
        )
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


# --- Logout ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# --- Dashboard ---
@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    total      = Task.query.filter_by(user_id=user_id).count()
    pendentes  = Task.query.filter_by(user_id=user_id, status="pendente").count()
    andamento  = Task.query.filter_by(user_id=user_id, status="em_andamento").count()
    concluidas = Task.query.filter_by(user_id=user_id, status="concluida").count()

    return render_template("dashboard.html",
        total=total,
        pendentes=pendentes,
        andamento=andamento,
        concluidas=concluidas
    )


# --- Lista de tarefas ---
@app.route("/tarefas")
@login_required
def tarefas():
    user_id    = session["user_id"]
    filtro     = request.args.get("filtro", "todas")
    prioridade = request.args.get("prioridade", "todas")
    ordem      = request.args.get("ordem", "recente")
    busca      = request.args.get("busca", "").strip()
    categoria  = request.args.get("categoria", "todas")

    query = Task.query.filter_by(user_id=user_id)

    if filtro != "todas":
        query = query.filter_by(status=filtro)

    if prioridade != "todas":
        query = query.filter_by(prioridade=prioridade)

    if categoria != "todas":
        query = query.filter_by(categoria=categoria)

    if busca:
        query = query.filter(Task.titulo.ilike(f"%{busca}%"))

    if ordem == "prazo":
        query = query.order_by(Task.prazo.asc().nullslast())
    elif ordem == "prioridade":
        prioridade_ordem = {"alta": 1, "media": 2, "baixa": 3}
        query = query.all()
        query = sorted(query, key=lambda t: prioridade_ordem.get(t.prioridade, 99))
        return render_template("tarefas.html", tarefas=query, filtro=filtro,
                               prioridade=prioridade, ordem=ordem, busca=busca,
                               categoria=categoria, today=datetime.today().date())
    else:
        query = query.order_by(Task.criado_em.desc())

    lista = query.all()
    return render_template("tarefas.html", tarefas=lista, filtro=filtro,
                           prioridade=prioridade, ordem=ordem, busca=busca,
                           categoria=categoria, today=datetime.today().date())


# --- Nova tarefa ---
@app.route("/nova-tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo     = request.form.get("titulo", "").strip()
        descricao  = request.form.get("descricao", "").strip()
        prioridade = request.form.get("prioridade", "media")
        categoria  = request.form.get("categoria", "geral")
        prazo_str  = request.form.get("prazo") or None
        prazo      = datetime.strptime(prazo_str, "%Y-%m-%d").date() if prazo_str else None

        if not titulo:
            flash("O título é obrigatório.", "warning")
            return render_template("nova_tarefa.html", today=datetime.today().strftime("%Y-%m-%d"))

        tarefa = Task(
            titulo=titulo,
            descricao=descricao if descricao else None,
            prioridade=prioridade,
            categoria=categoria,
            prazo=prazo,
            user_id=session["user_id"]
        )
        db.session.add(tarefa)
        db.session.commit()

        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("tarefas"))

    return render_template("nova_tarefa.html", today=datetime.today().strftime("%Y-%m-%d"))


# --- Atualizar status ---
@app.route("/tarefa/<int:id>/status", methods=["POST"])
@login_required
def atualizar_status(id):
    tarefa = Task.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()
    novo_status = request.form.get("status")

    if novo_status in ["pendente", "em_andamento", "concluida"]:
        tarefa.status = novo_status
        db.session.commit()

    return redirect(url_for("tarefas"))


# --- Deletar tarefa ---
@app.route("/tarefa/<int:id>/deletar", methods=["POST"])
@login_required
def deletar_tarefa(id):
    tarefa = Task.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()
    db.session.delete(tarefa)
    db.session.commit()
    flash("Tarefa removida.", "success")
    return redirect(url_for("tarefas"))


# --- Limpar prazo ---
@app.route("/tarefa/<int:id>/limpar-prazo", methods=["POST"])
@login_required
def limpar_prazo(id):
    tarefa = Task.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()
    tarefa.prazo = None
    db.session.commit()
    flash("Prazo removido.", "success")
    return redirect(url_for("editar_tarefa", id=id))


# --- Editar tarefa ---
@app.route("/tarefa/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_tarefa(id):
    tarefa = Task.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()
    today  = datetime.today().strftime("%Y-%m-%d")

    if request.method == "POST":
        titulo    = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        prioridade = request.form.get("prioridade", "media")
        prazo_str  = request.form.get("prazo") or None

        if not titulo:
            flash("O título é obrigatório.", "warning")
            return render_template("editar_tarefa.html", tarefa=tarefa, today=today)

        tarefa.titulo     = titulo
        tarefa.descricao  = descricao if descricao else None
        tarefa.prioridade = prioridade
        tarefa.categoria  = request.form.get("categoria", "geral")
        tarefa.prazo      = datetime.strptime(prazo_str, "%Y-%m-%d").date() if prazo_str else None

        db.session.commit()
        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("tarefas"))

    return render_template("editar_tarefa.html", tarefa=tarefa, today=today)


if __name__ == "__main__":
    app.run(debug=True)