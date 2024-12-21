import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from app.crud import cards
from app.config.database import SessionLocal
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
            error = 'Город отправления должен быть обязательным.'
        elif not finish_city:
            error = 'Город прибытия должен быть обязательным.'
        elif not time:
            error = 'Необходимо выбрать дату.'
        elif money is not None:
            if money > 3000000 or money < 0:
                error = 'Таких дорогих билетов у нас нет :('
        elif start_city == finish_city:
            error = 'Город отправления и город назначения не могут быть одинаковыми.'

        if error is None:
            time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
            if time < datetime.date.today():
                error = 'Вы не можете улететь в прошлое.'

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
                print(f"Ошибка добавления карточки: {str(e)}")
                flash(f"Ошибка добавления карточки: {str(e)}", 'error')

            return redirect(url_for('main.index'))

        flash(error)
    return render_template('add_card.html')


@cards_bp.route('/delete_card', methods=['POST'])
def delete_card():
    card_id = request.form.get('card_id')
    cards.delete_card(db, int(card_id))
    return redirect(url_for('main.index'))