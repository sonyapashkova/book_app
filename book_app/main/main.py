from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Book

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/find_book', methods=['POST', 'GET'])
def find_book():
    if request.method == "POST":
        name = request.form['name']
        author = request.form['author']
        year = request.form['year']
        try:
            if len(name) != 0 and len(author) == 0 and len(year) == 0:
                books = Book.query.filter_by(name=name).all()
            elif len(name) == 0 and len(author) != 0 and len(year) == 0:
                books = Book.query.filter_by(author=author).all()
            elif len(name) == 0 and len(author) == 0 and len(year) != 0:
                books = Book.query.filter_by(year=year).all()
            elif len(name) != 0 and len(author) != 0 and len(year) == 0:
                books = Book.query.filter_by(name=name, author=author).all()
            elif len(name) != 0 and len(author) == 0 and len(year) != 0:
                books = Book.query.filter_by(name=name, year=year).all()
            elif len(name) == 0 and len(author) != 0 and len(year) != 0:
                books = Book.query.filter_by(author=author, year=year).all()
            elif len(name) != 0 and len(author) != 0 and len(year) != 0:
                books = Book.query.filter_by(name=name, author=author, year=year).all()
            if len(books) == 0:
                flash("Книга/(и) с заданными аттрибутами отсутствует/(ют)", category='error')
            return render_template('main/find_book.html', books=books)
        except:
            return redirect(url_for('.find_book'))
    else:
        return render_template('main/find_book.html')