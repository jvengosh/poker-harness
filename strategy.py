from harness import *
from player import Player

class Strategy:
    """
    Base class for poker playing strategies.

    To create your own strategy, inherit from this class and implement the decide_action method.
    """

    def decide_action(self, player, community_cards, min_bet):
        """
        Decide the action to take based on the current game state.

        Args:
            player (Player): The player using this strategy.
            community_cards (list of tuple): The community cards on the table.
            min_bet (int): The minimum bet amount.

        Returns:
            str: The action to take, one of ["fold", "call", "raise", "all-in"].
        """
        raise NotImplementedError("Please Implement this method")


class DefaultStrategy(Strategy):
    """
    Default poker playing strategy.

    This strategy decides the action based on the best hand strength, either pre-flop or post-flop.
    """

    def decide_action(self, player, community_cards, min_bet):
        cards = player.cards.copy()

        # Combine player's hole cards with community cards (if any)
        if len(community_cards) != 0:
            cards += community_cards
            all_hands = list(combinations(cards, 5))
            best_hand = max(all_hands, key=hand_rank)
            best_hand = hand_rank(best_hand)
        else:
            best_hand = preflop_hand_rank(cards)

        print(f"{player.name}'s best hand: {best_hand}")

        # Determine the action based on hand strength
        if isinstance(best_hand[0], int):
            if best_hand[0] > 5:
                return "raise"
            else:
                return "call"
        else:
            raise TypeError(f"The first item of best_hand should be an int, but got {type(best_hand[0])}.")
