"""Blueprint з маршрутом JSON API."""

from importlib.metadata import version

from flask import Blueprint, current_app, jsonify

api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/info")
def info():
    return jsonify(
        framework="Flask",
        version=version("flask"),
        debug=current_app.debug,
        routes=sorted(rule.rule for rule in current_app.url_map.iter_rules()),
    )
