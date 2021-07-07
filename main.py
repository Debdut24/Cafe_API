# API_DOCUMENTATION : https://documenter.getpostman.com/view/14373528/Tzm3oxsH
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
import random

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
API_KEY = "qwertyuiop0987654321"
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class MySQL(SQLAlchemy):
    Column:Callable
    String:Callable
    Integer:Callable
    Boolean:Callable

db = MySQL(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

def change_to_dict(cafe):
    json_file = {
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "seats": cafe.seats,
        "has_toilet": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "has_sockets": cafe.has_sockets,
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
    }
    return json_file

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods = ['GET'] )
def random_cafe():
    cafe_list = Cafe.query.all()
    cafe = random.choice(cafe_list)
    return jsonify(change_to_dict(cafe))

@app.route('/all')
def send_all():
    cafe_list = Cafe.query.all ()
    final_list = []
    final_list = [change_to_dict(cafe) for cafe in cafe_list]

    return jsonify(final_list)


@app.route('/search')
def search():
    entry = request.args.get("loc")
    entry = entry.title()
    search_cafe = Cafe.query.filter_by(location = entry).all()
    dict_file = [change_to_dict(cafe) for cafe in search_cafe]
    if dict_file:
        return jsonify(dict_file)
    else:
        return jsonify({
            "error":{
                "Not Found":"Sorry we don't have that cafe location."
            }
        })

## HTTP GET - Read Record

# HTTP POST - Create Record
@app.route('/add', methods = ['POST'])
def add_cafe():
    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get("map_url"),
        img_url = request.form.get("img_url"),
        location = request.form.get("location"),
        seats = request.form.get("seats"),
        has_toilet = int(request.form.get("has_toilet")),
        has_wifi = int(request.form.get("has_wifi")),
        has_sockets = int(request.form.get("has_sockets")),
        can_take_calls = int(request.form.get("can_take_calls")),
        coffee_price = request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify({
        "response":{
            "success":"Successfully added the new cafe."
        }

    })

## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<cafe_id>', methods = ['PATCH'])
def update_price(cafe_id):
    cafe = Cafe.query.filter_by(id = cafe_id).first()
    if cafe:
        cafe.coffee_price = request.form.get("new_price")
        db.session.commit()
        return jsonify ({
            "response": {
                "success": "Successfully added the new cafe."
            }
        })
    else:
        return jsonify ({
            "error": {
                "Not Found": "Sorry a cafe with that id does not exist."
            }
        })


## HTTP DELETE - Delete Record
@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def delete(cafe_id):
    api_key = request.args.get ("api_key")
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe and api_key == API_KEY:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify ({
            "response": {
                "success": "Successfully deleted the new cafe."
            }
        })
    elif api_key != API_KEY:
        return jsonify ({
            "error": {
                "Error": "Sorry, that's not allowed. MAke sure you have the correct api_key"
            }
        })
    else:
        return jsonify ({
            "error": {
                "Not Found": "Sorry a cafe with that id does not exist."
            }
        })


if __name__ == '__main__':
    app.run(debug=True)
