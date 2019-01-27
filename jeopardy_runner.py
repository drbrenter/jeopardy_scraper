import os.path
import sys

import scraper
import jeopardy


if __name__ == "__main__":

    # TODO: Something better here...
    data_folder = './episode_data/'
    file_path = '2017-09-27.txt'
    data_to_read_path = data_folder + file_path

    # Initialize jeopardy data object
    jeopardy_game = jeopardy.JeopardyEpisode()

    # Get Jeopardy data
    txt = scraper.get_data_from_text_file(data_to_read_path)
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
        exit

    # Initialize players
    players = []
    for player in range(num_players):
        name = input('Player ' + str(player+1) + ' enter name: ')
        new_player = jeopardy.JeopardyPlayer(name)
        players.append(new_player)

    # Play jeopardy round
    jeopardy.play_jeopardy_round(jeopardy_game._single_jeopardy, players)

