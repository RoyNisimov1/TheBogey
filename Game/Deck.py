import random

import pygame
import LerpFuncs
from Card import Card
from Game.GLOBAL import GLOBAL


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
        s = self.get_top_card_surface()
        pos = self.start_pos
        screen.blit(s, pos)


    def draw_deck(self, start_pos, space, card_size=Card.WIDTH, skip=False):
        poses = []
        if skip:
            j = 0
            for i in range(len(self.deck)):
                if self.deck[i].active:
                    poses.append([0, 0])
                    continue
                poses.append([start_pos[0] + j * (card_size + space), start_pos[1]])
                j += 1
        else:
            poses = [[start_pos[0] + i * (card_size + space), start_pos[1]] for i in range(len(self))]
        return poses

    def get_rect(self):
        return pygame.Rect([self.start_pos[0], self.start_pos[1], Card.WIDTH, Card.HEIGHT])

    def on_mouse_hover(self):
        ...

    def can_add_card(self, card: Card):
        if len(self.deck) == 0: return True
        top_card = self.deck[len(self.deck)-1]
        if top_card.suit != card.suit: return False
        if top_card.value < card.value: return False
        return True


    def on_mouse_click(self):
        ...

    def remove_card_data(self, card: Card):
        i = 0
        found_card = False
        for c in range(len(self.deck)):
            if self.deck[c] == card:
                i = c
                found_card = True
        if found_card:
            self.remove(i)

    def on_mouse_release(self):

        if not GLOBAL().get_is_active() or GLOBAL().get_current() is None: return False
        card: Card = GLOBAL().get_current()
        if not self.can_add_card(card):
            return False
        self.add_card(card)
        return True

    def check_mouse_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_buttons_release = pygame.mouse.get_just_released()

        succeeded = False
        if self.get_rect().collidepoint(mouse_pos):
            self.on_mouse_hover()
            if mouse_buttons[0]:
                self.on_mouse_click()
            if mouse_buttons_release[0]:
                succeeded = self.on_mouse_release()
        return succeeded


    def get_top_card_surface(self):
        if len(self.deck) == 0:
            s = pygame.Surface([Card.WIDTH, Card.HEIGHT])
            s.fill((0, 0, 0))
            return s
        s = self.deck[len(self.deck)-1]
        if s.suit == 0:
            s = pygame.transform.scale_by(s.surface, 0.5)
        else:
            s = s.surface
        return s



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
