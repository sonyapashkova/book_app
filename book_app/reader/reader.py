from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user
from book_app import db
from models import Book


reader = Blueprint('reader', __name__, template_folder='templates', url_prefix='/reader')


@reader.route('/book_book', methods=['POST', 'GET'])
@login_required
def book_book():
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
            return render_template('reader/book_book.html', books=books)
        except:
            return redirect(url_for('.book_book'))
    else:
        return render_template('reader/book_book.html')
    

@reader.route("/book_book/<int:id>", methods=['POST', 'GET'])
@login_required
def book_one_book(id):
    if request.method == "POST":
        try:
            book = Book.query.get_or_404(id)
            if book.count == 0:
                flash("Все экзепляры книги забронированы", category='error')
            else:
                book.count = int(book.count) - 1
                db.session.commit()
                flash(f'''Книга "{book.name}" успешно забронирована''', category='success')
            return redirect(url_for('.book_book'))
        except:
            flash("Произошла ошибка при бронировании книги", category='error')
            return redirect(url_for('.book_book'))
    else:
        return redirect(url_for('.book_book'))


@reader.route('/')
@login_required
def reader_account():
    return render_template('reader/reader_account.html')


@reader.route('/logout_reader', methods=['POST', 'GET'])
@login_required
def logout_reader():
    logout_user()
    return redirect(url_for('main.index'))


@reader.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login.login_reader') + '?next=' + request.path)

    return response