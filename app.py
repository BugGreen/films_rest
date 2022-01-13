from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/films'  # Chain connection
mongo = PyMongo(app)  # Mongo connection


class Films(Resource):

    def post(self):
        # Receiving data
        data = request.json
        print(len(data))
        film_name = data['name']
        director = data['director']
        year = data['year']
        if film_name and director and year:
            film_id = mongo.db.films.insert_one(  # insert(this.json) into the collection films
                # use .insert_one() for versions of Pymongo previous to 3.0
                {
                    "name": film_name,
                    "director": director,
                    "year": year
                }
            )  # insert_one() returns the id of the data stored
            response = {
                'id': str(film_id.inserted_id),
                # Attribute inserted.id returns the id of the object film_id
                "name": film_name,
                "director": director,
                "year": year
            }
            return response


# URL routes for each resource:
api.add_resource(Films, '/api', endpoint='films')  # http://127.0.0.1:5000/api/films

if __name__ == '__main__':
    app.run(debug=True)