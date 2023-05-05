from ..models.RPSChoice import RPSChoice
from ..models.RPSPlayer import RPSPlayer
from ..models.RPSGamePhase import RPSGamePhase

class RPSGameState:
    def __init__(self) -> None:
        self.player: RPSPlayer = None
        self.game_state: RPSGamePhase = RPSGamePhase.PREGAME

    def is_player_waiting(self) -> bool:
        return not not self.player

    def add_player(self, player_id: str, choice: RPSChoice) -> None:
        self.player = RPSPlayer(player_id, choice)

    def set_player(self, player: RPSPlayer) -> None:
        self.player = player
        self.game_state = RPSGamePhase.WAITING_FOR_OPPONENT

    def reset(self) -> None:
        self.player = None
        self.game_state = RPSGamePhase.PREGAME

    def resolve_against(self, opponent: RPSPlayer) -> RPSGamePhase:
        if not self.player: raise ValueError("Cannot resolve if no current player")
        player = self.player
        self.reset()
        return player.determine_result_against(opponent)        

    