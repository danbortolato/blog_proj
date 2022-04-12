import datetime

from flask import Flask, render_template, request
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    client = MongoClient(
        "mongodb://localhost:27017")
    app.db = client.projetoblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            format_data = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.dados.insert_one(
                {"content": entry_content, "date": format_data})

        data_dado = [
            (
                dado["content"],
                dado["date"],
                datetime.datetime.strptime(
                    dado["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for dado in app.db.dados.find({})
        ]
        return render_template("home.html", dados=data_dado)
    return app
