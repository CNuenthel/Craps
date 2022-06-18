import random
from dataclasses import dataclass

from Craps.craps_table import CrapsTable
from Craps.player import Player
from Craps.craps_bets import CrapsBets

c = Player(name="Cody", chips=10000, id=1)
table = CrapsTable()
bet = CrapsBets(table)

table.add_player(c)

bet.bet_pass(c, 10, False)
bet.bet_no_pass(c, 10, False)
bet.bet_field(c, 10, True)
bet.bet_pass_odds(c, 10, True)

nums = ["4", "5", "6", "8", "9", "10"]
for num in nums:
    bet.bet_place(c, 10, num)

bet.bet_big(c, 10)

nums = ["4", "6", "8", "10"]
for num in nums:
    bet.bet_hardway(c, 10, num)

bet.bet_seven(c, 10)

nums = ["2", "3", "11", "12"]
for num in nums:
    bet.bet_craps(c, 10, num)

