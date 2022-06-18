import random
from Craps.player import Player



def need_more_chips(player_name: str):
    """ Returns a random response to a player betting more chips than they have """
    responses = [
        f"Hey {player_name}, you need more dosh to make that bet"
        # f"Nice try {player_name}, cash in first to make that bet",
        # f"With what chips {player_name}?",
        # f"Maybe you should win on a roll before placing chips you dont have {player_name}.",
        # f"Get some chips to put on the table first {player_name}"
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


class CrapsBets:
    """ Bet controller for Craps table """

    def __init__(self, table):
        self.table = table

    def bet_pass(self, player: Player, bet_value: int, point_on: bool):
        """ Adds player bet to table for Pass Line """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif point_on:
            return bet_off_comeout_roll(player.name)

        player.chips -= bet_value
        if player.id in self.table.bets["Pass"].keys():
            self.table.bets["Pass"][player.id] += bet_value
            return f"{player.name} pressed their Pass Line bet to ${self.table.bets['Pass'][player.id]}.00!"
        else:
            self.table.bets["Pass"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Pass Line!"

    def bet_no_pass(self, player: Player, bet_value: int, point_on: bool):
        """ Adds player bet to table for No Pass Line """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif point_on:
            return bet_off_comeout_roll(player.name)

        player.chips -= bet_value
        if player.id in self.table.bets["No_Pass"].keys():
            self.table.bets["No_Pass"][player.id] += bet_value
            return f"{player.name} pressed their No Pass Line bet to ${self.table.bets['No_Pass'][player.id]}.00!"
        else:
            self.table.bets["No_Pass"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the No Pass Line!"

    def bet_field(self, player: Player, bet_value: int):
        """ Adds player bet to table for Field """
        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value
        if player.id in self.table.bets["Field"].keys():
            self.table.bets["Field"][player.id] += bet_value
            return f"{player.name} pressed their Field bet to ${self.table.bets['Field'][player.id]}.00!"
        else:
            self.table.bets["Field"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Field!"

    def bet_pass_odds(self, player: Player, bet_value: int, point_on: bool):
        """ Adds player bet to table for Place Odds """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif not point_on:
            return bet_on_comeout_roll(player.name)
        elif player.id not in self.table.bets["Pass"].keys():
            return no_pass_bet(player.name)

        player.chips -= bet_value
        if player.id in self.table.bets["Odds"].keys():
            self.table.bets["Odds"][player.id] += bet_value
            return f"{player.name} pressed their Odds bet to ${self.table.bets['Odds'][player.id]}.00!"
        else:
            self.table.bets["Odds"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Odds!"

    def bet_place(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Place Bets """
        if bet_target not in ["4", "5", "6", "8", "9", "10"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Place bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.table.bets["Place"][bet_target].keys():
            self.table.bets["Place"][bet_target][player.id] += bet_value
            return f"{player.name} pressed their Place {bet_target} bet to ${self.table.bets['Place'][bet_target][player.id]}.00!"
        else:
            self.table.bets["Place"][bet_target][player.id] = bet_value
            return f"{player.name} has made a Place bet of {bet_value}.00 on {bet_target}!"

    def bet_big(self, player: Player, bet_value: int):
        """ Adds player bet to table for Big 6|8 """
        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.table.bets["Big"].keys():
            self.table.bets["Big"][player.id] += bet_value
            return f"{player.name} pressed their Big 6|8 bet to ${self.table.bets['Big'][player.id]}.00!"
        else:
            self.table.bets["Big"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Big 6|8!"

    def bet_hardway(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Hard Roll bets """
        if bet_target not in ["4", "6", "8", "10"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Hardway Bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.table.bets["Hardway"][bet_target].keys():
            self.table.bets["Hardway"][bet_target][player.id] += bet_value
            return f"{player.name} pressed their Hard {bet_target} bet to ${self.table.bets['Hardway'][bet_target][player.id]}.00!"
        else:
            self.table.bets["Hardway"][bet_target][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Hard {bet_target}"

    def bet_seven(self, player: Player, bet_value: int):
        """ Adds player bet to table for Any Seven"""
        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.table.bets["Seven"].keys():
            self.table.bets["Seven"][player.id] += bet_value
            return f"{player.name} pressed their Any 7 bet to ${self.table.bets['Seven'][player.id]}.00!"
        else:
            self.table.bets["Seven"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Any 7!"

    def bet_craps(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Craps Roll bets """
        if bet_target not in ["2", "3", "11", "12"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Craps Bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.table.bets["Craps"][bet_target].keys():
            self.table.bets["Craps"][bet_target][player.id] += bet_value
            return f"{player.name} pressed their Craps {bet_target} bet to ${self.table.bets['Craps'][bet_target][player.id]}.00!"
        else:
            self.table.bets["Craps"][bet_target][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Craps {bet_target}"

    def clear_all_bets(self):
        """ Clears all bets from the table """
        self.table.bets = {"Pass": {}, "No_Pass": {}, "Field": {}, "Odds": {}, "Big": {},
                     "Place": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Buy": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Hardway": {"4": {}, "6": {}, "8": {}, "10": {}},
                     "Seven": {}, "Craps": {"2": {}, "3": {}, "11": {}, "12": {}}
                     }
        return "All Bets Clear!"

    def clear_single_roll_bets(self):
        """ Clears all single roll bets from the table """
        self.table.bets["Field"] = {}
        self.table.bets["Seven"] = {}
        for item in self.table.bets["Craps"].keys():
            self.table.bets["Craps"][item] = {}


