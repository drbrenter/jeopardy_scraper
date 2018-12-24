import requests
import jeopardy
from bs4 import BeautifulSoup


def get_data_from_text_file(fname):
    """Read html data from a text file for debugging so we don't bother the server"""
    with open(fname) as f:
        content = f.read()
    return content


def get_data_from_web(url):
    """Read html data from a webpage"""

    # Make request and check if it was successful, raise exception if no
    content = requests.get(url)
    if content.status_code != requests.codes.ok:
        content.raise_for_status()

    # Return text of html
    return content.text


def write_data_to_text_file(text_content, output_fname):
    """Helper function to stash html text into a text file for later use"""
    with open(output_fname, 'w') as f:
        f.write(text_content)


def create_soup(content):
    """Create a beautifulsoup object from the html text"""
    soup = BeautifulSoup(content, 'lxml')
    return soup


def scrub_text(text):
    """Remove weird character formatting from text parsed from html that causes
        mismatched quotes"""
    # if "\"" in text:
    #     text.replace("\"", "")
    if '\'' in text:
        # import ipdb; ipdb.set_trace()
        return text.replace('\'', '')
    return text


def parse_single_clue(clue_data, is_final_jeopardy=False):
    """ Read a chunk of beautiful soup containing a single clue and answer. Parse
        them, format the text, and output them, plus a validity flag"""
    clue = None
    answer = None
    is_valid = True if clue_data.get_text().strip() else False
    if is_valid:
        clue_raw = clue_data.find('td', class_='clue_text').get_text()
        clue = scrub_text(clue_raw)
        answer_soup = BeautifulSoup(clue_data.find('div', onmouseover=True).get('onmouseover'), 'lxml')
        if not is_final_jeopardy:
            answer_raw = answer_soup.find('em', class_='correct_response').get_text()
        else:
            answer_raw = answer_soup.find('em').get_text()
        answer = scrub_text(answer_raw)

    return clue, answer, is_valid


def parse_jeopardy_round(soup, round_num, round_struct):
    """Parse the html data and extract the categories, questions, and answers into
        a data structure"""

    # Determine which round it is
    if round_num == 1:
        html_rid = 'jeopardy_round'
    elif round_num == 2:
        html_rid = 'double_jeopardy_round'
    elif round_num == 3:
        html_rid = 'final_round'
    else:
        print('Invalid round number given: '+str(round_num))
        round_struct._round_isvalid = False
        return

     # Get the relevant section of html data
    if round_num == 1 or round_num == 2:
        rdata = soup.find(id=html_rid)
    else:
        rdata = soup.find('table', class_=html_rid)
        # import ipdb; ipdb.set_trace()
    if not rdata:
        print('Round does not exist for this particular jeopardy dataset: '+html_rid)
        return

    # Get category names
    round_struct._categories = [category.get_text() for category in rdata.find_all('td',
        class_='category_name')]

    # Get clues and answers for single and double jeopardy
    if round_num == 1 or round_num == 2:
        ctr = 0
        for clue_html in rdata.find_all('td', class_='clue'):
            # Get clue data
            clue, answer, is_valid = parse_single_clue(clue_html, False)

            # Insert clue data in the round's data structure
            round_struct._clues[ctr] = jeopardy.jeopardy_clue(clue, answer, is_valid)
            ctr += 1
    # Get clues and answers for final jeopardy
    else:
        # Get clue data
        clue, answer, is_valid = parse_single_clue(rdata, True)

        # Insert clue data in the round's data structure
        round_struct._clues = jeopardy.jeopardy_clue(clue, answer, is_valid)


def parse_jeopardy_game(soup, jeopardy_struct):
    """Parse the html data for all three rounds and get the data"""

    # Get

    # Get single, double, and final jeopardy categories and clues
    parse_jeopardy_round(soup, 1, jeopardy_struct._single_jeopardy)
    parse_jeopardy_round(soup, 2, jeopardy_struct._double_jeopardy)
    parse_jeopardy_round(soup, 3, jeopardy_struct._final_jeopardy)

    # Get final jeopardy category and clues


