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
        self._air_date = None;

        # Structures for the three rounds of play
        self._single_jeopardy = JeopardyRound(1);
        self._double_jeopardy = JeopardyRound(2);
        self._final_jeopardy  = JeopardyRound(3);


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
    game_board_text = ''

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


def play_jeopardy_round(round_struct):

    # Update text string and number of valid questions
    update_round(round_struct)
    while round_struct._num_valid_questions > 0:

        # Clear console screen
        clear_screen()

        # Show game board
        print(round_struct._round_text)

        # Ask user for input, which category and question they want
        idx_category = int(input('Which category number? : '))
        idx_question = int(input('Which question number? : '))
        idx = get_clue_idx(idx_category, idx_question, round_struct._num_questions)

        # Clear console screen
        clear_screen()

        # Show their desired question and mark it as invalid
        clue = round_struct._clues[idx]
        print('Category: ' + round_struct._categories[idx_category])
        print('Question: ' + clue['clue'])
        print('Answer: ' + clue['answer'])
        round_struct._clues[idx]['isvalid'] = False

        # Wait for user input before proceding
        ok = input('OK? : ')

        # Update text string and number of valid questions
        update_round(round_struct)
