from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app import schemas
from app.database import SessionLocal
from app.crud.users import create_user, authenticate_user
from app.schemas import UserCreate

auth_bp = Blueprint("auth", __name__)
db = SessionLocal()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            return render_template('login.html')
        elif not password:
            return render_template('login.html')

        try:
            user = authenticate_user(db, username, password)
            print("Аутентификация успешна. Пользователь:", user)

            session.clear()
            session['login'] = username

            return redirect(url_for('main_pages.logged'))

        except ValueError as e:
            print(f"Ошибка аутентификации: {e}")
            return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():  # получаем все, все, все данные :)
    if request.method == 'POST':
        username = str(request.form['login'])
        password = str(request.form['password'])

        if not username:
            return render_template('register.html')
        elif not password:
            return render_template('register.html')

        try:
            new_user = schemas.UserCreate(
                login=username,
                password=password,
            )
            user = create_user(db, new_user)
            print("Регистрация успешна. Пользователь:", user)

            session.clear()
            session['login'] = username

            return redirect(url_for('main.telegram'))

        except ValueError as e:
            print(f"Ошибка регистрации: {e}")
            return render_template('register.html')

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.logged'))
