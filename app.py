"""Ponto de entrada da aplicação Monitor de Plantas."""

import os

from flask import Flask, redirect, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from controllers.colaborador_controller import colaborador_bp
from controllers.planta_controller import planta_bp
from controllers.registro_controller import registro_bp
from controllers.alerta_controller import alerta_bp
from services.repositorio import carregar_plantas_do_colaborador

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.secret_key = "chave-secreta-dev"  # TODO: mover para variável de ambiente antes de produção
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_ENV") == "production"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.register_blueprint(colaborador_bp)
app.register_blueprint(planta_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(alerta_bp)


@app.context_processor
def injetar_contagem_alertas():
    """Injeta a contagem de alertas em todos os templates (RNF15)."""
    contagem = 0
    if "colaborador_id" in session:
        plantas = carregar_plantas_do_colaborador(session["colaborador_id"])
        contagem = sum(1 for p in plantas if p.precisa_cuidado())
    return {"contagem_alertas": contagem}


@app.route("/")
def index():
    """Redireciona a raiz para a página de login."""
    return redirect(url_for("colaborador.login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)