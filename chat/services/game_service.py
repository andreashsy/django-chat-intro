from mywebsite.chat.models.RPSPlayer import RPSPlayer
from mywebsite.chat.models.RPSGamePhase import RPSGamePhase

class RPSGameState:
    def __init__(self) -> None:
        self.player: RPSPlayer = None
        self.game_state: RPSGamePhase = RPSGamePhase.PREGAME

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

    