from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, logout_user, login_required
import redis
import random

app = Flask(__name__)
app.secret_key = 'Wat3rH0me1nc'
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = "login"
login_manager.login_message = "R.E.T.A.W secret key required"

r = redis.StrictRedis()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
def index():
    names = r.lrange('restaurants', 0, -1)
    if names is None:
        return 'No restaurants are set up. visit /config to add more restaurants.'
    else:
        return random.choice(names)


@app.route('/login', methods=['POST'])
def login():
    if auth_admin(request.form['username'], request.form['password']):
        session['admin'] = True
    else:
        flash('Nope.')
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/config')
@login_required
def admin_config():
    return 'Welcome to R.E.T.A.W'


@login_manager.request_loader
def auth_admin(request):
    username = request.form['username']
    password = request.form['password']
    return username == 'retaw' and password == 'Wat3rH0me1nc'


if __name__ == '__main__':
    app.run(port=8080, debug=True)
