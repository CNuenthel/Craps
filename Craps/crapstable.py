import random
from dataclasses import dataclass

# TODO Pop single roll bets after roll

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


class CrapsTable:
    """ Emulates a Craps Table """

    def __init__(self):
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
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def find_player(self, player_id: int):
        for player in self.players:
            if player.id == player_id:
                return player

    def set_point(self, point_num: int):
        self.point_holder = point_num

    def process_roll(self, dice: tuple):
        if dice == (1, 1):
            return
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


class CrapsPayouts:
    def __init__(self, table: CrapsTable, player_bets: dict):
        self.table = table
        self.bets = player_bets

    def pass_payout(self):
        """ Pays out a winning bet on the Pass Line """
        payouts = []

        for bet_id in self.bets["Pass"]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["Pass"][bet_id]
            payout = player_bet
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their No Pass wager!")

        return payouts

    def no_pass_payout(self):
        """ Pays out a winning bet on the Don't Pass Line """
        payouts = []

        for bet_id in self.bets["No_Pass"]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["No_Pass"][bet_id]
            payout = player_bet
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their No Pass wager!")

        return payouts

    def field_payout(self, double_indicator: bool):
        """ Pays out a winning bet on the Field """
        if double_indicator:
            multiplier = 2
        else:
            multiplier = 1

        payouts = []

        for bet_id in self.bets["Field"]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["Field"][bet_id]
            payout = player_bet * multiplier
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Field wager!")

        return payouts

    def buy_odds_payout(self, point_num: int):
        """ Pays out a winning bet for Odds, must verify that point"""
        if point_num in [4, 10]:
            multiplier = 2
        elif point_num in [5, 9]:
            multiplier = 1.5
        elif point_num in [6, 8]:
            multiplier = 1.2
        else:
            raise ValueError(f"Point number {point_num} is an invalid selection for Odds Payout")

        payouts = []

        for bet_id in self.bets["Odds"]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["Odds"][bet_id]
            payout = round(player_bet * multiplier, 2)
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Buy Odds {point_num} wager!")

        return payouts

    def place_payout(self, point_num: str):
        """ Pays out a winning bet for Place """
        if point_num in ["4", "10"]:
            multiplier = 1.8
        elif point_num in ["5", "9"]:
            multiplier = 1.4
        elif point_num in ["6", "8"]:
            multiplier = 1.17
        else:
            raise ValueError(f"Point number {point_num} is an invalid selection for Place Payout")

        payouts = []

        for bet_id in self.bets["Place"][point_num]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["Place"][point_num][bet_id]
            payout = round(player_bet * multiplier, 2)
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Place {point_num} wager!")

        return payouts

    def big_68_payout(self):
        """ Pays out a winning bet for Big 6|8 """
        payouts = []

        for bet_id in self.bets["Big"]:
            player = self.table.find_player(bet_id)
            payout = self.bets["Big"][bet_id]
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Big 6|8 wager!")

        return payouts

    def hardway_payout(self, hardway_num: str):
        """ Pays out a winning bet for Hardway"""
        if hardway_num in ["6", "8"]:
            multiplier = 9
        elif hardway_num in ["4", "10"]:
            multiplier = 7
        else:
            raise ValueError(f"Hardway number {hardway_num} is an invalid selection for Hardway Payout")

        payouts = []

        for bet_id in self.bets["Hardway"][hardway_num]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["Hardway"][hardway_num][bet_id]
            payout = player_bet * multiplier
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Hard {hardway_num} wager!")

        return payouts

    def seven_payout(self):
        payouts = []

        for id in self.bets["No_Pass"]:
            player = self.table.find_player(id)
            payout = self.bets["Seven"][id] * 4
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Seven wager!")

        return payouts

    def craps_payout(self, craps_roll: str):
        if craps_roll in ["2", "12"]:
            multiplier = 30
        elif craps_roll in ["3", "11"]:
            multiplier = 15
        else:
            raise ValueError(f"Number provided for Craps Roll is invalid: {craps_roll}")

        payouts = []

        for bet_id in self.bets["Craps"][craps_roll]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["Craps"][craps_roll][bet_id]
            payout = player_bet * multiplier
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Craps wager!")

        for bet_id in self.bets["Craps"]["Any"]:
            player = self.table.find_player(bet_id)
            player_bet = self.bets["Craps"]["Any"][bet_id]
            payout = player_bet * 7
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Craps wager!")


class CrapsStickman:
    def __init__(self, payout: CrapsPayouts, player_bets: dict):
        self.payout = payout
        self.bets = player_bets

    def snake_eyes(self, point_on: bool):
        """ Processes payout for a roll of Snake Eyes """
        payouts = []

        if not point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.field_payout(double_indicator=True))
        payouts.append(self.payout.craps_payout("2"))

        return payouts

    def ace_deuce(self, point_on: bool):
        """ Processes payout for a roll of Ace Deuce """
        payouts = []

        if not point_on:
            payouts.append(self.payout.no_pass_payout())

        payouts.append(self.payout.craps_payout("3"))
        payouts.append(self.payout.field_payout(double_indicator=False))

        return payouts

    def four(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Four """
        payouts = []

        if roll == (2, 2):
            payouts.append(self.payout.hardway_payout("4"))

        if point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.place_payout("4"))
        payouts.append(self.payout.field_payout(double_indicator=False))

        return payouts

    def five(self, point_on: bool):
        """ Processes payout for a roll of Five """
        payouts = []

        if point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.place_payout("5"))

        return payouts

    def six(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Six """
        payouts = []

        if roll == (3, 3):
            payouts.append(self.payout.hardway_payout("6"))
        if point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.place_payout("6"))

        return payouts

    def seven(self, point_on: bool):
        """ Processes payout for a roll of Seven """
        payouts = []

        if not point_on:
            payouts.append(self.payout.pass_payout())
            return
        elif point_on:
            payouts.append(self.payout.seven_payout())

        return payouts

    def eight(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Eight """
        payouts = []

        if roll == (4, 4):
            payouts.append(self.payout.hardway_payout("8"))
        if point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.place_payout("8"))

        return payouts

    def nine(self, point_on: bool):
        """ Processes payout for a roll of Nine """
        payouts = []

        if point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.field_payout(double_indicator=False))
        payouts.append(self.payout.place_payout("9"))

        return payouts

    def ten(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Ten """
        payouts = []

        if roll == (5, 5):
            payouts.append(self.payout.hardway_payout("10"))
        if point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.field_payout(double_indicator=False))
        payouts.append(self.payout.place_payout("10"))

        return payouts

    def eleven(self, point_on: bool):
        """ Processes payout for a roll of Eleven """
        payouts = []

        if not point_on:
            payouts.append(self.payout.pass_payout())

        payouts.append(self.payout.craps_payout("11"))
        payouts.append(self.payout.field_payout(double_indicator=False))

        return payouts

    def twelve(self, point_on: bool):
        """ Processes payout for a roll of Twelve """
        payouts = []

        if not point_on:
            payouts.append(self.payout.no_pass_payout())

        payouts.append(self.payout.field_payout(double_indicator=True))
        payouts.append(self.payout.craps_payout("12"))

        return payouts


class CrapsDealer:
    """ Bet controller for Craps table """

    def __init__(self):
        self.bets = {"Pass": {}, "No_Pass": {}, "Field": {}, "Odds": {}, "Big": {},
                     "Place": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Buy": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Hardway": {"4": {}, "6": {}, "8": {}, "10": {}},
                     "Seven": {}, "Craps": {"2": {}, "3": {}, "11": {}, "12": {}, "Any": {}}
                     }

    def bet_pass(self, player: Player, bet_value: int, point_on: bool):
        """ Adds player bet to table for Pass Line """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif point_on:
            return bet_off_comeout_roll(player.name)

        player.chips -= bet_value
        if player.id in self.bets["Pass"].keys():
            self.bets["Pass"][player.id] += bet_value
            return f"{player.name} pressed their Pass Line bet to ${self.bets['Pass'][player.id]}.00!"
        else:
            self.bets["Pass"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Pass Line!"

    def bet_no_pass(self, player: Player, bet_value: int, point_on: bool):
        """ Adds player bet to table for No Pass Line """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif point_on:
            return bet_off_comeout_roll(player.name)

        player.chips -= bet_value
        if player.id in self.bets["No_Pass"].keys():
            self.bets["No_Pass"][player.id] += bet_value
            return f"{player.name} pressed their No Pass Line bet to ${self.bets['No_Pass'][player.id]}.00!"
        else:
            self.bets["No_Pass"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the No Pass Line!"

    def bet_field(self, player: Player, bet_value: int, point_on: bool):
        """ Adds player bet to table for Field """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif not point_on:
            return bet_on_comeout_roll(player.name)

        player.chips -= bet_value
        if player.id in self.bets["Field"].keys():
            self.bets["Field"][player.id] += bet_value
            return f"{player.name} pressed their Field bet to ${self.bets['Field'][player.id]}.00!"
        else:
            self.bets["Field"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Field!"

    def bet_pass_odds(self, player: Player, bet_value: int, point_on: bool):
        """ Adds player bet to table for Place Odds """
        if player.chips <= bet_value:
            return need_more_chips(player.name)
        elif not point_on:
            return bet_on_comeout_roll(player.name)
        elif player.id not in self.bets["Pass"].keys():
            return no_pass_bet(player.name)

        player_pass_bet = self.bets["Pass"][player.id]
        if bet_value not in [2 * player_pass_bet, 3 * player_pass_bet]:
            return f"{player.name}, your Odds bet must be 2x or 3x your Pass bet!"

        player.chips -= bet_value
        if player.id in self.bets["Odds"].keys():
            self.bets["Odds"][player.id] += bet_value
            return f"{player.name} pressed their Odds bet to ${self.bets['Odds'][player.id]}.00!"
        else:
            self.bets["Odds"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on the Odds!"

    def bet_place(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Place Bets """
        if bet_target not in ["4", "5", "6", "8", "9", "10"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Place bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.bets["Place"][bet_target].keys():
            self.bets["Place"][bet_target][player.id] += bet_value
            return f"{player.name} pressed their Place {bet_target} bet to ${self.bets['Place'][player.id]}.00!"
        else:
            self.bets["Place"][bet_target][player.id] = bet_value
            return f"{player.name} has made a Place bet of {bet_value}.00 on {bet_target}!"

    # def bet_buy(self, player: Player, bet_value: int, bet_target: str):
    #     """ Adds player bet to table for Buy Bets """
    #     if bet_target not in ["4", "5", "6", "8", "9", "10"]:
    #         raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Buy bet")
    #
    #     if player.chips <= bet_value:
    #         return need_more_chips(player.name)
    #
    #     player.chips -= bet_value
    #
    #     if player.name in self.bets["Buy"][bet_target].keys():
    #         self.bets["Buy"][bet_target][player.name] += bet_value
    #         return f"{player.name} pressed their Buy {bet_target} bet to ${self.bets['Buy'][player.name]}.00!"
    #     else:
    #         self.bets["Buy"][bet_target][player.name] = bet_value
    #         return f"{player.name} has made a Buy bet of {bet_value}.00 on {bet_target}!"

    def bet_big(self, player: Player, bet_value: int):
        """ Adds player bet to table for Big 6|8 """
        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.bets["Big"].keys():
            self.bets["Big"][player.id] += bet_value
            return f"{player.name} pressed their Big 6|8 bet to ${self.bets['Big'][player.id]}.00!"
        else:
            self.bets["Big"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Big 6|8!"

    def bet_hardway(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Hard Roll bets """
        if bet_target not in ["4", "6", "8", "10"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Hardway Bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.bets["Hardway"][bet_target].keys():
            self.bets["Hardway"][bet_target][player.id] += bet_value
            return f"{player.name} pressed their Hard {bet_target} bet to ${self.bets['Hardway'][bet_target][player.id]}.00!"
        else:
            self.bets["Hardway"][bet_target][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Hard {bet_target}"

    def bet_seven(self, player: Player, bet_value: int):
        """ Adds player bet to table for Any Seven"""
        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.bets["Seven"].keys():
            self.bets["Seven"][player.id] += bet_value
            return f"{player.name} pressed their Any 7 bet to ${self.bets['Big'][player.id]}.00!"
        else:
            self.bets["Seven"][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Any 7!"

    def bet_craps(self, player: Player, bet_value: int, bet_target: str):
        """ Adds player bet to table for Craps Roll bets """
        if bet_target not in ["2", "3", "11", "12"]:
            raise ValueError(f"Bet Target {bet_target} is an invalid target to make a Craps Bet")

        if player.chips <= bet_value:
            return need_more_chips(player.name)

        player.chips -= bet_value

        if player.id in self.bets["Craps"][bet_target].keys():
            self.bets["Craps"][bet_target][player.id] += bet_value
            return f"{player.name} pressed their Craps {bet_target} bet to ${self.bets['Craps'][bet_target][player.id]}.00!"
        else:
            self.bets["Craps"][bet_target][player.id] = bet_value
            return f"{player.name} has bet ${bet_value}.00 on Craps {bet_target}"

    def clear_all_bets(self):
        self.bets = {"Pass": {}, "No_Pass": {}, "Field": {}, "Odds": {}, "Big": {},
                     "Place": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Buy": {"4": {}, "5": {}, "6": {}, "8": {}, "9": {}, "10": {}},
                     "Hardway": {"4": {}, "6": {}, "8": {}, "10": {}},
                     "Seven": {}, "Craps": {"2": {}, "3": {}, "11": {}, "12": {}}
                     }
        return "All Bets Clear!"
