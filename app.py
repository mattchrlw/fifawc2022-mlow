# https://levelup.gitconnected.com/how-to-deploy-a-python-flask-api-on-heroku-2e5ddfd943ef
from flask import Flask, request, jsonify
from data import elo_ranking
import random
app = Flask(__name__)

@app.route('/tip', methods=['POST'])
# a tipping method based entirely on fifa ranking numbers and meaningless gut feel arithmetic
def tip():
    data = request.get_json()
    print(data)
    if 'round' in data and 'match' in data and 'team1' in data and 'team2' in data and 'results' in data:
        team1, team2 = elo_ranking(data['team1']), elo_ranking(data['team2'])
        # take 1300 off for no reason
        # lowest ranking is ghana which is 1393 so 1300 felt close enough
        team1_points, team2_points = int(team1['points']) - 1300, int(team2['points']) - 1300
        team1_name, team2_name = team1['name'], team2['name']
        # MOMENTUM CALCULATOR
        # add 50 (once again arbitrary points) for each won game so far
        team1_momentum = len(list(filter(lambda x: (x['team1']['name'] == team1_name and x['team1']['winner']) or (x['team2']['name'] == team1_name and x['team2']['winner']), data['results'])))
        team2_momentum = len(list(filter(lambda x: (x['team1']['name'] == team2_name and x['team1']['winner']) or (x['team2']['name'] == team2_name and x['team2']['winner']), data['results'])))
        team1_points += team1_momentum * 50
        team2_points += team2_momentum * 50

        print(team1_points, team2_points, team1_momentum, team2_momentum)

        if data['round'] == 'Group':
            # bigger difference = less likely to draw.
            # smaller difference = more likely to draw.
            # i pulled this number from nowhere
            # biggest difference is 1841 - 1393 = 448
            draw_points = 700 - (team1_points - team2_points)
            # print(team1_points, draw_points, team2_points)
            # pick a random number up to team1_points + draw_points + team2_points and based on where it lands, choose that
            guess = random.randint(0, team1_points + draw_points + team2_points - 1)
            winner = 'draw'
            if guess < team1_points:
                winner = team1['name']
            elif guess >= team1_points + draw_points:
                winner = team2['name']
            return jsonify({
                'winner': winner
            })
        else:
            # no draws outside of group stage
            # print(team1_points, team2_points)
            guess = random.randint(0, team1_points + team2_points - 1)
            winner = team2['name']
            if guess < team1_points:
                winner = team1['name']
            return jsonify({
                'winner': winner
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