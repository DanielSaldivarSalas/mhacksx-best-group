from app import app, db
from flask import render_template, redirect, url_for, session
from forms import LoginForm, RegisterForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from coinbase.wallet.client import Client

import config
import datetime
import requests
import json

client = Client(config.CB_API_KEY, config.CB_API_SECRET, api_version='2017-09-22')

login_manager = LoginManager()
login_manager.init_app(app)
BITCOIN_ENDPOINT = 'https://api.gdax.com'
login_manager.login_view = 'login'
currency_code = 'USD'
accuracy = 5
digital_type ='BTC-USD'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #Check if the form is submitted,
    if form.validate_on_submit():
        #usernames are unique so it's okay to return the first query we find
        user = User.query.filter_by(username=form.username.data).first()

        # if user exists
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<p>{}</p><p>{}</p>'.format(form.username.data,
        #                                   form.password.data)

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()

    #Check if the form is submited
    if form.validate_on_submit():

        #shaw256 generates a password that's 80 characters long, models should reflect that
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        #we're passing the data without hashing for testing purposes
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
        #return '<p>{}</p><p>{}</p><p>{}</p><h1>'.format(form.email.data, form.username.data, form.password.data)


    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    price = client.get_spot_price(currency=currency_code)
    data = requests.get(BITCOIN_ENDPOINT + '/products/' + digital_type + '/stats').text
    r = json.loads(data)
    return render_template('dashboard.html',
                            name=current_user.username,
                            bitcoin_val = str(price.amount),
                            dollar_val = str(round(1/float(price.amount),accuracy)),
                            timestamp = datetime.datetime.now(),
                            stats_open = str(round(float(r['open']),2)),
                            stats_high = str(round(float(r['high']),2)),
                            stats_low = str(round(float(r['low']),2)),
                            stats_volume = str(round(float(r['volume']),2)))

@app.route('/bitgame')
@login_required
def bitgame():
    print(current_user.id)
    user= User.query.filter_by(username=current_user.username).first_or_404()
    print(user)
    profiles = profileinfo.query.all()
    return render_template('bitgame.html', name=current_user.username)
