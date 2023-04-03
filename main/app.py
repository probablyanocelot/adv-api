from dataclasses import dataclass
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
import requests

# from producer import publish

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'  # :root
# :5432 , :33068
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:test@db:5432/adv_lnd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
CORS(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@dataclass
class JsonObject(db.Model):
    __tablename__ = 'bank'
    id: int
    data: str

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/bank/wipe')
def wipe():
    # for all records
    db.session.query(JsonObject).delete()
    db.session.commit()
    return jsonify({
        'message': 'wiped'
    })


@app.route('/api/bank', methods=['POST', 'GET'])
def bank():
    # content = request.json
    # content = {'me': 'irritable'}
    # return jsonify(JsonObject.query.all())
    if request.method == 'GET':
        try:
            return jsonify(JsonObject.query.all())
        except:
            abort(400, 'Something went wrong in GET!')

    if request.method == 'POST':
        try:
            # print(request)
            data = request.json
            jsonObject = JsonObject(data=str(data))
            db.session.add(jsonObject)
            db.session.commit()

        except:
            abort(400, 'Something went wrong in POST!')

        return jsonify({
            'message': 'success'
        })
    # return jsonify(JsonObject.query.all())


@app.route('/api/bank/<int:id>', methods=['GET'])
def bank_by_id(id):
    return jsonify(JsonObject.query.get(id))

# @app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
# def add_message(uuid):
#     content = request.json
#     print(content['mytext'])
#     return jsonify({"uuid":uuid})


@ app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
