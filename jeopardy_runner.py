import os.path

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