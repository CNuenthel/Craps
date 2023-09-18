# Craps
Craps creates a group of classes that can be utilized to create a craps app. 

## Modules

### craps
Craps is the main app file and just shows the anticipated structure of object creation for the required classes to construct a functional craps table, create players, and operate rolls, bets, and winnings. 

### craps_bets
Holds the CrapsBets class that holds player bets as an attribute for easy access by the main app. CrapsBets takes in player objects and their craps bets, parses them into a central dataset to be accessed while the game operates. This module checks for bet legality and returns text responses if specific bets cannot be made by that player. This class works as the dealer of a craps table who would take and organize your chips upon making a bet.

### craps_stickman
Holds the CrapsPayout and CrapsStickman classes. CrapsStickman takes in the Table and CrapsPayout objects to call out dice rolls on the table and provide the appropriate payout based on bets.

### craps_table
Holds the CrapsTable class which stores player objects and allows dice rolls.

### craps_test
CrapsTest is the unittest test suite for the application. CrapsTest runs bets and payouts and verifies that appropriate data changes are assigned following bets and dice rolls, as well as confirming certain bets are blocked when not authorized. 

### player
Player hols the player class. Simply a player with a name, a number of chips and an ID number.

## Order
To utilize this codebase there is an order of operations to follow to make sure all objects are in place. I'll break that down here.

### Instantiate the table
Create a table utilizing the table class from craps_table -> table = CrapsTable()
The craps table is the root object that will hold all players, their bets, and dice rolls. 

### Create players
Can't play craps without players. Create player objects from player -> user = Player(name=user_name, chips=1000, id=1), or simply Player(user_name, 1000, 1)
You can add players to the table using methods contained in the CrapsTable class (i.e. CrapsTable.add_player(Player(...,))

### Instantiate the bet handler
Craps bets is the bet handler and requires a table. Instantiate the bet handler using the CrapsBets class -> bets = CrapsBets(CrapsTable())
The craps bets object will store player ID and bet amount specified to a bet on the table for payout reference.

### Stickman?
No need to worry about creating the dealer. The table class you made will call the stickman while processing your dice roll, assess the value on the dice and assign payouts based on your bet handler. 

## Play Craps!
You can now have a player roll the dice using the CrapsTable roll_dice method and process the dice rolls using the CrapsTable process_roll method. The stickman will also handle point on and point off operations based on the state of the table and value of the dice. One off bets will be cleared following the roll and running bets will be maintained until dice results clear bets (such as rolling a 7 while the point is on).

Questions, comments, complaints:
[cnuenthel@gmail.com] 
