# Name: cli.py - command-line interface exercise
# Synopsis: python3 cli.py -t "Team Name" [-d]
# Description: Shows a list of the teams that a given team has played this season,
# and, with -d, prints that team's cumulative point differential.
# Usage: python3 cli.py -t "School name (Team name)" -d
# Example: python3 cli.py -t "Air Force (Afterburn)" -d

import argparse
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
GAMES_FILE = BASE_DIR / 'data' / 'games.json'

def get_parsed_arguments():
    parser = argparse.ArgumentParser(
        description='Report the teams a given team has played this season, '
                    'and optionally their cumulative point differential.'
    )
    parser.add_argument(
        '-t','--team',
        metavar='TEAM',
        help='Team name, e.g. -t "Air Force (Afterburn)"',
        required=True
    )
    parser.add_argument(
        '-d','--differential',
        action='store_true',
        help='Also report the cumulative point differential for the team'
    )
    return parser.parse_args()

def get_competitors(team1):
    try:
        with open(GAMES_FILE, 'r') as f:
            games = json.load(f)
    except FileNotFoundError:
        print("The file containing game data could not be found.")
        return []

    opponents = set()
    for game in games:
        if team1 == game['teamOneName']:
            opponents.add(game['teamTwoName'])
        elif team1 == game['teamTwoName']:
            opponents.add(game['teamOneName'])
    return list(opponents)

def get_differential(team1):
    try:
        with open(GAMES_FILE, 'r') as f:
            games = json.load(f)
    except FileNotFoundError:
        print("The file containing game data could not be found.")
        return 0

    diff = 0
    for game in games:
        if team1 == game['teamOneName']:
            diff += game['teamOneScore'] - game['teamTwoScore']
        elif team1 == game['teamTwoName']:
            diff += game['teamTwoScore'] - game['teamOneScore']
    return diff

def main():
    args = get_parsed_arguments()
    team = args.team
    opponents = get_competitors(team)

    if not opponents:
        print(f"{team} hasn't played anyone in an official USAU event this season.")
        return

    print(f"The teams that {team} has played this season are: {', '.join(opponents)}")

    if args.differential:
        total_diff = get_differential(team)
        print(f"The cumulative point differential for {team} is: {total_diff}")

if __name__ == '__main__':
    main()
