from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user
from book_app import db
from models import Book


employee = Blueprint('employee', __name__, template_folder='templates', url_prefix='/employee')


@employee.route('/add_book', methods=['POST', 'GET'])
@login_required
def add_book():
    if request.method == "POST":
        name = request.form['name']
        author = request.form['author']
        year = request.form['year']
        count = request.form['count']
        try:
            cur_book = Book.query.filter_by(name=name, author=author, year=year).first()
            if cur_book is None:
                book = Book(name=name, author=author, year=year, count=count)
                db.session.add(book)
                db.session.commit()
                flash(f'''Книга "{name}" успешно добалена''', category='success')
            else:
                cur_book.count = int(cur_book.count) + int(count)
                db.session.commit()
                flash(f'''Количество экземпляров книги "{name}" увеличено на {count}''', category='success')
            return redirect(url_for('.add_book'))
        except:
            flash("Произошла ошибка при добавлении книги", category='error')
            return redirect(url_for('.add_book'))   
    else:
        return render_template('employee/add_book.html')


@employee.route('/delete_book', methods=['POST', 'GET'])
@login_required
def delete_book():
    if request.method == "POST":
        name = request.form['name']
        author = request.form['author']
        year = request.form['year']
        count = request.form['count']
        try:
            book = Book.query.filter_by(name=name, author=author, year=year).first_or_404()
            book.count = int(book.count) - min(int(count), int(book.count))
            if book.count == 0:
                db.session.delete(book)
                flash(f'''Книга "{name}" удалена''')
            else:
                flash(f'''Успешно списано {min(int(count), int(book.count))} экземпляра/(ов) книги "{book.name}"''', category='success')
            db.session.commit()
            return redirect(url_for('.delete_book'))
        except:
            flash("Произошла ошибка при списании книги", category='error')
            return redirect(url_for('.delete_book'))
    else:
        return render_template('employee/delete_book.html')


@employee.route('/')
@login_required
def employee_account():
    return render_template('employee/employee_account.html')


@employee.route('/logout_employee', methods=['POST', 'GET'])
@login_required
def logout_employee():
    logout_user()
    return redirect(url_for('main.index'))


@employee.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login.login_employee') + '?next=' + request.path)

    return response