import random


class CrapsTable:
    """ Emulates a Craps Table """

    def __init__(self):
        self.bets = {"Pass": {}, "No_Pass": {}, "Field": {}, "Odds": {}, "Big": {},
                     "Place": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Buy": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Hardway": {"4": {}, "6": {}, "8": {}, "10": {}},
                     "Seven": {}, "Craps": {"2": {}, "3": {}, "11": {}, "12": {}, "Any": {}}
                     }
        self.table_open = False
        self.roller = None
        self.players = []
        self.dice_roll = None
        self.point_holder = None
        self.point_on = False

    def roll_dice(self):
        """ Rolls two six-sided die """
        rolls = []
        for i in range(2):
            roll = random.randint(1, 6)
            rolls.append(roll)
        self.dice_roll = rolls

    def add_player(self, player):
        """ Add player to the table """
        self.players.append(player)

    def remove_player(self, player):
        """ Remove player from the table """
        self.players.remove(player)

    def find_player(self, player_id: int):
        """ Find player at the table """
        for player in self.players:
            if player.id == player_id:
                return player

    def set_point(self, point_num: int):
        """ Set point number """
        self.point_holder = point_num

    def process_roll(self, dice: tuple):
        if dice == (1, 1):
            payouts = self.stickman
        elif dice in [(1, 2), (2, 1)]:
            pass
        elif dice in [(1, 3), (3, 1), (2, 2)]:
            pass
        elif dice in [(1, 4), (4, 1), (3, 2), (2, 3)]:
            pass
        elif dice in [(1, 5), (5, 1), (4, 2), (2, 4), (3, 3)]:
            pass
        elif dice in [(1, 6), (6, 1), (2, 5), (5, 2), (3, 4), (4, 3)]:
            pass
        elif dice in [(2, 6), (6, 2), (3, 5), (5, 3), (4, 4)]:
            pass
        elif dice in [(3, 6), (6, 3), (4, 5), (5, 4)]:
            pass
        elif dice in [(4, 6), (6, 4), (5, 5)]:
            pass
        elif dice in [(5, 6), (6, 5)]:
            pass
        elif dice == (6, 6):
            pass
        else:
            raise ValueError("Dice combination provided is not a valid 2x D6 result")