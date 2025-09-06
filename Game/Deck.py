import random

import pygame
from Card import Card

class Deck:

    def __init__(self, cards: [Card]):
        self.deck: list[Card] = cards

    @staticmethod
    def get_new_deck() -> [Card]:
        cards: [Card] = []
        for s in range(4):
            for v in range(1, 13):
                cards.append(Card(v, s))
        return cards.copy()

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop(0)

    def add_card(self, card: Card):
        self.deck.append(card)

    def draw_deck(self, screen, start_pos, space, card_size = 200):
        for i, c in enumerate(self.deck):
            pos = [start_pos[0] + i * (card_size + space), start_pos[1]]
            c.set_pos(pos)

    def clear(self):
        self.deck = []

    def add_cards(self, cards: list[Card]):
        self.deck.extend(cards)

    def __len__(self):
        return len(self.deck)

    def __repr__(self):
        return f"{[str(i) for i in self.deck]}"

