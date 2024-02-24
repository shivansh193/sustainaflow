from flask import Flask, request, jsonify
import distance

from flask_cors import CORS


CORS(app)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"


@app.route('/solve-tsp', methods=['POST'])
def solve_tsp():
    data = request.get_json()
    starting_point = data.get('starting_point')
    distance_matrix = data.get('distance_matrix')

    if starting_point is None or distance_matrix is None:
        return jsonify({'error': 'Missing data for starting point or distance matrix'}), 400

    optimal_route = distance.brute_force_tsp(starting_point, distance_matrix)
    return jsonify({'optimal_route': optimal_route})

if __name__ == '__main__':
    app.run(debug=True)
