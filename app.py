"""Ponto de entrada da aplicação Monitor de Plantas."""

from flask import Flask, redirect, url_for

from controllers.colaborador_controller import colaborador_bp
from controllers.planta_controller import planta_bp
from controllers.registro_controller import registro_bp
from controllers.alerta_controller import alerta_bp

app = Flask(__name__)
app.secret_key = "chave-secreta-dev"  # TODO: mover para variável de ambiente antes de produção

app.register_blueprint(colaborador_bp)
app.register_blueprint(planta_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(alerta_bp)


@app.route("/")
def index():
    """Redireciona a raiz para a página de login."""
    return redirect(url_for("colaborador.login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)