

class JeopardyRound:
    def __init__(self, rnum):
        """Data structure representing a round of single or double jeopardy"""

        # Round name
        if rnum == 1:
            self._round_name = 'Jeopardy'
        elif rnum == 2:
            self._round_name = 'Double Jeopardy'
        elif rnum == 3:
            self._round_name = 'Final Jeopardy'
        else:
            self._round_name = None

        # Initialize helper variables
        self._categories = None;
        self._round_isvalid = False;

        # Initialize empty clue array for all clues, column major order
        if rnum == 1 or rnum == 2:
            # 6 categories of 5 questions = 30 per round
            self._clues = [dict() for x in range(30)]
        elif rnum == 3:
            # Initialize empty clue array for single clue
            self._clues = dict()


class FinalJeopardyRound:
    def __init__(self):
        """Data structure for a round of final jeopardy"""

        # Round name
        self._round_name = 'Final Jeopardy'

        # Helper variables
        self._categories = None;
        self._round_isvalid = True

        # Initialize empty clue array for single clue
        self._clues = dict()


class JeopardyEpisode:
    def __init__(self):
        """Python data structure representing an entire three round episode of Jeopardy"""

        # Date when episode first aired, and identifier number within j-archive
        self._air_date = None;
        self._j_archive_id = None;

        # Structures for the three rounds of play
        self._single_jeopardy = JeopardyRound(1);
        self._double_jeopardy = JeopardyRound(2);
        self._final_jeopardy  = JeopardyRound(3);


def jeopardy_clue(clue_txt, answer_txt, isvalid=False):
    """Used to create a dictionary of key/values with clue, answer, and validity
        for a single clue in Jeopardy"""
    clue = {'clue': clue_txt, 'answer': answer_txt, 'isvalid': isvalid}
    return clue
