import unittest
from craps import Player, CrapsTable, CrapsBets


def create_test_objects():
    player = Player(name="Test", chips=250, id=1)
    table = CrapsTable()
    dealer = CrapsBets(table)
    return player, table, dealer


def need_more_chips_responses(player_name: str):
    return [
            f"Hey {player_name}, you need more dosh to make that bet",
            f"Nice try {player_name}, cash in first to make that bet",
            f"With what chips {player_name}?",
            f"Maybe you should win on a roll before placing chips you dont have {player_name}.",
            f"Get some chips to put on the table first {player_name}"
        ]


def bet_on_comeout_roll_responses(player_name: str):
    return [
        f"{player_name}, hold that bet, the point is on right now. Wait for a new comeout roll"
    ]


def bet_off_comeout_roll_responses(player_name: str):
    return [
        f"{player_name}, you cannot make that bet while the point is off"
    ]


def no_pass_bet_responses(player_name: str):
    return [
        f"{player_name}, you cannot make that bet without a previous pass bet"
    ]


class CrapsDealerTestCase(unittest.TestCase):
    def test_ok(self):
        pass



if __name__ == '__main__':
    unittest.main()
