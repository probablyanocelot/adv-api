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
    data: str

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())


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


@dataclass
class BankTeller(db.Model):
    __tablename__ = 'bank_teller'
    id: str
    name: str
    items: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    items = db.Column(db.Text())


@app.route('/api/bank/wipe')
def wipe():
    # for all records
    db.session.query(Bank).delete()
    db.session.commit()
    return jsonify({
        'message': 'wiped'
    })


@app.route('/api/bank', methods=['POST', 'GET'])
def bank():

    if request.method == 'GET':
        try:
            return jsonify(Bank.query.all())
        except:
            abort(400, 'Something went wrong in GET!')

    if request.method == 'POST':
        # try:
        # print(request)
        data = request.json
        print(data)
        # if data.data:
        #     print(1)
        #     data = data.data
        #     print(2)
        print(3)
        bank = Bank(data=str(data))
        print(4)
        db.session.add(bank)
        print(5)
        db.session.commit()
        print(6)

        # except:
        #     abort(400, 'Something went wrong in POST!')

        return jsonify({
            'message': 'success'
        })


@app.route('/api/bank/latest', methods=['GET'])
def get_latest_bank():
    latest = Bank.query.order_by(Bank.id.desc()).first()
    return latest.data


@app.route('/api/bank/<int:id>', methods=['GET'])
def get_bank_teller(id):
    latest = Bank.query.order_by(Bank.id.desc()).first()
    # bank = Bank.query.get(0)
    if latest is None:
        abort(404, 'Bank not found')
    return latest[id]


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
