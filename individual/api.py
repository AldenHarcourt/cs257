#!/usr/bin/env python3
import sys
import argparse
import flask
import json

app = flask.Flask(__name__)

with open('games.json') as f:
    games = json.load(f)

@app.route('/')
def hello():
    return 'Hello frisbee enthusiast.'

@app.route('/competitors_of/<team>')
def get_competitors_of(team):
    '''Returns all teams played in the 2025 regular season by a given team'''
    competitors = []
    for game in games:
        if team == game['teamOneName']:
            competitors.append(game['teamTwoName'])
        elif team == game['teamTwoName']:
            competitors.append(game['teamTwoName'])
    return json.dumps(competitors)

@app.route('/point_diff/<team>')
def get_point_diff(team):
    ''' Returns the total point differential of a given team throughout the 2025 regular season. '''
    diff = 0
    for game in games:
        if team == game['teamOneName']:
            diff += game['teamOneScore'] - game['teamTwoScore']
        elif team == game['teamTwoName']:
            diff += game['teamTwoScore'] - game['teamOneScore']
    return json.dumps(diff)

@app.route('/teams')
def get_teams():
    teams = []
    for game in games:
        if game['teamOneName'] not in teams:
            teams.append(game['teamOneName'])
        if game['teamTwoName'] not in teams:
            teams.append(game['teamTwoName'])
    return json.dumps(teams)


@app.route('/help')
def get_help():
    return flask.render_template('help.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
