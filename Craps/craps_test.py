import unittest
from Craps.player import Player
from Craps.craps_bets import CrapsBets
from Craps.craps_table import CrapsTable

def create_test_objects():
    player = Player(name="Test", chips=10000, id=1)
    table = CrapsTable()
    dealer = CrapsBets(table)
    return player, table, dealer


def place_bets(bet_handler, player):
    bet_handler.bet_pass(player, 10, False)
    bet_handler.bet_no_pass(player, 10, False)
    bet_handler.bet_field(player, 10)
    bet_handler.bet_pass_odds(player, 10, True)

    nums = ["4", "5", "6", "8", "9", "10"]
    for num in nums:
        bet_handler.bet_place(player, 10, num)

    bet_handler.bet_big(player, 10)

    nums = ["4", "6", "8", "10"]
    for num in nums:
        bet_handler.bet_hardway(player, 10, num)

    bet_handler.bet_seven(player, 10)

    nums = ["2", "3", "11", "12"]
    for num in nums:
        bet_handler.bet_craps(player, 10, num)


class CrapsTableTest(unittest.TestCase):

    def test_add_player(self):
        player, table, dealer = create_test_objects()
        table.add_player(player)

        # Verify player is added to player list
        self.assertIn(player, table.players, "ADD PLAYER: Player was not added to table player list")

    def test_remove_player(self):
        player, table, dealer = create_test_objects()
        table.add_player(player)
        table.remove_player(player)

        # Verify player list is not empty
        self.assertTrue(player not in table.players, "REMOVE PLAYER: Player was not removed from table players")

    def test_find_player(self):
        player, table, dealer = create_test_objects()
        table.add_player(player)

        # Verify player is found using the find player method
        self.assertEqual(table.find_player(1), player, "FIND PLAYER: Player was not found in table players")

    def test_set_point(self):
        player, table, dealer = create_test_objects()
        table.set_point(9)

        # Verify point set to desired number
        self.assertEqual(table.point_holder, 9, "SET POINT: Point was set to the wrong value")

    def test_process_roll(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)
        place_bets(bet_handler, player)

        table.dice_roll = (1, 1)



class CrapsBetsTest(unittest.TestCase):

    def test_bet_pass(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_pass(player, 999999, False)
        point_on = bet_handler.bet_pass(player, 10, True)
        proper_bet = bet_handler.bet_pass(player, 10, False)
        press_bet = bet_handler.bet_pass(player, 10, False)

        self.assertEqual(point_on, f"{player.name}, hold that bet, the point is on right now. Wait for a new comeout roll")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on the Pass Line!")
        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(press_bet, f"{player.name} pressed their Pass Line bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["Pass"].keys())

    def test_no_pass(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_no_pass(player, 999999, False)
        point_on = bet_handler.bet_no_pass(player, 10, True)
        proper_bet = bet_handler.bet_no_pass(player, 10, False)
        press_bet = bet_handler.bet_no_pass(player, 10, False)

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(point_on, f"{player.name}, hold that bet, the point is on right now. Wait for a new comeout roll")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on the No Pass Line!")
        self.assertEqual(press_bet, f"{player.name} pressed their No Pass Line bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["No_Pass"].keys())

    def test_bet_field(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_field(player, 999999)
        proper_bet = bet_handler.bet_field(player, 10)
        press_bet = bet_handler.bet_field(player, 10)

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on the Field!")
        self.assertEqual(press_bet, f"{player.name} pressed their Field bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["Field"].keys())

    def test_bet_pass_odds(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_pass_odds(player, 999999, True)
        point_off = bet_handler.bet_pass_odds(player, 10, False)
        no_pass_bet = bet_handler.bet_pass_odds(player, 10, True)

        # Make a pass bet to allow proper bet
        bet_handler.bet_pass(player, 10, False)

        proper_bet = bet_handler.bet_pass_odds(player, 10, True)
        press_bet = bet_handler.bet_pass_odds(player, 10, True)

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(point_off, f"{player.name}, you cannot make that bet while the point is off")
        self.assertEqual(no_pass_bet, f"{player.name}, you cannot make that bet without a previous pass bet")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on the Odds!")
        self.assertEqual(press_bet, f"{player.name} pressed their Odds bet to $20.00!")
        self.assertEqual(player.chips, 9970)
        self.assertIn(player.id, table.bets["Odds"].keys())

    def test_bet_place(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_place(player, 999999, "4")
        proper_bet = bet_handler.bet_place(player, 10, "4")
        press_bet = bet_handler.bet_place(player, 10, "4")

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(proper_bet, f"{player.name} has made a Place bet of 10.00 on 4!")
        self.assertEqual(press_bet, f"{player.name} pressed their Place 4 bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["Place"]["4"].keys())

    def test_bet_big(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_big(player, 999999)
        proper_bet = bet_handler.bet_big(player, 10)
        press_bet = bet_handler.bet_big(player, 10)

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on Big 6|8!")
        self.assertEqual(press_bet, f"{player.name} pressed their Big 6|8 bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["Big"].keys())

    def test_bet_hardway(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_hardway(player, 999999, "4")
        proper_bet = bet_handler.bet_hardway(player, 10, "4")
        press_bet = bet_handler.bet_hardway(player, 10, "4")

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on Hard 4")
        self.assertEqual(press_bet, f"{player.name} pressed their Hard 4 bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["Hardway"]["4"].keys())

    def test_bet_seven(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_seven(player, 999999)
        proper_bet = bet_handler.bet_seven(player, 10)
        press_bet = bet_handler.bet_seven(player, 10)

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on Any 7!")
        self.assertEqual(press_bet, f"{player.name} pressed their Any 7 bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["Seven"].keys())

    def test_bet_craps(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        no_chips = bet_handler.bet_craps(player, 999999, "2")
        proper_bet = bet_handler.bet_craps(player, 10, "2")
        press_bet = bet_handler.bet_craps(player, 10, "2")

        self.assertEqual(no_chips, f"Hey {player.name}, you need more dosh to make that bet")
        self.assertEqual(proper_bet, f"{player.name} has bet $10.00 on Craps 2")
        self.assertEqual(press_bet, f"{player.name} pressed their Craps 2 bet to $20.00!")
        self.assertEqual(player.chips, 9980)
        self.assertIn(player.id, table.bets["Craps"]["2"].keys())

    def test_clear_all_bets(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        place_bets(bet_handler, player)

        bet_handler.clear_all_bets()

        for key in table.bets.keys():
            if key in ["Place", "Buy", "Hardway", "Craps"]:
                for subKey in table.bets[key].keys():
                    self.assertFalse(table.bets[key][subKey])
            else:
                self.assertFalse(table.bets[key])

    def test_clear_single_roll_bets(self):
        player, table, dealer = create_test_objects()
        bet_handler = CrapsBets(table)

        place_bets(bet_handler, player)

        bet_handler.clear_single_roll_bets()

        self.assertFalse(table.bets["Field"])
        self.assertFalse(table.bets["Seven"])

        for key in table.bets["Craps"].keys():
            self.assertFalse(table.bets["Craps"][key])

if __name__ == '__main__':
    unittest.main()
