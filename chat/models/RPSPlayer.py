from ..models.GameResult import GameResult
from ..models.RPSChoice import RPSChoice

class RPSPlayer:
    def __init__(self, player_id: str, choice: RPSChoice) -> None:
        self.player_id = player_id
        self.choice = choice
        self.result: GameResult = None

    def set_choice(self, choice: RPSChoice) -> None:
        self.choice = choice

    def get_choice(self) -> RPSChoice:
        return self.choice
    
    def determine_result_against(self, opponent) -> GameResult:
        result = None
        is_win = any([(self.choice == RPSChoice.PAPER and opponent.choice == RPSChoice.ROCK),
                    (self.choice == RPSChoice.SCISSORS and opponent.choice == RPSChoice.PAPER),
                    (self.choice == RPSChoice.ROCK and opponent.choice == RPSChoice.SCISSORS),
                     ])
        is_draw = self.choice == opponent.choice

        if is_win:
            result = GameResult.WIN
        elif is_draw:
            result = GameResult.DRAW
        else:
            result = GameResult.LOSE
        return result