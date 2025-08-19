from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name_genre = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Genre {self.name_genre}>"


class Subgenre(db.Model):
    name_subgenre_id = db.Column(db.Integer, primary_key=True, nullable=True)
    name_subgenre = db.Column(db.String(120), nullable=False)
    genre_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Subgenre {self.name_subgenre}>"


@app.route('/')
def index():
    genres = Genre.query.all()
    return render_template('index.html', genres=genres)


@app.route('/info/<int:id>')
def info(id):
    subgenres = Subgenre.query.filter_by(genre_id=id)
    return render_template('info.html', subgenres=subgenres)


# @app.route('/book/')
# def info(id):
#     subgenres = Subgenre.query.filter_by(genre_id=id)
#     return render_template('book.html', subgenres=subgenres)


if __name__ == "__main__":
    app.run(debug=True)
