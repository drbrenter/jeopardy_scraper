import requests
from bs4 import BeautifulSoup


def get_data_from_text_file(fname):
    '''Read html data from a text file for debugging so we don't bother the server'''
    # Open file
    with open(fname) as f:
        content = f.read()
    return content


def get_data_from_web(url):
    '''Read html data from a webpage'''
    # Make request and check if it was successful, raise exception if no
    content = requests.get(url)
    if content.status_code != requests.codes.ok:
        content.raise_for_status()

    # Return text of html
    return content.text


def create_soup(content):
    '''Create a beautifulsoup object from the html text'''
    soup = BeautifulSoup(content)
    return soup


def parse_jeopardy_round(soup, round_num, jeopardy):
    '''Parse the html data and extract the categories, questions, and answers into
        a data structure'''

    # Determine which round it is and get the relevant section of html data
    if round_num == 1:
        rid = 'jeopardy_round'
    else if round_num == 2:
        rid = 'double_jeopardy_round'
    else:
        print('Bad round number given: '+str(round_num))
        return
    rdata = soup.find(id=rid)
    if not rdata:
        print('Round does not exist for this jeopardy game: '+rid)
        return
