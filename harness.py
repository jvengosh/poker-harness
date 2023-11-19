import math
import random
from itertools import combinations
from collections import OrderedDict

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = 'Hearts Diamonds Clubs Spades'.split()


class SidePot:
    """Represents a side pot in a poker game."""

    def __init__(self, chips, contributing_players):
        """
        Initialize a SidePot object.

        Args:
            chips (int): The chips in the side pot.
            contributing_players (list): List of Player objects contributing to this side pot.
        """
        self.chips = chips
        self.contributing_players = contributing_players


class Pot:
    """Represents the main pot in a poker game."""

    def __init__(self, cards = []):
        """Initialize a Pot object."""
        self.chips = 0
        self.cards = [] if cards == [] else cards

    def reset(self):
        """Reset the pot to its initial state."""
        self.chips = 0
        self.cards = []


class Deck:
    """Represents a deck of playing cards."""

    def __init__(self):
        """Initialize a Deck object and populate it with a standard deck of cards."""
        self.cards = []
        self.reset()

    def reset(self):
        """Reset the deck to its initial state with a standard deck of cards."""
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        self.cards = [(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        """Shuffle the deck to randomize card order."""
        random.shuffle(self.cards)

    def draw(self):
        """
        Draw a card from the deck.

        Returns:
            tuple: A tuple representing the card drawn, e.g., ('Ace', 'Spades').
        """
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def __len__(self):
        """Get the number of remaining cards in the deck."""
        return len(self.cards)


def blinds(big, little, blind):
    """
    Posts blinds for the current hand.

    Args:
        big (Player): The player posting the big blind.
        little (Player): The player posting the little blind.
        blind (int): The blind amount for the current hand.

    Returns:
        int: The total chips posted for blinds.
    """
    big_blind = min(big.chips, blind)
    little_blind = min(little.chips, math.floor(blind / 2))
    big.chips -= big_blind
    big.round_bet = big_blind
    little.chips -= little_blind
    little.round_bet = little_blind
    return big_blind + little_blind


def hand_rank(hand):
    """
    Evaluate the rank of a poker hand.

    Args:
        hand (list of tuple): A list of card tuples representing the hand.

    Returns:
        tuple: A tuple containing the hand rank (integer) and the best hand cards (list of tuples).
    """
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']

    rank_count = {rank: 0 for rank in ranks}
    suit_count = {suit: 0 for suit in suits}
    for card in hand:
        rank, suit = card
        rank_count[rank] += 1
        suit_count[suit] += 1

    # Original Royal Flush Logic ???
    # if all(suit_count[suit] == 5 for suit in suits) and all(rank_count[rank] == 1 for rank in ranks[-5:]):
    # return (10, hand)

    if all(card[1] == hand[0][1] for card in hand):  # All cards are of the same suit
        rank_order = [ranks.index(card[0]) for card in hand]
        rank_order.sort()
        if rank_order == [ranks.index('10'), ranks.index('Jack'), ranks.index('Queen'), ranks.index('King'),
                          ranks.index('Ace')]:
            return (10, hand)

    for suit in suits:
        if suit_count[suit] == 5:
            suited_cards = [card for card in hand if card[1] == suit]
            suited_ranks = sorted([ranks.index(card[0]) for card in suited_cards], reverse=True)
            if len(suited_ranks) == 5 and max(suited_ranks) - min(suited_ranks) == 4:
                return (9, suited_cards)

    for rank, count in rank_count.items():
        if count == 4:
            quads_cards = [card for card in hand if card[0] == rank]
            kicker_card = max((card for card in hand if card[0] != rank), key=lambda x: ranks.index(x[0]))
            return (8, quads_cards + [kicker_card])

    has_three = any(count == 3 for count in rank_count.values())
    has_pair = any(count == 2 for count in rank_count.values())
    if has_three and has_pair:
        three_rank = next(rank for rank, count in rank_count.items() if count == 3)
        pair_rank = next(rank for rank, count in rank_count.items() if count == 2)
        three_cards = [card for card in hand if card[0] == three_rank]
        pair_cards = [card for card in hand if card[0] == pair_rank]
        return (7, three_cards + pair_cards)

    for suit in suits:
        if suit_count[suit] == 5:
            suited_cards = [card for card in hand if card[1] == suit]
            return (6, suited_cards)

    ranks_in_hand = sorted([ranks.index(card[0]) for card in hand], reverse=True)
    if len(set(ranks_in_hand)) == 5 and max(ranks_in_hand) - min(ranks_in_hand) == 4:
        return (5, hand)

    for rank, count in rank_count.items():
        if count == 3:
            trips_cards = [card for card in hand if card[0] == rank]
            kicker_cards = sorted((card for card in hand if card[0] != rank), key=lambda x: ranks.index(x[0]),
                                  reverse=True)[:2]
            return (4, trips_cards + kicker_cards)

    pairs = [rank for rank, count in rank_count.items() if count == 2]
    if len(pairs) == 2:
        pairs.sort(key=lambda x: ranks.index(x), reverse=True)
        pair1_cards = [card for card in hand if card[0] == pairs[0]]
        pair2_cards = [card for card in hand if card[0] == pairs[1]]
        kicker_card = max((card for card in hand if card[0] not in pairs), key=lambda x: ranks.index(x[0]))
        return (3, pair1_cards + pair2_cards + [kicker_card])

    if len(pairs) == 1:
        pair_cards = [card for card in hand if card[0] == pairs[0]]
        kicker_cards = sorted((card for card in hand if card[0] != pairs[0]), key=lambda x: ranks.index(x[0]),
                              reverse=True)[:3]
        return (2, pair_cards + kicker_cards)

    sorted_hand = sorted(hand, key=lambda x: (ranks.index(x[0]), suits.index(x[1])), reverse=True)[:5]
    return (1, sorted_hand)


def preflop_hand_rank(hand):
    """
    Evaluate the rank of a preflop poker hand.

    Args:
        hand (list of tuple): A list of card tuples representing the preflop hand.

    Returns:
        tuple: A tuple containing the hand rank (integer) and the best hand cards (list of tuples).
    """
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']

    rank_count = {rank: 0 for rank in ranks}
    suit_count = {suit: 0 for suit in suits}
    for card in hand:
        rank, suit = card
        rank_count[rank] += 1
        suit_count[suit] += 1

    for rank, count in rank_count.items():
        if count == 2:
            pair_cards = [card for card in hand if card[0] == rank]
            return (1, pair_cards)

    sorted_hand = sorted(hand, key=lambda x: (ranks.index(x[0]), suits.index(x[1])), reverse=True)
    return (0, sorted_hand)


def preflop(players, dealer, deck, pot, blind):
    """
    Execute the preflop betting round.

    Args:
        players (list of Player): List of players in the current hand.
        dealer (int): Index of the dealer position among players.
        deck (Deck): The deck of cards for the hand.
        pot (Pot): The main pot.
        blind (int): The blind amount for the current hand.

    Returns:
        list of Player: The remaining active players after the preflop round.
    """
    players = [player for player in players if player.chips >= blind // 2]

    little = players[(dealer + 1) % len(players)]
    big = players[(dealer + 2) % len(players)]

    pot.chips += blinds(big, little, blind)
    players = players[(dealer + 1):] + players[:(dealer + 1)]

    for i in range(2):
        for p in players:
            p.cards.append(deck.draw())

    min_bet = blind
    raise_count = 0
    last_raiser = None

    while True:
        all_called_or_folded = True
        for player in players:
            if player.fold or player == last_raiser or player.chips == 0:
                continue
            player_action = player.choose_action(pot.cards, min_bet)
            if player_action == "fold":
                player.fold = True
                if all(p.fold for p in players if p != player):
                    print("all fold")
                    return 1
            elif player_action == "call":
                call_amount = min(player.chips, min_bet - player.round_bet)
                pot.chips += call_amount
                player.chips -= call_amount
                player.round_bet += call_amount
                if player.chips == 0:
                    handle_side_pots(players, [player for player in players if not player.fold], pot)
            elif player_action == "raise" and raise_count < 3:
                raise_amount = min(player.chips, min_bet * 2 - player.round_bet)
                pot.chips += raise_amount
                player.chips -= raise_amount
                player.round_bet += raise_amount
                min_bet = player.round_bet
                raise_count += 1
                all_called_or_folded = False
                last_raiser = player
                if player.chips == 0:
                    handle_side_pots(players, [player for player in players if not player.fold], pot)
            elif player_action == "all-in":
                all_in_amount = player.chips
                pot.chips += all_in_amount
                player.round_bet += all_in_amount
                player.chips = 0
                if player.round_bet > min_bet:
                    min_bet = player.round_bet
                    raise_count += 1
                    all_called_or_folded = False
                    last_raiser = player
                handle_side_pots(players, [player for player in players if not player.fold], pot)
            else:
                print("Invalid Action")
                return

        if all_called_or_folded:
            break

    return players


def betting_round(players, pot, deck, min_bet, round_name):
    """
    Execute a betting round (flop, turn, or river).

    Args:
        players (list of Player): List of players in the current hand.
        pot (Pot): The main pot.
        deck (Deck): The deck of cards for the hand.
        min_bet (int): The minimum bet amount.
        round_name (str): The name of the betting round (e.g., "flop", "turn", "river").

    Returns:
        None
    """
    if round_name == "flop":
        for _ in range(3):  # Deal 3 cards for the flop
            pot.cards.append(deck.draw())
        # print(f"Flop cards: {pot.cards}")
    elif round_name in ["turn", "river"]:  # Deal 1 card for the turn and the river
        pot.cards.append(deck.draw())
        # print(f"{round_name.capitalize()} card: {pot.cards[-1]}")

    # Initialize betting variables
    raise_count = 0
    last_raiser = None

    # Betting loop
    while True:
        old_pot = pot.chips
        active_players = [player for player in players if not player.fold and player.chips > 0]

        print(len(active_players))

        for player in active_players:
            if player == last_raiser:
                # Reset round bets and return if the cycle of betting is complete
                for player in active_players:
                    player.round_bet = 0
                return

            player_action = player.choose_action(pot.cards, min_bet)
            if player_action == "fold":
                player.fold = True
                print(f"Player {player.name} folded!")
                if all(p.fold for p in players if p != player):
                    print("all fold")
                    return 1  # End the round if everyone else has folded
            elif player_action == "call":
                call_amount = min(player.chips, min_bet - player.round_bet)
                pot.chips += call_amount
                player.chips -= call_amount
                player.round_bet += call_amount
                if player.chips == 0:
                    handle_side_pots(players, active_players, pot)
            elif player_action == "raise" and raise_count < 3:
                proposed_raise_amount = min_bet * 2 - player.round_bet
                if player.chips < proposed_raise_amount:
                    all_in_amount = player.chips
                    pot.chips += all_in_amount
                    player.round_bet += all_in_amount
                    player.chips = 0
                    if player.round_bet > min_bet:
                        min_bet = player.round_bet
                        raise_count += 1
                    last_raiser = player
                    print(f"{player.name} goes all-in with {all_in_amount} chips.")
                    handle_side_pots(players, active_players, pot)
                else:
                    raise_amount = proposed_raise_amount
                    pot.chips += raise_amount
                    player.chips -= raise_amount
                    player.round_bet += raise_amount
                    min_bet = player.round_bet
                    raise_count += 1
                    last_raiser = player
                    print(f"{player.name} raises to {raise_amount} chips.")
            elif player_action == "raise" and raise_count == 3:
                call_amount = min(player.chips, min_bet - player.round_bet)
                pot.chips += call_amount
                player.chips -= call_amount
                player.round_bet += call_amount
            elif player_action == "all-in":
                all_in_amount = player.chips
                pot.chips += all_in_amount
                player.round_bet += all_in_amount
                player.chips = 0
                if player.round_bet > min_bet:
                    min_bet = player.round_bet
                    raise_count += 1
                last_raiser = player
                print(f"{player.name} goes all-in with {all_in_amount} chips.")
                handle_side_pots(players, active_players, pot)
            else:
                print("Invalid Action!")
                return

        # End the betting round if everyone has acted and there is no new raise
        if old_pot == pot.chips:
            break

    # Reset the round bets for the next betting round
    for player in players:
        player.round_bet = 0


def handle_side_pots(all_players, active_players, main_pot):
    """
    Handle side pots in the current hand.

    Args:
        all_players (list of Player): List of all players in the current hand.
        active_players (list of Player): List of active players in the current hand.
        main_pot (Pot): The main pot.

    Returns:
        int: The chips in the last side pot (if any) or the chips in the main pot.
    """
    # Sort active players based on their round bets in descending order
    active_players.sort(key=lambda x: x.round_bet, reverse=True)

    # Initialize an empty list to store side pots
    side_pots = []

    # Initialize the current pot with the main pot
    current_pot = main_pot

    # Iterate through the active players
    for i in range(len(active_players)):
        player = active_players[i]

        # Check if the player's round bet is less than the chips in the current pot
        if player.round_bet < current_pot.chips:
            # Create a new side pot and set its chips based on the player's round bet and the number of remaining players
            side_pot = Pot(cards = main_pot.cards)
            side_pot.chips = player.round_bet * (len(active_players) - i)

            # Update the chips in the current pot by subtracting the chips in the side pot
            current_pot.chips -= side_pot.chips

            # Add the side pot to the list of side pots
            side_pots.append(side_pot)
        else:
            # If the player's round bet is greater than or equal to the chips in the current pot, break out of the loop
            break

    # # Move the cards from the current pot to the main pot and reset the current pot
    # main_pot.cards.extend(current_pot.cards)
    # main_pot.reset()

    # # Distribute the cards from the current pot to each side pot
    # for side_pot in side_pots:
    #     side_pot.cards.extend(current_pot.cards.copy())

    # Print information about the side pots
    print("\nSide Pots:")
    for i, side_pot in enumerate(side_pots):
        print(f"Side Pot {i + 1}: {side_pot.chips} chips - Cards: {side_pot.cards}")

    # Reset the round bets for all players
    for player in all_players:
        player.round_bet = 0

    # Return the chips in the last side pot (if any) or the chips in the main pot
    return side_pots[-1].chips if side_pots else main_pot.chips


def showdown(players, pot):
    """
    Determine the winner(s) of the current hand during the showdown.

    Args:
        players (list of Player): List of players in the current hand.
        pot (Pot): The main pot.

    Returns:
        None
    """
    best_hands = []

    print(players[0].cards)

    for player in players:
        if not player.fold:
            all_hands = list(combinations(player.cards + pot.cards, 5))
            best_hand = max(all_hands, key=hand_rank)
            best_hand = hand_rank(best_hand)

            best_hands.append((player, best_hand))
    # print(best_hands)
    best_hands = sorted(best_hands, key=lambda x: x[1][0], reverse=True)
    best_hands = [item for item in best_hands if item[1][0] >= best_hands[0][1][0]]

    print(best_hands)

    if len(best_hands) == 1:
        best_hands[0][0].chips += pot.chips
        print("\n" + best_hands[0][0].name + " won " + str(pot.chips) + " chips!")
    else:
        player_dict = {}
        for player in best_hands:
            player_dict[player[0]] = []
            temp = []
            for card in player[1][1]:
                if card[0] == "Ace":
                    val = 14
                elif card[0] == "King":
                    val = 13
                elif card[0] == "Queen":
                    val = 12
                elif card[0] == "Jack":
                    val = 11
                else:
                    val = int(card[0])
                temp.append(val)
            player_dict[player[0]] = temp

        print(player_dict)

        for key, value in player_dict.items():
            count_dict = {}  # Initialize an empty dictionary

            for item in value:
                if item in count_dict:
                    count_dict[item] += 1  # If the item is already in the dictionary, increment its count
                else:
                    count_dict[item] = 1  # If the item is not in the dictionary, initialize its count to 1
            player_dict[key] = OrderedDict(sorted(count_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))

            # print(player_dict[key])

        print(player_dict)

        maximum = list(list(player_dict.values())[0])
        equal = []
        for key, value in player_dict.items():
            value = list(value)
            if value > maximum:
                maximum = value
                equal = [key]
            elif value == maximum:
                equal.append(key)

        print("\n")

        for player in equal:
            player.chips += int(pot.chips / len(equal))
            print(player.name + " won " + str(int(pot.chips / len(equal))) + " chips!")

        print("\n")

    pot.reset()
