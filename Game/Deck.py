import random

import pygame
import LerpFuncs
from Card import Card


class Deck:

    def __init__(self, cards: list[Card], start_pos: list[int] = None):
        self.deck: list[Card] = cards
        if start_pos is None: start_pos = [0,0]
        self.start_pos = start_pos

    @staticmethod
    def get_new_deck() -> list[Card]:
        cards: list[Card] = []
        for s in range(4):
            for v in range(1, 13):
                c = Card(v, s)
                cards.append(c)
        return cards.copy()

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop(0)

    def add_card(self, card: Card):
        self.deck.append(card)

    def add_card_index(self, card: Card, index: int):
        self.deck.insert(index, card)

    def gyzmos(self, screen):
        s = pygame.Surface([Card.WIDTH, Card.HEIGHT])
        s.fill((0, 0, 0))
        pos = self.start_pos
        screen.blit(s, pos)


    def draw_deck(self, start_pos, space, card_size=Card.WIDTH):
        poses = []
        j = 0
        for i in range(len(self.deck)):
            if self.deck[i].active:
                poses.append([0,0])
                continue
            poses.append([start_pos[0] + j * (card_size + space), start_pos[1]])
            j += 1
        return poses


    def get_len_not_active(self):
        l = len(self)
        n = 0
        for i in range(l):
            if self.deck[i].active: n+=1
        return l-n


    def clear(self):
        self.deck = []

    def remove(self, index: int):
        self.deck.remove(self.deck[index])

    def add_cards(self, cards: list[Card]):
        self.deck.extend(cards)

    def __len__(self):
        return len(self.deck)

    def __repr__(self):
        return f"{[str(i) for i in self.deck]}"
