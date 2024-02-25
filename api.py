from flask import Flask, request, jsonify
import distance

from flask_cors import CORS




app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'key': 'value'})

@app.route('/solve-tsp', methods=['POST'])
def solve_tsp():
    data = request.get_json()

    cities = data.get('cities')
    #print(cities)
    starting_point = 0
    distance_matrix = distance.create_data_model(cities)

    distance_matrix = distance_matrix['distance_matrix']

    if starting_point is None or distance_matrix is None:
        return jsonify({'error': 'Missing data for starting point or distance matrix'}), 400

    optimal_route = distance.brute_force_tsp(starting_point, distance_matrix)
    return jsonify({'optimal_route': optimal_route})


CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
