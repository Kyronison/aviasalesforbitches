from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

from app.crud.users import create_user, authenticate_user
from app.database import SessionLocal
from app.schemas import UserCreate

auth_bp = Blueprint("auth", __name__)


class RegistrationForm(FlaskForm):
    login = StringField(validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField(validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Регистрация')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


db = SessionLocal()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = authenticate_user(db, username, password)
            print("Аутентификация успешна. Пользователь:", user)
            session.clear()
            session['login'] = username
            return redirect(url_for('main_pages.logged'))
        except ValueError as e:
            print(f"Ошибка аутентификации: {e}")
            flash(f"Ошибка аутентификации: {e}", 'error')
    return render_template('login.html', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.login.data
        password = form.password.data # Хэшируем пароль
        try:
            new_user = UserCreate(login=username, password=password)
            user = create_user(db, new_user)
            print("Регистрация успешна. Пользователь:", user)
            session.clear()
            session['login'] = username
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            print(f"Ошибка регистрации: {e}")

            flash(f"Ошибка регистрации: {e}", 'error')
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.logged'))