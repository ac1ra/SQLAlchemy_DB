from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

conn = sqlite3.connect('instance/db_catalog.db')
cursor = conn.cursor()
json_file = 'books_catalog.json'


class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    name_genre = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Genre {self.name_genre}>"


class Subgenre(db.Model):
    __tablename__ = 'subgenre'
    name_subgenre_id = db.Column(db.Integer, primary_key=True, nullable=True)
    name_subgenre = db.Column(db.String(120), nullable=False)
    genre_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Subgenre {self.name_subgenre}>"


class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, unique=True,
                        primary_key=True, nullable=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer)
    genre = db.Column(db.String(120), nullable=False)
    cover = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Book Title {self.title}>"


with app.app_context():
    db.create_all()


def insert_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            for item in data:
                print(item['title'], type(item['title']))
                cursor.execute('''
                INSERT OR IGNORE INTO book(book_id,title,author,price,genre,cover,description,rating,year) VALUES(?,?,?,?,?,?,?,?,?)''', (item['id'], item['title'], item['author'], item['price'], item['genre'], item['cover'], item['description'], item['rating'], item['year']))
            conn.commit()
            conn.close()
        except json.JSONDecodeError as e:
            print(f"Error JSON:{e}")


@app.route('/')
def index():
    genres = Genre.query.all()
    return render_template('index.html', genres=genres)


@app.route('/info/<int:id>')
def info(id):
    subgenres = Subgenre.query.filter_by(genre_id=id)
    return render_template('info.html', subgenres=subgenres)


@app.route('/book/<string:genre_name>')
def book(genre_name):
    books = Book.query.filter_by(genre=genre_name)
    return render_template('book.html', books=books)


if __name__ == "__main__":
    insert_data(json_file)
    app.run(debug=True)
