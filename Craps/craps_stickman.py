from Craps.craps_table import CrapsTable


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