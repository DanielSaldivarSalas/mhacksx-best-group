from app import app, db
from flask import render_template, redirect, url_for, session
from forms import LoginForm, RegisterForm
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from coinbase.wallet.client import Client
from game_logic import *

import pandas as pd
import numpy as np
import plotly
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
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    graphs = [
        dict(
            data=[
                dict(
                    x=[1, 2, 3],
                    y=[10, 20, 30],
                    type='scatter'
                ),
            ],
            layout=dict(
                title='first graph'
            )
        ),

        dict(
            data=[
                dict(
                    x=[1, 3, 5],
                    y=[10, 50, 30],
                    type='bar'
                ),
            ],
            layout=dict(
                title='second graph'
            )
        ),

        dict(
            data=[
                dict(
                    x=ts.index,  # Can use the pandas data structures directly
                    y=ts
                )
            ]
        )
    ]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',ids=ids,
                           graphJSON=graphJSON)

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
                        password=hashed_password,
                        pic_url =form.pic_url.data,
                        game_bit_balance = 0.00,
                        game_usd_balance = 100.00)

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
    start_game(datetime.datetime.now())
    bit_balance = User.query.filter_by(id = current_user.id).first().game_bit_balance
    usd_balance = User.query.filter_by(id = current_user.id).first().game_usd_balance
    return render_template('bitgame.html', bit_bal = bit_balance,
                                        usd_val = usd_balance,
                                        name = current_user.username)

@app.route('/bitgame/join')
@login_required
def join():
    player = Gameplayer.query.filter_by(id = current_user.id).first()
    if not player:
        join_game(current_user.id)
    bit_balance = User.query.filter_by(id = current_user.id).first().game_bit_balance
    usd_balance = User.query.filter_by(id = current_user.id).first().game_usd_balance

    return redirect(url_for('bitgame'), bit_bal = bit_balance,
                                        usd_val = usd_balance,
                                        name = current_user.username)
