import os.path
import sys
from random import randint

import scraper
import jeopardy


if __name__ == "__main__":

    # TODO: Something better here...
    data_folder = './episode_data/'
    data_source = 'web'
    # data_source = 'file'

    # Initialize jeopardy data object
    jeopardy_game = jeopardy.JeopardyEpisode()

    # Get Jeopardy data from existing text file
    if data_source == 'file':
        file_path = '2017-09-27.txt'
        data_to_read_path = data_folder + file_path
        txt = scraper.get_data_from_text_file(data_to_read_path)

    # Get Jeopardy data - pick a random episode from j-archive
    elif data_source == 'web':
        url_base = 'http://www.j-archive.com/showgame.php?game_id='
        # Valid episode numbers range from 173 (season 1, episode 1) to 6201 (current as of 1/25/19)
        episode_number = randint(173,6201)
        full_url = url_base + str(episode_number)
        txt = scraper.get_data_from_web(full_url)

    soup = scraper.create_soup(txt)
    scraper.parse_jeopardy_game(soup, jeopardy_game)

    # Check if a text file with this data already exists, if not then write it
    output_txt_file = data_folder + jeopardy_game._air_date + '.txt'
    if not os.path.isfile(output_txt_file):
        print('Writing game data to file: '+output_txt_file)
        scraper.write_data_to_text_file(txt, output_txt_file)

    # Query for number of players
    num_players = int(input('Welcome to Jeopardy. How many players? '))
    if num_players < 1 or num_players > 3:
        print('Invalid number of players selected. Please choose  a number between ' \
            '1 and 3. Chosen: ' + str(num_players))
        sys.exit

    # Initialize players
    players = []
    for player in range(num_players):
        name = input('Player ' + str(player+1) + ' enter name: ')
        new_player = jeopardy.JeopardyPlayer(name)
        players.append(new_player)

    # Play single jeopardy round
    jeopardy.play_jeopardy_round(jeopardy_game._single_jeopardy, players)

    # Find who has the least score and denote that they go first
    scores = [player._score for player in players]
    jeopardy_game._double_jeopardy._whose_pick = scores.index(min(scores))

    # Play double jeopardy
    jeopardy.play_jeopardy_round(jeopardy_game._double_jeopardy, players)

    # Play final jeopardy
    # TODO
    # jeopardy.play_jeopardy_round(jeopardy_game._final_jeopardy, players)

    # Print final scores
    print(jeopardy.get_player_scores(players))
