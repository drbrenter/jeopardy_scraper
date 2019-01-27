import os


class JeopardyRound:
    def __init__(self, rnum):
        """Data structure representing a round of single or double jeopardy"""

        # Round name and number of questions and categories
        self._num_categories = 6
        self._num_questions  = 5
        if rnum == 1:
            self._round_name = 'Jeopardy'
            self._values = [200, 400, 600, 800, 1000]
        elif rnum == 2:
            self._round_name = 'Double Jeopardy'
            self._values = [400, 800, 1200, 1600, 2000]
        elif rnum == 3:
            self._round_name = 'Final Jeopardy'
            self._num_categories = 1
            self._num_questions  = 1
        else:
            self._round_name = 'Invalid'
            self._num_categories = 0
            self._num_questions  = 0

        # Initialize helper variables
        self._categories = None
        self._round_isvalid = False
        self._round_text = ''
        self._num_valid_questions = 0
        self._whose_pick = 0

        # Initialize empty clue array for all clues, column major order
        if rnum == 1 or rnum == 2:
            # 6 categories of 5 questions = 30 per round
            self._clues = [dict() for x in range(30)]
        elif rnum == 3:
            # Initialize empty clue array for single clue
            self._clues = dict()


class JeopardyEpisode:
    def __init__(self):
        """Python data structure representing an entire three-round episode of Jeopardy"""

        # Date when episode first aired
        self._air_date = None

        # Structures for the three rounds of play
        self._single_jeopardy = JeopardyRound(1)
        self._double_jeopardy = JeopardyRound(2)
        self._final_jeopardy  = JeopardyRound(3)


class JeopardyPlayer:
    def __init__(self, name=''):
        """A structure representing a player in the game of Jeopardy"""

        # Initialize score to zero
        self._score = 0
        # Initialize name to empty
        self._name = name

    def correct_answer(self, value):
        """Player got answer correct, increment score."""
        self._score += value

    def incorrect_answer(self, value):
        """Player got answer wrong, decrement score."""
        self._score -= value


def jeopardy_clue(clue_txt, answer_txt, isvalid=False):
    """Used to create a dictionary of key/values with clue, answer, and validity
        for a single clue in Jeopardy"""
    clue = {'clue': clue_txt, 'answer': answer_txt, 'isvalid': isvalid}
    return clue


def clear_screen():
    """Clear previous outputs from console. Should work cross-platform."""
    os.system('cls' if os.name=='nt' else 'clear')


def get_clue_idx(category_number, question_number, questions_per_category):
    """Helper function to get the index of a particular clue in the list"""
    return question_number + category_number*questions_per_category


def get_game_board(round_struct):
    """Reads the data structure (dictionary array) for the jeopardy round and returns
       a string containing the remaining clues to choose from."""
    game_board_text = round_struct._round_name + ' \n'

    # Iterate through categories
    for category_idx, category in enumerate(round_struct._categories):
        category_text = str(category_idx) + ': ' + category + ': '

        # Iterate through questions within category
        for question_idx in range(round_struct._num_questions):
            # Get index of clue
            idx = get_clue_idx(category_idx, question_idx, round_struct._num_questions)

            # Add a user friendly printout if this clue is valid
            question_text = str(question_idx) + ': '
            if round_struct._clues[idx]['isvalid']:
                question_text += '$' + str(round_struct._values[question_idx]) + ', '
            else:
                question_text += '   '
            category_text += question_text
        category_text += '\n'
        game_board_text += category_text

    return game_board_text


def get_player_scores(players):
    """ Return a string with player's names and scores."""
    player_score_text = 'Current Player Scores: \n'

    # Iterate through players
    for player_idx, player in enumerate(players):
        player_text = player._name + ': ' + str(player._score) + '\n'
        player_score_text += player_text
    return player_score_text


def update_round(round_struct):
    """For a given round, update the text string for user friendly visualization of
        remaining questions, as well as the number of remaining valid questions."""
    # Update text
    round_struct._round_text = get_game_board(round_struct)

    # Update number of valid questions variable
    num_valid = 0
    for question in round_struct._clues:
        if question['isvalid']:
            num_valid += 1
    round_struct._num_valid_questions = num_valid


def test_string_for_int(input_str):
    """Test an input string to see if it contains an integer or something else."""
    try:
        int_str = int(input_str)
        return True
    except:
        return False

def play_question(round_struct, idx_category, idx_question, players):
    """ Play a single question."""

    idx = get_clue_idx(idx_category, idx_question, round_struct._num_questions)
    clue = round_struct._clues[idx]
    category = round_struct._categories[idx_category]
    value = round_struct._values[idx_question]

    # Check question is valid
    if not round_struct._clues[idx]['isvalid']:
        return

    # Show question
    print('Category: ' + category)
    print('Value: ' + str(value))
    print('Question: ' + clue['clue'])

    # Mark clue as invalid now that it has been played
    round_struct._clues[idx]['isvalid'] = False

    # Wait for user input before proceding
    user_input = input('Player buzz in [1/2/3] or skip [s]? : ')

    # Parse player input
    if user_input == 's':
        # Selected skip, do nothing
        return
    elif test_string_for_int(user_input):
        # Rang in, check that its a valid player
        who_rang = int(user_input)-1
        if who_rang <= (len(players) - 1):
            was_correct = player_rang_in(players, who_rang, clue, value)
            if was_correct:
                round_struct._whose_pick = who_rang
    else:
        print('Invalid option: ' + user_input + '. Skipping question.')
        return


def player_rang_in(players, player_idx, clue, value):
    """After a player has rung in, show the answer, see if they were correct, and
        increment the score appropriately."""

    # Give the player a chance to answer
    print(players[player_idx]._name + ' rang in.')
    any_input = input('Press any key when ready for answer: ')

    # Show answer and query if player answered correctly
    print('Correct answer: ' + clue['answer'])
    was_correct = input(players[player_idx]._name + ' got correct answer [y/n]? Or skip [s]:')

    # Increment player score, or skip
    return_correct = False
    if was_correct == 'y':
        players[player_idx].correct_answer(value)
        return_correct = True
    elif was_correct == 'n':
        players[player_idx].incorrect_answer(value)
    elif was_correct == 's':
        print('Selected to skip, no penalty.')
    else:
        print('Invalid option: ' + was_correct + '. Skipping.')

    return return_correct


def play_jeopardy_round(round_struct, players):

    # Update text string and number of valid questions
    update_round(round_struct)
    while round_struct._num_valid_questions > 0:

        # Clear console screen
        clear_screen()

        # Show game board
        print(get_player_scores(players))
        print(round_struct._round_text)

        # Ask user for input, which category and question they want
        whose = players[round_struct._whose_pick]._name
        print(whose + '\'s choice: ')
        idx_category = input('Which category number? : ')
        idx_question = input('Which question number? : ')

        # Check we got valid inputs
        if not test_string_for_int(idx_category) or not test_string_for_int(idx_question):
            continue
        if int(idx_category) >= round_struct._num_categories or \
            int(idx_question) >= round_struct._num_questions:
            continue

        # Clear console screen
        clear_screen()

        # Show their desired question and mark it as invalid
        play_question(round_struct, int(idx_category), int(idx_question), players)

        # Update text string and number of valid questions
        update_round(round_struct)


