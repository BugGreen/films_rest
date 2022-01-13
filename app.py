from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from bson import json_util, ObjectId

app = Flask(__name__)
api = Api(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/films'  # Chain connection
mongo = PyMongo(app)  # Mongo connection


class Films(Resource):

    def post(self):  # This method is used to add a new movie to the database using a POST request
        # Expected data:
        film_data = {
            'name': '',
            'director': '',
            'duration': '',
            'year': ''
        }

        # Receiving data
        data = request.json
        try:
            if data['name']:  # The user have to at least insert the name of the movie
                possible_data = film_data.keys()
                for k, v in data.items():  # Fill film_data whit the received information
                    if k in possible_data:  # Ignores any additional data
                        film_data[k] = v

                film_id = mongo.db.films.insert_one(film_data)

                response = {
                    'id': str(film_id.inserted_id),
                    }
                return response  # User gets the ID of the film
        except KeyError:
            return jsonify({'message': 'expected input structure: {\'name\': \'film_name\', '
                                       '\'director\': \'dierctor_name\', \'duration\': \'movie_duration\','
                                       '\'year\': \'movie_year\'}'})


# URL routes for each resource:
api.add_resource(Films, '/films/add_film/')  # http://127.0.0.1:5000/films/add_film/

if __name__ == '__main__':
    app.run(debug=True)