import csv
import os
import random

owned_games = {}
game_constraints = {}


def main():
    load_games()
    random_game()


def load_games():
    try:
        with open('games.csv', 'r') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                game_constraints[line[0]] = int(line[1])

        for player_file in os.listdir('players'):
            player = player_file.partition('.')[0]
            owned_games[player] = set()
            with open('players/' + player_file, 'r') as f:
                owned_games[player] = {line.strip().lower() for line in f.readlines()}
        print('Loaded previous data from disk')
    except Exception as ex:
        print('Nothing to load from disk')
        ...


def save_games():
    with open('games.csv', 'w+', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(list(game_constraints.items()))
    for player in owned_games:
        if not os.path.exists('players'):
            os.makedirs('players')
        with open(f'players/{player}.csv', 'w+', newline='') as f:
            f.writelines(sorted(list(owned_games[player])))


def random_game():
    players_picked = False
    players = []
    while not players_picked:
        print('Who is playing? (csv)')
        players = input('>').split(',')
        print('')
        players_picked = all(
            player in owned_games for player in players
        ) and len(players) > 0
        if not players_picked:
            print('Invalid player(s). Try again.\n')
    intersect = owned_games[players[0]]
    for player in players[1:]:
        intersect = intersect.intersection(owned_games[player])
    intersect = {
        item for item in intersect
        if game_constraints[item] <= len(players)
    }
    while True:
        game_choice = random.choice(list(intersect))
        print(f'You can play {game_choice}.')
        print("Play or retry? ('R' to retry)")
        choice = input('>')
        print('')
        if choice != 'R':
            break


if __name__ == '__main__':
    main()
