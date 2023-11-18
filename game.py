from player import Player
from harness import *
from strategy import DefaultStrategy

# Entry Point
def main():
    # Create four players with default strategies
    player_0 = Player("Alpha", strategy=DefaultStrategy())
    player_1 = Player("Bravo", strategy=DefaultStrategy())
    player_2 = Player("Charlie", strategy=DefaultStrategy())
    player_3 = Player("Delta", strategy=DefaultStrategy())
    players = [player_0, player_1, player_2, player_3]

    num_hands = 1  # For example, to play 10 hands
    current_hand = 1
    blind = 20  # Starting blind, could increase as hands go by

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
    print("\nGame over. Final chip counts:")
    for player in players:
        print(f"{player.name}: {player.chips} chips")


def play_hand(players, dealer, deck, pot, blind):
    """Plays out a single hand of poker."""
    print("\nPreflop")
    preflop(players, dealer, deck, pot, blind)
    print("\nFlop")
    betting_round(players, pot, deck, blind, "flop")
    print("\nTurn")
    betting_round(players, pot, deck, blind, "turn")
    print("\nRiver")
    betting_round(players, pot, deck, blind, "river")

    # Create a list to store side pots
    side_pots = []

    # Determine if there are players who went all-in
    all_in_players = [player for player in players if player.round_bet > 0 and not player.fold]

    if all_in_players:
        # Handle side pots and continue the game with the last side pot
        last_side_pot = handle_side_pots(players, all_in_players, pot)
        side_pots.append(last_side_pot)

    showdown(players, pot)

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