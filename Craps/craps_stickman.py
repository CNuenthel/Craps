
class CrapsPayouts:
    def __init__(self, table):
        self.table = table

    def pass_payout(self):
        """ Pays out a winning bet on the Pass Line """
        payouts = []

        for bet_id in self.table.bets["Pass"]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["Pass"][bet_id]
            payout = player_bet
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their No Pass wager!")

        return payouts

    def no_pass_payout(self):
        """ Pays out a winning bet on the Don't Pass Line """
        payouts = []

        for bet_id in self.table.bets["No_Pass"]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["No_Pass"][bet_id]
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

        for bet_id in self.table.bets["Field"]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["Field"][bet_id]
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

        for bet_id in self.table.bets["Odds"]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["Odds"][bet_id]
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

        for bet_id in self.table.bets["Place"][point_num]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["Place"][point_num][bet_id]
            payout = round(player_bet * multiplier, 2)
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Place {point_num} wager!")

        return payouts

    def big_68_payout(self):
        """ Pays out a winning bet for Big 6|8 """
        payouts = []

        for bet_id in self.table.bets["Big"]:
            player = self.table.find_player(bet_id)
            payout = self.table.bets["Big"][bet_id]
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

        for bet_id in self.table.bets["Hardway"][hardway_num]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["Hardway"][hardway_num][bet_id]
            payout = player_bet * multiplier
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Hard {hardway_num} wager!")

        return payouts

    def seven_payout(self):
        payouts = []

        for id in self.table.bets["No_Pass"]:
            player = self.table.find_player(id)
            payout = self.table.bets["Seven"][id] * 4
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

        for bet_id in self.table.bets["Craps"][craps_roll]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["Craps"][craps_roll][bet_id]
            payout = player_bet * multiplier
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Craps wager!")

        for bet_id in self.table.bets["Craps"]["Any"]:
            player = self.table.find_player(bet_id)
            player_bet = self.table.bets["Craps"]["Any"][bet_id]
            payout = player_bet * 7
            player.chips += payout
            payouts.append(f"{player.name} won ${payout} on their Craps wager!")


class CrapsStickman:
    """ Calls dice result and requests appropriate payout """
    def __init__(self, table):
        self.payout = CrapsPayouts(table)
        self.bets = table.bets

    def flatten_payouts(self, *args):
        master = [payout for inner_payout in args for payout in inner_payout if payout]
        return master

    def snake_eyes(self, point_on: bool):
        """ Processes payout for a roll of Snake Eyes """
        pass_payout = [None]
        if not point_on:
            pass_payout = self.payout.pass_payout()

        field_payout = self.payout.field_payout(double_indicator=True)
        craps_payout = self.payout.craps_payout("2")

        return self.flatten_payouts(pass_payout, field_payout, craps_payout)

    def ace_deuce(self, point_on: bool):
        """ Processes payout for a roll of Ace Deuce """
        no_pass_payout = [None]
        if not point_on:
            no_pass_payout = self.payout.no_pass_payout()

        craps_payout = self.payout.craps_payout("3")
        field_payout = self.payout.field_payout(double_indicator=False)

        return self.flatten_payouts(no_pass_payout, craps_payout, field_payout)

    def four(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Four """
        hardway_payout = [None]
        if roll == (2, 2):
            hardway_payout = self.payout.hardway_payout("4")

        pass_payout = [None]
        if point_on:
            pass_payout = self.payout.pass_payout()

        return self.flatten_payouts(hardway_payout, pass_payout)

    def five(self, point_on: bool):
        """ Processes payout for a roll of Five """
        pass_payout = [None]
        if point_on:
            pass_payout = self.payout.pass_payout()

        place_payout = self.payout.place_payout("5")

        return self.flatten_payouts(pass_payout, place_payout)

    def six(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Six """
        hardway_payout = [None]
        if roll == (3, 3):
            hardway_payout = self.payout.hardway_payout("6")

        pass_payout = [None]
        if point_on:
            pass_payout = self.payout.pass_payout()

        place_payout = self.payout.place_payout("6")

        return self.flatten_payouts(hardway_payout, pass_payout, place_payout)

    def seven(self, point_on: bool):
        """ Processes payout for a roll of Seven """
        seven_payout = [None]
        if not point_on:
            return self.flatten_payouts(self.payout.pass_payout())

        elif point_on:
            seven_payout = self.payout.seven_payout()

        return self.flatten_payouts(seven_payout)

    def eight(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Eight """
        hardway_payout = [None]
        if roll == (4, 4):
            hardway_payout = self.payout.hardway_payout("8")

        pass_payout = [None]
        if point_on:
            pass_payout = self.payout.pass_payout()

        place_payout = self.payout.place_payout("8")

        return self.flatten_payouts(hardway_payout, pass_payout, place_payout)

    def nine(self, point_on: bool):
        """ Processes payout for a roll of Nine """
        pass_payout = [None]
        if point_on:
            pass_payout = self.payout.pass_payout()

        field_payout = self.payout.field_payout(double_indicator=False)
        place_payout = self.payout.place_payout("9")


        return self.flatten_payouts(pass_payout, field_payout, place_payout)

    def ten(self, roll: tuple, point_on: bool):
        """ Processes payout for a roll of Ten """
        hardway_payout = [None]
        if roll == (5, 5):
            hardway_payout = self.payout.hardway_payout("10")

        pass_payout = [None]
        if point_on:
            pass_payout = self.payout.pass_payout()

        field_payout = self.payout.field_payout(double_indicator=False)
        place_payout = self.payout.place_payout("10")

        return self.flatten_payouts(hardway_payout, pass_payout, field_payout, place_payout)

    def eleven(self, point_on: bool):
        """ Processes payout for a roll of Eleven """
        pass_payout = [None]
        if not point_on:
            pass_payout = self.payout.pass_payout()

        craps_payout = self.payout.craps_payout("11")
        field_payout = self.payout.field_payout(double_indicator=False)

        return self.flatten_payouts(pass_payout, craps_payout, field_payout)

    def twelve(self, point_on: bool):
        """ Processes payout for a roll of Twelve """
        no_pass_payout = [None]
        if not point_on:
            no_pass_payout = self.payout.no_pass_payout()

        field_payout = self.payout.field_payout(double_indicator=True)
        craps_payout = self.payout.craps_payout("12")

        return self.flatten_payouts(no_pass_payout, field_payout, craps_payout)