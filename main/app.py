from dataclasses import dataclass
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
import requests

# from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:test@db:5432/adv_lnd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
CORS(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# @dataclass
# class ProductUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     product_id = db.Column(db.Integer)

#     UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@dataclass
class Bank(db.Model):
    __tablename__ = 'bank'
    id: int
    bank: str

    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.Text())


@dataclass
class BankSlot(db.Model):
    __tablename__ = 'bank_slot'
    id: int
    bank_id: str
    items: str

    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.String(8))
    items = db.Column(db.Text())


@dataclass
class Item(db.Model):
    __tablename__ = 'item'
    id: int
    name: str
    price: int
    quantity: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    location = db.Column(db.String(128))
    quantity = db.Column(db.Integer, nullable=True)


@app.route('/api/bank/wipe')
def wipe():
    # for all records
    db.session.query(Bank).delete()
    db.session.commit()
    return jsonify({
        'message': 'wiped'
    })


@app.route('/api/bank', methods=['POST', 'GET'])
def get_or_post_bank():

    if request.method == 'GET':
        try:
            return jsonify(Bank.query.all())
        except:
            abort(400, 'Something went wrong in GET!')

    if request.method == 'POST':
        bank_data = request.json
        print(bank_data)
        for slot in bank_data:
            print(slot)
            teller = BankSlot(bank_id=str(slot), items=str(bank_data[slot]))
            try:
                db.session.add(teller)
                db.session.commit()
            except:
                abort(400, 'Something went wrong in bank teller POST!')

        bank = Bank(bank=str(bank_data))

        try:
            db.session.add(bank)
            db.session.commit()
        except:
            abort(400, 'Something went wrong in bank POST!')

        return jsonify({
            'message': 'bank post success'
        })


@app.route('/api/bank/latest', methods=['GET'])
def get_latest_bank():
    latest = Bank.query.order_by(Bank.id.desc()).first()
    return latest.bank


@app.route('/api/bank/<string:bank_id>', methods=['GET'])
def get_bank_teller(bank_id):

    teller = db.session.query(BankSlot).filter_by(
        bank_id=bank_id).order_by(BankSlot.id.desc()).first()
    if teller is None:
        abort(404, 'Teller not found')
    return jsonify(teller)


# @app.route('/api/bank/<int:id>', methods=['GET'])
# def get_bank_teller(id):
#     latest = Bank.query.order_by(Bank.id.desc()).first()
#     # bank = Bank.query.get(0)
#     if latest is None:
#         abort(404, 'Bank not found')
#     return latest[id]


# @app.route('/api/bank/<int:id>', methods=['GET'])
# def bank_by_id(id):
#     return jsonify(Bank.query.get(id))


# @app.route('/api/products/<int:id>/like', methods=['POST'])
# def like(id):
#     req = requests.get('http://docker.for.mac.localhost:8000/api/user')
#     json = req.json()

#     try:
#         productUser = ProductUser(user_id=json['id'], product_id=id)
#         db.session.add(productUser)
#         db.session.commit()

#         publish('product_liked', id)
#     except:
#         abort(400, 'You already liked this product')

#     return jsonify({
#         'message': 'success'
#     })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
