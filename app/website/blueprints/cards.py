from flask import Blueprint, render_template, request, flash, redirect, url_for

cards_bp = Blueprint("cards", __name__)

@cards_bp.route('/addcard', methods=['GET', 'POST'])
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
            return redirect(url_for('main.index'))

        flash(error)
    return render_template('add_card.html')