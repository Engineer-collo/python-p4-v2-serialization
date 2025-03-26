# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id==id).first()

    if pet:
        response_body = pet.to_dict()
        response_status = 200
    else:
        response_body = {'message': f'Pet id {id} not found.'}
        response_status = 404
    
    response = make_response(response_body,response_status)
    return response

@app.route('/species/<string:species>')
def pet_by_species(species):
    #fets from database species
    pets = Pet.query.filter_by(species=species).all()
    pets_dict = []
    for pet in pets:
        #store pet dictionary
        pets_dict.append(pet.to_dict())
     
    count = len(pets_dict)
    #response body
    response_body = {
        'count' : count,
        'pets' : pets_dict
        }
    response_status = 200

    response = make_response(response_body,response_status)
    return response
if __name__ == '__main__':
    app.run(port=5555, debug=True)
