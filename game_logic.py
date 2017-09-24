import datetime
from models import *
from coinbase.wallet.client import Client

currency_code = 'USD'  # can also use EUR, CAD, etc.


todays_date = str(datetime.datetime.now())[:10]


def start_game(time):
    game = Gameinfo.query.all()
    if not game:
        newgame = Gameinfo(round_time= time)
        db.session.add(newgame)
        db.session.commit()


def join_game(user_id):
    current_round = Gameinfo.query.order_by("id").first().id
    newgameplayer = Gameplayer(r_id = current_round,
                                u_id = user_id)

    db.session.add(newgameplayer)
    db.session.commit()



def buy_bitcoin(amount,client, user_id):
    bit_price = get_bitcoin_price(client)
    bitcoin_diff = float(amount) / float(bit_price)
    usd_diff = (amount)*-1

    #current_round = Gameinfo.query.order_by("id").first()
    current_round = 1
    new_transaction = Usergametransactions(game_round_id = current_round,
                                            amount = amount,
                                            user_id = user_id,
                                            bitcoin_price = bit_price,
                                            transaction_time = datetime.datetime.now(),
                                            transaction_type = True)  #True means buy
    db.session.add(new_transaction)
    db.session.commit()

    #Update the balance in the User Model
    balance = User.query.filter_by(id = user_id).first()
    balance.game_bit_balance += bitcoin_diff
    balance.game_usd_balance += usd_diff
    db.session.commit()

#amount measured by bitcoin
def sell_bitcoin(amount,client,user_id):
    bit_price = get_bitcoin_price(client)
    bitcoin_diff = amount * -1
    usd_diff = amount * bit_price

    #current_round = Gameinfo.query.order_by("id").first()
    current_round = 1
    new_transaction = Usergametransactions(game_round_id = current_round,
                                            amount = amount,
                                            user_id = user_id,
                                            bitcoin_price = bit_price,
                                            transaction_time = datetime.datetime.now(),
                                            transaction_type = False)  #False means sell
    db.session.add(new_transaction)
    db.session.commit()

    #Update the balance in the User Model
    balance = User.query.filter_by(id = user_id).first()
    balance.game_bit_balance += bitcoin_diff
    balance.game_usd_balance += usd_diff
    db.session.commit()

def get_bitcoin_price(client):
    """
    Input: None
    return type: float
    """
    todays_date = str(datetime.datetime.now())[:10]
    #client = Client(config.CB_API_KEY, config.CB_API_SECRET, api_version= todays_date)


    current_bitcoin_price = client.get_spot_price(currency=currency_code)
    current_bitcoin_price = dict(current_bitcoin_price)



    return float(current_bitcoin_price['amount'])

def get_leaderboard(round_id,client):
    #out put a list of Users
    player_ranks = []
    players = Gameplayer.query.filter_by(r_id = round_id)
    for x in players:
        player_ranks.append({get_total_balance(x.u_id,client), x.u_id})
    player_ranks.sort(reverse = True)
    print(player_ranks)
    return player_ranks



def get_total_balance(user_id,client):
    currUser = User.query.filter_by(id = user_id).first()
    balance = currUser.game_usd_balance + currUser.game_bit_balance * get_bitcoin_price(client)
    return balance
