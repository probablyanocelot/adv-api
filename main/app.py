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
class Inventory(db.Model):
    __tablename__ = 'inventory'
    id: int
    inventory: str

    id = db.Column(db.Integer, primary_key=True)
    inventory = db.Column(db.Text())


class EquippedItems(db.Model):
    __tablename__ = 'equipped_items'
    id: int
    character: str
    equipped_items: str
    head: str
    body: str
    legs: str
    feet: str
    hands: str
    neck: str
    ring1: str
    ring2: str
    weapon: str
    shield: str
    earring1: str
    earring2: str

    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(128))
    equipped_items = db.Column(db.Text())
    head = db.Column(db.String(128))
    body = db.Column(db.String(128))
    legs = db.Column(db.String(128))
    feet = db.Column(db.String(128))
    hands = db.Column(db.String(128))
    neck = db.Column(db.String(128))
    ring1 = db.Column(db.String(128))
    ring2 = db.Column(db.String(128))
    weapon = db.Column(db.String(128))
    shield = db.Column(db.String(128))
    earring1 = db.Column(db.String(128))
    earring2 = db.Column(db.String(128))


@dataclass
class Item(db.Model):
    __tablename__ = 'item'
    id: int
    name: str
    level: int
    slot: int
    # price: int
    quantity: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=True)
    level = db.Column(db.Integer)
    slot = db.Column(db.Integer)


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
    return teller.items  # jsonify(teller)


@app.route('/api/<string:char>/slots', methods=['POST', 'GET'])
def char_equipment(char):
    if request.method == 'GET':
        try:
            return jsonify(EquippedItems.query.all())
        except:
            abort(400, 'Something went wrong in GET!')

    if request.method == 'POST':
        equipment_data = request.json
        print(equipment_data)
        equipment = EquippedItems(
            equipped_items=str(equipment_data),
            head=str(equipment_data['head']),
            body=str(equipment_data['body']),
            legs=str(equipment_data['legs']),
            feet=str(equipment_data['feet']),
            hands=str(equipment_data['hands']),
            neck=str(equipment_data['neck']),
            ring1=str(equipment_data['ring1']),
            ring2=str(equipment_data['ring2']),
            weapon=str(equipment_data['weapon']),
            shield=str(equipment_data['shield']),
            earring1=str(equipment_data['earring1']),
            earring2=str(equipment_data['earring2'])
        )

        try:
            db.session.add(equipment)
            db.session.commit()
        except:
            abort(400, 'Something went wrong in equipment POST!')

        return jsonify({
            'message': 'equipment post success'
        })


@app.route('/api/<string:char>/inventory', methods=['POST', 'GET'])
def char_inventory(char):
    if request.method == 'GET':
        try:
            return jsonify(Inventory.query.all())
        except:
            abort(400, 'Something went wrong in GET!')

    if request.method == 'POST':
        inventory_data = request.json
        print(inventory_data)
        inventory = Inventory(
            inventory=str(inventory_data)
        )

        try:
            db.session.add(inventory)
            db.session.commit()
        except:
            abort(400, 'Something went wrong in inventory POST!')

        return jsonify({
            'message': 'inventory post success'
        })

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
