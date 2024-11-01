from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,
"bookdatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Movie(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def __repr__(self):
        return "<Title: {}>".format(self.name)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            name = Movie(name=request.form.get("title"))
            db.session.add(name)
            db.session.commit()
        except Exception as e:
            print("Failed to add movie")
            print(e)
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        movie = Movie.query.filter_by(name=oldtitle).first()
        if movie:
            movie.name = newtitle
            db.session.commit()
        else:
            print("Filme não encontrado")
    except Exception as e:
        print("Não foi possível atualizar o nome do filme")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    movie = Movie.query.filter_by(name=title).first()
    if movie:
        db.session.delete(movie)
        db.session.commit()
    else:
        print("Filme não encontrado")
    return redirect("/")



@app.route('/listar_filmes')
def nova_pagina():
    movies = Movie.query.all()

    return render_template("listar_filmes.html", movies=movies)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
    
