from flask import Blueprint, render_template, session, redirect, url_for

from app.crud.cards import get_cards_by_user_login
from app.database import SessionLocal

main_bp = Blueprint("main", __name__)
db = SessionLocal()


@main_bp.route('/logged')
def logged():
    # получаем информацию о пользователе по логину в сессии
    if not ("login" in session):
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.index'))


@main_bp.route('/telegram')
def telegram():
    user = {"login": session['login']}
    bot_username = "AForBitches_bot"
    bot_link = f"https://t.me/{bot_username}?start={user['login']}"
    return render_template('connect_telegram.html', bot_link=bot_link)


@main_bp.route('/')
def index():
    if "login" in session:
        # cards = get_cards_by_user_login(db, session['login'])
        cards = []
        return render_template('main.html', username=session['login'], cards=cards)
    else:
        return redirect(url_for('auth.login'))


