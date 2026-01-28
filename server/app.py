# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def quake(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake is None:
        return {
            "message": f"Earthquake {id} not found."
        }, 404
    return {
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
    }, 200

@app.route("/earthquakes/magnitude/<float:magnitude>")
def magnitude(magnitude):
    magnitudes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return {            
            "count":len(magnitudes),
            "quakes":[{
            "id": m.id,
            "location": m.location,
            "magnitude": m.magnitude,
             "year": m.year,
             } for m in magnitudes
           ]}, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
