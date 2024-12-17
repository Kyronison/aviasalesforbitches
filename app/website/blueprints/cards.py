import datetime
from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from app.crud import cards
from app.database import SessionLocal
from app.schemas import CardCreate, CityCode

cards_bp = Blueprint("cards", __name__)
db = SessionLocal()


@cards_bp.route('/addcard', methods=['GET', 'POST'])
def add_card():  # получаем все, все, все данные :)
    if request.method == 'POST':
        start_city = str(request.form['scity'])
        finish_city = str(request.form['fcity'])
        time = request.form['date']
        if str(request.form['sum']) == "":
            money = None
        else:
            money = int(request.form['sum'])

        error = None

        if not start_city:
            error = 'Start city is required.'
        elif not finish_city:
            error = 'Finish city is required.'
        elif not time:
            error = 'Date is required.'
        elif money > 3000000 or money < 0:
            error = 'We do not have tickets with such cost'
        elif start_city == finish_city:
            error = 'Cities can not be same'

        if error is None:
            time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
            if time < datetime.date.today():
                error = 'You can not fly into the past'

        if error is None:
            try:
                card_data = CardCreate(
                    user_login=session['login'],
                    origin=CityCode(code=start_city),
                    destination=CityCode(code=finish_city),
                    flight_date=time,
                    price_threshold=money
                )

                new_card = cards.create_card(db, card_data)
                return redirect(url_for('main.logged'))
            except ValueError as e:
                print(f"Ошибка добавления карточки: {e}")
                flash(f"Ошибка добавления карточки: {e}", 'error')

            return redirect(url_for('main.index'))

        flash(error)
    return render_template('add_card.html')


@cards_bp.route('/delete_card', methods=['POST'])
def delete_card():
    card_id = request.form.get('card_id')
    cards.delete_card(db, int(card_id))
    return redirect(url_for('main.index'))