from book_app import app


from book_app.login.login import login
app.register_blueprint(login)


from book_app.main.main import main
app.register_blueprint(main)


from book_app.employee.employee import employee
app.register_blueprint(employee)


from book_app.reader.reader import reader
app.register_blueprint(reader)


if __name__ == "__main__":
    app.run(debug=True)