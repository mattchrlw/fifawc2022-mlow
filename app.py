# https://levelup.gitconnected.com/how-to-deploy-a-python-flask-api-on-heroku-2e5ddfd943ef
from flask import Flask, request, jsonify
from data import elo_ranking
app = Flask(__name__)

@app.route('/tip', methods=['POST'])
def tip():
    data = request.get_json()
    print(data)
    if 'round' in data and 'match' in data and 'team1' in data and 'team2' in data and 'results' in data:
        print(elo_ranking(data['team1']))
        print(elo_ranking(data['team2']))
        return jsonify({
            'winner': "Australia"
        })
    else:
        return jsonify({
            "ERROR": "Invalid POST"
        })


@app.route('/',)
def index():
    # A welcome message to test our server
    return "Welcome to Matt's horrible World Cup tipping service."


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)