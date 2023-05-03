from django.db import models
from enum import Enum
# Create your models here.

class RPSChoice(Enum):
    ROCK = 'r'
    PAPER = 'p'
    SCISSORS = 's'

class RPSPlayer:
    def __init__(self, player_id = '', choice = None) -> None:
        self.player_id = player_id
        self.choice = choice

    def set_choice(self, choice: RPSChoice) -> None:
        self.choice = choice

    def get_choice(self) -> RPSChoice:
        return self.choice
    
    def is_win_against(self, opponent) -> bool:
        return any([(self.choice == RPSChoice.PAPER and opponent.get_choice() == RPSChoice.ROCK),
                    (self.choice == RPSChoice.SCISSORS and opponent.get_choice() == RPSChoice.PAPER),
                    (self.choice == RPSChoice.ROCK and opponent.get_choice() == RPSChoice.SCISSORS),
                     ])