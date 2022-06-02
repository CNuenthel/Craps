import random
from dataclasses import dataclass


def need_more_chips(player_name: str):
    """ Returns a random response to a player betting more chips than they have """
    responses = [
        f"Hey {player_name}, you need more dosh to make that bet",
        f"Nice try {player_name}, cash in first to make that bet",
        f"With what chips {player_name}?",
        f"Maybe you should win on a roll before placing chips you dont have {player_name}.",
        f"Get some chips to put on the table first {player_name}"
    ]
    return random.choice(responses)


def bet_off_comeout_roll(player_name: str):
    """ Returns a random response to a player making a bet requiring the point to be off"""
    responses = [
        f"{player_name}, hold that bet, the point is on right now. Wait for a new comeout roll"
    ]
    return random.choice(responses)


def bet_on_comeout_roll(player_name: str):
    """ Returns a random response to a player making a bet requiring the point to be on """
    responses = [
        f"{player_name}, you cannot make that bet while the point is off"
    ]
    return random.choice(responses)


def no_pass_bet(player_name: str):
    """ Returns a random response to a player making a bet requiring a current pass line bet """
    responses = [
        f"{player_name}, you cannot make that bet without a previous pass bet"
    ]
    return random.choice(responses)

@dataclass
class Player:
    name: str
    chips: int
    id: int


class Craps:
    """ Emulates a Craps Table """

    def __init__(self):
        self.table_open = False
        self.roller = None
        self.players = {}
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


class CrapsDealer:
    """ Bet controller for Craps table """

    def __init__(self, craps_table: Craps):
        self.table = craps_table
        self.bets = {"Pass": {}, "No_Pass": {}, "Field": {}, "Odds": {}, "Big": {},
                     "Place": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Buy": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Hardway": {"4": {}, "6": {}, "8": {}, "10": {}},
                     "Seven": {}, "Craps": {"2": {}, "3": {}, "11": {}, "12": {}}
                     }

    def bet_pass(self, player: Player, bet_value: int):
        """ Adds player bet to table for Pass Line """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif self.table.point_on:
            return bet_off_comeout_roll(player.name)

        player.chips -= bet_value
        if player.name in self.bets["Pass"].keys():
            self.bets["Pass"][player.name] += bet_value
            return f"{player.name} pressed their Pass Line bet to ${self.bets['Pass'][player.name]}.00!"
        else:
            self.bets["Pass"][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Pass Line!"

    def bet_no_pass(self, player: Player, bet_value: int):
        """ Adds player bet to table for No Pass Line """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif self.table.point_on:
            return bet_off_comeout_roll(player.name)

        player.chips -= bet_value
        if player.name in self.bets["No_Pass"].keys():
            self.bets["No_Pass"][player.name] += bet_value
            return f"{player.name} pressed their No Pass Line bet to ${self.bets['No_Pass'][player.name]}.00!"
        else:
            self.bets["No_Pass"][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the No Pass Line!"

    def bet_field(self, player: Player, bet_value: int):
        """ Adds player bet to table for Field """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif not self.table.point_on:
            return bet_on_comeout_roll(player.name)

        player.chips -= bet_value
        if player.name in self.bets["Field"].keys():
            self.bets["Field"][player.name] += bet_value
            return f"{player.name} pressed their Field bet to ${self.bets['Field'][player.name]}.00!"
        else:
            self.bets["Field"][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Field!"

    def bet_odds(self, player: Player, bet_value: int):
        """ Adds player bet to table for Place Odds """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif not self.table.point_on:
            return bet_on_comeout_roll(player.name)
        elif player.name not in self.bets["Pass"].keys():
            return no_pass_bet(player.name)

        player_pass_bet = self.bets["Pass"][player.name]
        if bet_value not in [2*player_pass_bet, 3*player_pass_bet]:
            return f"{player.name}, your Odds bet must be 2x or 3x your Pass bet!"

        player.chips -= bet_value
        if player.name in self.bets["Odds"].keys():
            self.bets["Odds"][player.name] += bet_value
            return f"{player.name} pressed their Odds bet to ${self.bets['Odds'][player.name]}.00!"
        else:
            self.bets["Odds"][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Odds!"

    def bet_place(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Place Bets """
        if bet_target not in ["4", "5", "6", "8", "9", "10"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Place bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.name in self.bets["Place"][bet_target].keys():
            self.bets["Place"][bet_target][player.name] += bet_value
            return f"{player.name} pressed their Place {bet_target} bet to ${self.bets['Place'][player.name]}.00!"
        else:
            self.bets["Place"][bet_target][player.name] = bet_value
            return f"{player.name} has made a Place bet of {bet_value}.00 on {bet_target}!"

    def bet_buy(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Buy Bets """
        if bet_target not in ["4", "5", "6", "8", "9", "10"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Buy bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.name in self.bets["Buy"][bet_target].keys():
            self.bets["Buy"][bet_target][player.name] += bet_value
            return f"{player.name} pressed their Buy {bet_target} bet to ${self.bets['Buy'][player.name]}.00!"
        else:
            self.bets["Buy"][bet_target][player.name] = bet_value
            return f"{player.name} has made a Buy bet of {bet_value}.00 on {bet_target}!"

    def bet_big(self, player: Player, bet_value: int):
        """ Adds player bet to table for Big 6|8 """
        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.name in self.bets["Big"].keys():
            self.bets["Big"][player.name] += bet_value
            return f"{player.name} pressed their Big 6|8 bet to ${self.bets['Big'][player.name]}.00!"
        else:
            self.bets["Big"][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Big 6|8!"

    def bet_hardway(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Hard Roll bets """
        if bet_target not in ["4", "6", "8", "10"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Hardway Bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.name in self.bets["Hardway"][bet_target].keys():
            self.bets["Hardway"][bet_target][player.name] += bet_value
            return f"{player.name} pressed their Hard {bet_target} bet to ${self.bets['Hardway'][bet_target][player.name]}.00!"
        else:
            self.bets["Hardway"][bet_target][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Hard {bet_target}"

    def bet_seven(self, player: Player, bet_value: int):
        """ Adds player bet to table for Any Seven"""
        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.name in self.bets["Seven"].keys():
            self.bets["Seven"][player.name] += bet_value
            return f"{player.name} pressed their Any 7 bet to ${self.bets['Big'][player.name]}.00!"
        else:
            self.bets["Seven"][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Any 7!"

    def bet_craps(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Craps Roll bets """
        if bet_target not in ["2", "3", "11", "12"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Craps Bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.name in self.bets["Craps"][bet_target].keys():
            self.bets["Craps"][bet_target][player.name] += bet_value
            return f"{player.name} pressed their Craps {bet_target} bet to ${self.bets['Craps'][bet_target][player.name]}.00!"
        else:
            self.bets["Craps"][bet_target][player.name] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Craps {bet_target}"

    def clear_all_bets(self):
        self.bets = {"Pass": {}, "No_Pass": {}, "Field": {}, "Odds": {}, "Big": {},
                     "Place": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Buy": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Hardway": {"4": {}, "6": {}, "8": {}, "10": {}},
                     "Seven": {}, "Craps": {"2": {}, "3": {}, "11": {}, "12": {}}
                     }
        return "All Bets Clear!"

