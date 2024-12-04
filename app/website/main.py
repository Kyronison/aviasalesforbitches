from flask import Blueprint, render_template, session, flash, request, redirect, url_for

from flask import Blueprint, redirect, session
from app.database import SessionLocal
from app.crud.users import create_user
from app.crud.users import authenticate_user
from app import schemas
mn = Blueprint("main_pages", __name__)
db = SessionLocal()


@mn.route('/logged')
def logged():
    # получаем информацию о пользователе по логину в сессии
    if not ("login" in session):
        return redirect(url_for('main_pages.login'))
    else:
        return redirect(url_for('index'))


@mn.route('/telegram')
def telegram():
    user = {"login": session['login']}
    bot_username = "AForBitches_bot"
    bot_link = f"https://t.me/{bot_username}?start={user['login']}"
    return render_template('connect_telegram.html', bot_link=bot_link)


@mn.route('/login', methods=('GET', 'POST'))
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


@mn.route('/signup', methods=('GET', 'POST'))
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

            return redirect(url_for('main_pages.telegram'))

        except ValueError as e:
            print(f"Ошибка регистрации: {e}")
            return render_template('register.html')

    return render_template('register.html')


@mn.route('/addcard', methods=('GET', 'POST'))
def add_card():  # получаем все, все, все данные :)
    if request.method == 'POST':
        start_city = str(request.form['scity'])
        finish_city = str(request.form['fcity'])
        time = str(request.form['date'])
        money = str(request.form['sum'])
        print(start_city, finish_city, time, money)
        error = None

        if not start_city:
            error = 'Start city is required.'
        elif not finish_city:
            error = 'Finish city is required.'
        elif not time:
            error = 'Time city is required.'
        elif not money:
            error = 'Money city is required.'

        if error is None:
            return redirect(url_for('index'))

        flash(error)
    return render_template('add_card.html')


@mn.route('/logout')  # чистим сессию и переходим на страницу без регистрации
def logout():
    session.clear()
    return redirect(url_for('main_pages.logged'))
