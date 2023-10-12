from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash
from book_app import db, login_manager
from models import User


login = Blueprint('login', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login.route('/login_reader', methods=['POST', 'GET'])
def login_reader():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('reader.reader_account'))
        else:
            flash("Неверный логин или пароль", category='error')
            return redirect(url_for('.login_reader'))
    
    return render_template('login/login_reader.html')


@login.route('/login_employee', methods=['POST', 'GET'])
def login_employee():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        if "@corp.ru" not in login:
            flash("Неверный логин или пароль", category='error')
            return redirect(url_for('.login_employee'))
        else:
            user = User.query.filter_by(login=login).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('employee.employee_account'))
            else:
                flash("Неверный логин или пароль", category='error')
                return redirect(url_for('.login_employee'))
    
    return render_template('login/login_employee.html')


@login.route('/register_reader', methods=['POST', 'GET'])
def register_reader():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == "POST":
        if password != password2:
            flash("Пароли не совпадают", category='error')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('.login_reader'))
    else:
        return render_template('login/register_reader.html')