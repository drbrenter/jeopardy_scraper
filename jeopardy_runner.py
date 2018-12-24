import scraper
import jeopardy


if __name__ == "__main__":

    # TODO: Something better here...
    file_path = 'episode1.txt'

    # Initialize jeopardy data object
    jeopardy_game = jeopardy.JeopardyEpisode()

    # Get Jeopardy data
    txt = scraper.get_data_from_text_file(file_path)
    soup = scraper.create_soup(txt)
    scraper.parse_jeopardy_game(soup, jeopardy_game)