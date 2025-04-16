# Name: cli.py - command-line interfce exercise
# Synopsis: python3 cli.py competitors of team
# Description: Shows a list of the teams that a given team has playd this season.
#     The inputted team name should be of the format "School name (Team name)"
# Usage: python3 cli.py -t "School name (Team name)"
# Example: python3 cli.py -t "Air Force (Afterburn)"

import argparse
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
GAMES_FILE = BASE_DIR / 'data' / 'games.json'
# Had to do some weird stuff because WSL doesn't like normal paths because of /mnt/

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Report a list of the teams a given team has played this season.')
    parser.add_argument('-t','--team', metavar='team1', help='one team whose competitors you seek. Example: -t Air Force (Afterburn)', required=True)
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def get_competitors(team1):
    try:
        with open(GAMES_FILE, 'r') as file:
            games = json.load(file)
    except FileNotFoundError:
        print("The file containing game data could not be found.")
        return []
    
    competitors = set()
    for game in games:
        if team1 == game['teamOneName']:
            competitors.add(game['teamTwoName'])
        elif team1 == game['teamTwoName']:
            competitors.add(game['teamOneName'])
    return list(competitors)

def main():
    arguments = get_parsed_arguments()
    team1 = arguments.team
    competitors = get_competitors(team1)
    if competitors:
        print(f'The teams that {team1} has played this season are: {", ".join(competitors)}')
    else:
        print(f'{team1} hasn\'t played anyone in an official USAU event this season.')



if __name__ == '__main__':
    main()