"""Точка запуску Flask та фабрика додатка."""

from flask import Flask, render_template, request

if __package__:
    from .api import api
    from .config import config_by_name
else:
    from api import api
    from config import config_by_name


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name]())
    register_routes(app)
    app.register_blueprint(api)
    return app


def register_routes(app: Flask):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/greet")
    @app.route("/greet/<name>")
    def greet(name=None):
        # Параметр шляху має пріоритет над параметром запиту.
        if name is None:
            name = request.args.get("name", "Гість")
        return render_template("greet.html", name=name.strip() or "Гість")


if __name__ == "__main__":
    application = create_app("development")
    application.run(host="127.0.0.1", port=5000)
