from flask import render_template

from web import app
from web.db_handler import get_chronicles, get_heroes


@app.route("/", methods=["GET"])
@app.route('/index', methods=["GET"])
def main_route():
    heroes = get_heroes()
    chronicles = get_chronicles()
    return render_template("main.html", heroes=heroes, chronicles=chronicles)
