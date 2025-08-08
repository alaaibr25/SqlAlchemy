from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from random import *
import os

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    has_sockets: Mapped[bool] = mapped_column(nullable=False)
    has_toilet: Mapped[bool] = mapped_column(nullable=False)
    has_wifi: Mapped[bool] = mapped_column(nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(nullable=False)
    seats: Mapped[str] = mapped_column(nullable=False)
    coffee_price: Mapped[str] = mapped_column(nullable=False)

    # to serialising our db row object to JSON
    #first converting it to a dictionary and then using jsonify()
    def to_dict(self):
        dictionary ={}
        # for column in self.__table__.columns:
        #     #key= col's name, value= col's value
        #     dictionary[column.name] = getattr(self, column.name)
        # #Method 1.
        # return dictionary
        #Method 2.
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


with app.app_context():
     db.create_all()


#✅ 1. Create a /random that allows GET requests to be made to it.

@app.route('/')
def random_cafe():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    rand_cafe = choice(all_cafes)

    #Method 0
    # return jsonify(cafe={'id': rand_cafe.id,
    #                     'can_take_calls': rand_cafe.can_take_calls,
    #                     'name': rand_cafe.name})
    #Method 1. 2.
    return jsonify(cafe=rand_cafe.to_dict())

#✅return all the cafes in your database as a JSON

@app.route('/all')
def all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

#🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡
#The user will make a GET request to your /search route and
# pass the location (loc) as a parameter.
# Parameters are passed in the URL with "?" .
#http://127.0.0.1:5000/search?loc=Peckham
#🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡

@app.route('/search')
def cafe_per_area():
    query_loc = request.args.get('loc')
    cafes_area = db.session.execute(db.select(Cafe).where(Cafe.location == query_loc)).scalars().all()

    if cafes_area:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes_area])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


#🟡POSTMAN
#🟡The Key-Value pairs you enter into the Body tab in Postman is equivalent to <input> elements.
#POST, http://127.0.0.1:5000/add, Body, x-www-form
#then make the form as a key value pair on postman
#you need to create a new route as before but without WTForm


@app.route('/add', methods=['POST'])
def add_page():

    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),

    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe"})


@app.route('/update-price/<int:cafe_id>', methods=['POST'])
def update_patch(cafe_id):
    #🟡to get the typed data after '?'
    query_price = request.args.get('new_price')

    #🟡 fine by the cafe_id param that will typed before '?'
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    #🟡finally update structure
    if cafe:
        cafe.coffee_price = query_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated"}), 200

    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    query_api = request.args.get('api-key')
    if query_api == 'Top123':
        cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()

        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Delete is Done"}), 200
        else:
            return jsonify(response={"Failed": "Not Found"}), 404

    else:
        return jsonify(response={'ERROR': 'Not Allowed'}), 401

app.run(debug=True)
