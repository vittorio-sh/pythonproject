import pygame
import random
import sys

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

CARD_WIDTH = 121
CARD_HEIGHT = 188

SUITS = ['H', 'D', 'C', 'S']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
#using dictionary to assign a color to each card based on suit this helps with step iv)
COLORS = {'H': 'red', 'D': 'red', 'C': 'black', 'S': 'black'}

class Card:
    def __init__(self, rank, suit, face_up=False):
        self.rank = rank  # (iii) Card values are appropriately displayed
        self.suit = suit  # (ii) Card suits are appropriately displayed
        self.color = COLORS[suit]
        self.face_up = face_up
        self.face_up_image = pygame.image.load(f"assets/front_card/{rank}{suit}.png")  # (i) Front side of the card is displayed
        self.face_down_image = pygame.image.load("assets/back_card/back.png")  # (i) Back side of the card is displayed
        self.image = self.face_down_image if not face_up else self.face_up_image
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))

    def flip(self):
        self.face_up = not self.face_up
        self.image = self.face_up_image if self.face_up else self.face_down_image
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))

#following classes are used to ensure game logic with adding and transfering cards
class Pile:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)  # (iii) As cards are sorted into their piles, they must be subtracted from the full deck of cards.


class Tableau(Pile):
    def can_add(self, card):
        if not self.cards:  
            return card.rank == 'K'  # (v) Spare tableau spots can only be filled with kings
        else:
            top_card = self.cards[-1]
            return COLORS[card.suit] != COLORS[top_card.suit] and RANKS.index(card.rank) == RANKS.index(top_card.rank) - 1  # (iv) Tableau cards can only be stacked in alternating colors


class Foundation(Pile):
    def can_add(self, card):
        if not self.cards:
            return card.rank == 'A'  # (vi) Foundations can only be filled starting with an ace
        else:
            top_card = self.cards[-1]
            return card.suit == top_card.suit and RANKS.index(card.rank) == RANKS.index(top_card.rank) + 1  # (i) Rank of cards is functional


class Waste(Pile):
    #need to add logic to pop from deck and add card to waste pile upon clicking
    pass


class Deck:
    def __init__(self):
        #declaring deck of cards and setting the image plus scalling
        self.cards = []
        self.deck_image = pygame.image.load("assets/back_card/back.png")  # (i) Back side of the card is displayed
        self.deck_image = pygame.transform.scale(self.deck_image, (CARD_WIDTH, CARD_HEIGHT))

    def fill(self):
        #filling deck with cards by using a for loop
        for suit in SUITS:
            for rank in RANKS:
                card = Card(rank, suit)
                self.cards.append(card)  # (ii) A full deck of cards is implemented.

    def shuffle(self):
        random.shuffle(self.cards)  # (ii) Deck can be shuffled

    def deal(self, tableau_piles):
        #ensure the right amount of cards are placed per tableau
        for i in range(7):
            for j in range(i + 1):
                card = self.cards.pop()  # (iii) cards are sorted into their piles, than subtracted from full deck
                tableau_pile = tableau_piles[i]
                tableau_pile.add_card(card)
                if j == i:  
                    card.flip()


class GameInterface:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Solitaire")
        self.screen.fill((0, 128, 0))

    def draw_start_button(self):
        #drawring start button i need to add functionality to potentially switch it to a restart button after clicked
        button_width = 100
        button_height = 50
        button_color = (200, 200, 200)
        button_text = "Start"

        button_rect = pygame.Rect(10, 10, button_width, button_height)
        pygame.draw.rect(self.screen, button_color, button_rect)

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(button_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_tableau_piles(self):
        pile_x = 100
        pile_y = 300
        pile_spacing = 20

        for tableau_pile in self.game.tableau_piles:
            #the deal function will ensure the right amount is placed on each tableau this for loop is just used to draw and space
            for i, card in enumerate(tableau_pile.cards):
                card_x = pile_x
                card_y = pile_y + i * pile_spacing
                self.screen.blit(card.image, (card_x, card_y))

            pile_x += CARD_WIDTH + pile_spacing

    def draw_deck_and_waste_piles(self):
        #the deck is drawn on the top left of the screen but need to add space for cards when clicked
        deck_x = 100
        deck_y = 50
        self.screen.blit(self.game.deck.deck_image, (deck_x, deck_y))

        if self.game.waste_pile.cards:
            self.screen.blit(self.game.waste_pile.cards[-1].image, (deck_x + CARD_WIDTH + 20, deck_y))

    def draw_foundation_piles(self):
        foundation_x = WINDOW_WIDTH - 100 - 4 * CARD_WIDTH
        foundation_y = 20

        for foundation_pile in self.game.foundation_piles:
            #this will draw the foundation piles based on whether theres a card there or empty 
            if foundation_pile.cards:
                #drawing card
                self.screen.blit(foundation_pile.cards[-1].image, (foundation_x, foundation_y))
            else:
                #drawing rectangle
                pygame.draw.rect(self.screen, (255, 255, 255), (foundation_x, foundation_y, CARD_WIDTH, CARD_HEIGHT), 1)

            foundation_x += CARD_WIDTH + 20

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(10, 10, 100, 50)

                if button_rect.collidepoint(mouse_pos):
                    self.game.start_button_clicked = True

    def render(self):
        self.screen.fill((0, 128, 0))
        self.draw_tableau_piles()
        self.draw_foundation_piles()

        if self.game.start_button_clicked:
            self.draw_deck_and_waste_piles()

        self.draw_start_button()
        pygame.display.update()


class Game:
    def __init__(self):
        self.tableau_piles = [Tableau() for _ in range(7)]
        self.foundation_piles = [Foundation() for _ in range(4)]
        self.waste_pile = Waste()
        self.deck = Deck()
        self.setup()
        self.start_button_clicked = False
        self.cards_dealt = False

    def setup(self):
        self.deck.fill()  # (ii) A full deck of cards is implemented.
        self.deck.shuffle()  # (ii) Deck can be shuffled

    def run(self):
        pygame.init()
        interface = GameInterface(self)
        while True:
            interface.events()
            if self.start_button_clicked and not self.cards_dealt:
                self.deck.deal(self.tableau_piles) 
                self.cards_dealt = True
            interface.render()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()