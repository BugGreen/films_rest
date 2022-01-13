from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from bson import json_util, ObjectId

app = Flask(__name__)
api = Api(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/films'  # Chain connection
mongo = PyMongo(app)  # Mongo connection


class BrowserFilm(Resource):  # Resource

    def get(self):

        film = mongo.db.films.find()  # Receives all films stored into the mongo db.

        response = json_util.dumps(film)
        return Response(response, mimetype='application/json')

    def post(self):  # This method is used to add a new movie to the database using a POST request
        # Expected data:
        film_data = {
            'name': None,
            'director': None,
            'duration': None,
            'year': None
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
                                       '\'director\': \'director_name\', \'duration\': \'movie_duration\','
                                       '\'year\': \'movie_year\'}'})


class BrowserFilmModifier(Resource):
    def get(self, film_id):  # Allows user to access to a film_data by its id
        film = mongo.db.films.find_one({'_id': ObjectId(film_id)})
        if not film:
            return {"response": "no film found for {}".format(film_id)}

        response = json_util.dumps(film)
        return Response(response, mimetype='application/json')

    def delete(self, film_id):  # Allows user to delete a film of the database by its id
        mongo.db.films.delete_one({'_id': ObjectId(film_id)})
        response = jsonify({'message': 'Film {} was successfully deleted.'.format(film_id)})
        return response


api.add_resource(BrowserFilm, '/films-browser/')  # Resource BrowserFilm is associated with the route
# APP_URL + /films-browser/
api.add_resource(BrowserFilmModifier, '/films-browser/<string:film_id>')

if __name__ == '__main__':
    app.run(debug=True)
