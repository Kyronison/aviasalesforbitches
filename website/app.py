from flask import Flask, session, redirect, url_for, render_template
import main

app = Flask(__name__)
app.config.update(
    SECRET_KEY='pGy5lNdVGMf6pGy5lNdVGMf6'
)

# Регистрируем маршруты из другого модуля
app.register_blueprint(main.mn)


@app.route('/')  # лавная страница
def index():
    if "login" in session:
        return render_template('main.html', username=session['login'])
    else:
        return redirect(url_for('main_pages.login'))


if __name__ == "__main__":
    app.run(debug=True)
