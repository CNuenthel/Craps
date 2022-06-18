import random
from Craps.craps_stickman import CrapsStickman
from Craps.craps_bets import CrapsBets


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
        self.dice_roll = tuple(rolls)

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

    def process_roll(self):
        stickman = CrapsStickman(self)
        if self.dice_roll == (1, 1):
            result = stickman.snake_eyes(self.point_on)

        elif self.dice_roll in [(1, 2), (2, 1)]:
            result = stickman.ace_deuce(self.point_on)

        elif self.dice_roll in [(1, 3), (3, 1), (2, 2)]:
            result = stickman.four(self.dice_roll, self.point_on)

        elif self.dice_roll in [(1, 4), (4, 1), (3, 2), (2, 3)]:
            result = stickman.five(self.point_on)

        elif self.dice_roll in [(1, 5), (5, 1), (4, 2), (2, 4), (3, 3)]:
            result = stickman.six(self.dice_roll, self.point_on)

        elif self.dice_roll in [(1, 6), (6, 1), (2, 5), (5, 2), (3, 4), (4, 3)]:
            result = stickman.seven(self.point_on)
            if self.point_on:
                CrapsBets(self).clear_all_bets()
                return result

        elif self.dice_roll in [(2, 6), (6, 2), (3, 5), (5, 3), (4, 4)]:
            result = stickman.eight(self.dice_roll, self.point_on)

        elif self.dice_roll in [(3, 6), (6, 3), (4, 5), (5, 4)]:
            result = stickman.nine(self.point_on)

        elif self.dice_roll in [(4, 6), (6, 4), (5, 5)]:
            result = stickman.ten(self.dice_roll, self.point_on)

        elif self.dice_roll in [(5, 6), (6, 5)]:
            result = stickman.eleven(self.point_on)

        elif self.dice_roll == (6, 6):
            result = stickman.twelve(self.point_on)

        else:
            raise ValueError("Dice combination provided is not a valid 2x D6 result")

        # Clear all single roll bets
        CrapsBets(self).clear_single_roll_bets()
        return result






