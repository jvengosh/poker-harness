from player import Player
from harness import *
from strategy import DefaultStrategy

from Alpha import Winning
from SuperiorBOTO import SuperiorStrategy
from Manifest import Manifest

# Entry Point
def main():
    # Create four players with default strategies
    player_0 = Player("Alpha", strategy=Winning())
    player_1 = Player("SuperiorBOTO", strategy=SuperiorStrategy())
    player_2 = Player("Manifest", strategy=Manifest())
    players = [player_0, player_1, player_2]

    matches = 50
    num_hands = 100  # For example, to play 10 hands
    current_hand = 1
    blind = 20  # Starting blind, could increase as hands go by

    win = [0, 0, 0]

    for match in range(matches):
        while current_hand <= num_hands and not game_over(players):
            print(f"Hand {current_hand} begins.")
            pot = Pot()
            deck = Deck()
            deck.shuffle()

            # Assign dealer position that rotates each hand
            dealer = (current_hand - 1) % len(players)  # This will rotate the dealer position

            play_hand(players, dealer, deck, pot, blind)

            current_hand += 1
            # Optional: Increase blinds at intervals or based on conditions
            # Optional: Check and remove any players out of chips from the player list

        # End game summary
        chips = [0, 0, 0]

        print("\nGame over. Final chip counts:")
        for player in range(len(players)):
            print(f"{players[player].name}: {players[player].chips} chips")
            chips[player] = players[player].chips

            players[player].hard_reset(players[player].name, players[player].strategy)
    
        winner = chips.index(max(chips))

        win[winner] += 1
        current_hand = 1
        
    
    print("\n")
    for player in range(len(players)):
        print(f"{players[player].name}: {win[player]}")


def play_hand(players, dealer, deck, pot, blind):
    """Plays out a single hand of poker."""
    print("\nPreflop")
    output = preflop(players, dealer, deck, pot, blind)
    
    if (output == 1):
        players[-1].chips += pot.chips
        print(players[-1].name + " won " + str(pot.chips) + " chips!")
        round_end(players)
        return
    else:
        print(output)

    print("\nFlop")
    betting_round(players, pot, deck, blind, "flop")

    if (output == 1):
        players[-1].chips += pot.chips
        print(players[-1].name + " won " + str(pot.chips) + " chips!")
        round_end(players)
        return
    else:
        print(output)

    print("\nTurn")
    betting_round(players, pot, deck, blind, "turn")

    if (output == 1):
        players[-1].chips += pot.chips
        print(players[-1].name + " won " + str(pot.chips) + " chips!")
        round_end(players)
        return
    else:
        print(output)

    print("\nRiver")
    betting_round(players, pot, deck, blind, "river")

    if (output == 1):
        players[-1].chips += pot.chips
        print(players[-1].name + " won " + str(pot.chips) + " chips!")
        round_end(players)
        return
    else:
        print(output)

    # Create a list to store side pots
    side_pots = []

    # Determine if there are players who went all-in
    all_in_players = [player for player in players if player.round_bet > 0 and not player.fold]

    if all_in_players:
        # Handle side pots and continue the game with the last side pot
        last_side_pot = handle_side_pots(players, all_in_players, pot)
        side_pots.append(last_side_pot)

    showdown(players, pot)

    round_end(players)

    return


def round_end(players):
    # Reset player states for the next hand
    for player in players:
        player.reset()  # Ensure this method resets only hand-specific states, not chip counts
        print(f"{player.name}: {player.chips} chips")

def game_over(players):
    """Returns True if the game is over (i.e., only one player left with all chips)."""
    return sum(player.chips > 0 for player in players) <= 1


if __name__ == "__main__":
    main()
    # Good Luck :)