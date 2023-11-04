import numpy as np
import math
import random
from itertools import combinations
from collections import OrderedDict

class Strategy:
    def decide_action(self, player, community_cards, min_bet):
        raise NotImplementedError("Please Implement this method")


class DefaultStrategy(Strategy):
    def decide_action(self, player, community_cards, min_bet):
        cards = player.cards.copy()
        if len(community_cards) != 0:
            cards += community_cards
            all_hands = list(combinations(cards, 5))
            best_hand = max(all_hands, key=hand_rank)
            best_hand = hand_rank(best_hand)
        else:
            best_hand = preflop_hand_rank(cards)
        print(f"{player.name}'s best hand: {best_hand}")
        if isinstance(best_hand[0], int):
            if best_hand[0] > 5:
                return "raise"
            else:
                return "call"
        else:
            raise TypeError(f"The first item of best_hand should be an int, but got {type(best_hand[0])}.")

class Player:
    def __init__(self, n, strategy=None):
        self.name = n
        self.chips = 2000
        self.action = ""
        self.fold = False
        self.round_bet = 0
        self.cards = []
        self.strategy = strategy if strategy else DefaultStrategy()

    def reset(self):
        self.action = ""
        self.fold = False
        self.round_bet = 0
        self.cards = []

    def choose_action(self, community_cards, min_bet):
        action = self.strategy.decide_action(self, community_cards, min_bet)
        self.action = action
        return action


class Pot:
    def __init__(self):
        self.chips = 0
        self.cards = []

    def reset(self):
        self.chips = 0
        self.cards = []


class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        self.cards = [(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)


def blinds(big, little, blind):
    big_blind = min(big.chips, blind)
    little_blind = min(little.chips, math.floor(blind / 2))
    big.chips -= big_blind
    big.round_bet = big_blind
    little.chips -= little_blind
    little.round_bet = little_blind
   #  print(f"Big blind posted by {big.name}: {big_blind} chips.")
   # print(f"Little blind posted by {little.name}: {little_blind} chips.")
    return big_blind + little_blind


def hand_rank(hand):
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']

    rank_count = {rank: 0 for rank in ranks}
    suit_count = {suit: 0 for suit in suits}
    for card in hand:
        rank, suit = card
        rank_count[rank] += 1
        suit_count[suit] += 1

    if all(suit_count[suit] == 5 for suit in suits) and all(rank_count[rank] == 1 for rank in ranks[-5:]):
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
            kicker_cards = sorted((card for card in hand if card[0] != rank), key=lambda x: ranks.index(x[0]), reverse=True)[:2]
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
        kicker_cards = sorted((card for card in hand if card[0] != pairs[0]), key=lambda x: ranks.index(x[0]), reverse=True)[:3]
        return (2, pair_cards + kicker_cards)

    sorted_hand = sorted(hand, key=lambda x: (ranks.index(x[0]), suits.index(x[1])), reverse=True)[:5]
    return (1, sorted_hand)


def preflop_hand_rank(hand):
    ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
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
    little = players[(dealer + 1) % len(players)]
    big = players[(dealer + 2) % len(players)]

    pot.chips += blinds(big, little, blind)
    players = players[(dealer + 1):] + players[:(dealer + 1)]
    #print(players[0].name)

    for i in range(2):
        for p in players:
            p.cards.append(deck.draw())

    min_bet = blind
    raise_count = 0
    last_raiser = None

    while True:
        all_called_or_folded = True
        for player in players:
            if player.fold or player == last_raiser:
                continue
            player_action = player.choose_action(pot.cards, min_bet)
            if player_action == "fold":
                player.fold = True
                if all(p.fold for p in players if p != player):
                    break
            elif player_action == "call":
                call_amount = min(player.chips, min_bet - player.round_bet)
                pot.chips += call_amount
                player.chips -= call_amount
                player.round_bet += call_amount
            elif player_action == "raise" and raise_count < 3:
                raise_amount = min_bet * 2
                pot.chips += raise_amount
                player.chips -= raise_amount
                player.round_bet += raise_amount
                min_bet = player.round_bet
                raise_count += 1
                all_called_or_folded = False
                last_raiser = player
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
            else:
                print("Invalid Action")
                return

        if all_called_or_folded:
            break

    return players


def betting_round(players, pot, deck, min_bet, round_name):
    # Deal community cards based on the round
    if round_name == "flop":
        for _ in range(3):  # Deal 3 cards for the flop
            pot.cards.append(deck.draw())
        #print(f"Flop cards: {pot.cards}")
    elif round_name in ["turn", "river"]:  # Deal 1 card for the turn and the river
        pot.cards.append(deck.draw())
        #print(f"{round_name.capitalize()} card: {pot.cards[-1]}")

    # Initialize betting variables
    raise_count = 0
    last_raiser = None

    # Betting loop
    while True:
        old_pot = pot.chips
        for player in players:
            if player == last_raiser:
                for player in players:
                    player.round_bet = 0
                return

            if player.fold:
                continue

            player_action = player.choose_action(pot.cards, min_bet)
            if player_action == "fold":
                player.fold = True
                print("Player " + player.name + " folded!")
                if all(p.fold for p in players if p != player):
                    return  # End the round if everyone else has folded
            elif player_action == "call":
                call_amount = min(player.chips, min_bet - player.round_bet)
                pot.chips += call_amount
                player.chips -= call_amount
                player.round_bet += call_amount
                #print(f"{player.name} calls {call_amount} chips.")
            elif player_action == "raise" and raise_count < 3:
                raise_amount = min(player.chips, min_bet * 2 - player.round_bet)
                print("Player " + player.name + " raised " + str(raise_amount) + "!")
                pot.chips += raise_amount
                player.chips -= raise_amount
                player.round_bet += raise_amount
                min_bet = player.round_bet
                raise_count += 1
                last_raiser = player
                #print(f"{player.name} raises to {raise_amount} chips.")
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
                #print(f"{player.name} goes all-in with {all_in_amount} chips.")
            else:
                print("Invalid Action!")
                return

        # End the betting round if everyone has acted and there is no new raise
        if old_pot == pot.chips:
            break

    # Reset the round bets for the next betting round
    for player in players:
        player.round_bet = 0


def showdown(players, pot):
    best_hands = []

    for player in players:
        if not player.fold:
            all_hands = list(combinations(player.cards + pot.cards, 5))
            best_hand = max(all_hands, key=hand_rank)
            best_hand = hand_rank(best_hand)

            best_hands.append((player, best_hand))
    # print(best_hands)
    best_hands = sorted(best_hands, key=lambda x: x[1][0], reverse=True)
    best_hands = [item for item in best_hands if item[1][0] >= best_hands[0][1][0]]

    # print(best_hands)

    if len(best_hands) == 1:
        best_hands[0][0].chips += pot.chips
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
        
        # print(player_dict)

        for key, value in player_dict.items():
            count_dict = {}  # Initialize an empty dictionary

            for item in value:
                if item in count_dict:
                    count_dict[item] += 1  # If the item is already in the dictionary, increment its count
                else:
                    count_dict[item] = 1  # If the item is not in the dictionary, initialize its count to 1
            player_dict[key] = OrderedDict(sorted(count_dict.items()))

        # print(player_dict)

        maximum = list(list(player_dict.values())[0])
        equal = []
        for key, value in player_dict.items():
            value = list(value)
            if value > maximum:
                maximum = value
                equal = [key]
            elif value == maximum:
                equal.append(key)

        for player in equal:
            player.chips += int(pot.chips / len(equal))

    pot.reset()


def main():
    player_0 = Player("Alpha")
    player_1 = Player("Bravo")
    player_2 = Player("Charlie")
    player_3 = Player("Delta")
    players = [player_0, player_1, player_2, player_3]

    pot = Pot()
    deck = Deck()
    deck.shuffle()

    blind = 20
    dealer = math.floor(random.random() * 4)
    print("\nPreflop")
    preflop(players, dealer, deck, pot, blind)
    print("\nFlop")
    betting_round(players, pot, deck, blind, "flop")
    print("\nTurn")
    betting_round(players, pot, deck, blind, "turn")
    print("\nRiver")
    betting_round(players, pot, deck, blind, "river")
    showdown(players, pot)

    print(f"\n\nGame over. Final chip counts:")
    for p in players:
        print(f"{p.name}: {p.chips} chips")
    print(f"Total chips in pot: {pot.chips}")

main()