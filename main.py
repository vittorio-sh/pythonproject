import pygame
import random

#Variables used to make colours 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

pygame.init()

# check if game started
game_started = False

# Set the width and height of the screen
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Solitaire")

# Define card dimensions note the images I downloaded are too big so the screen is also set pretty large. We can download differents PNG later
card_width = 121
card_height = 188

# Load the card images
class CardImage(pygame.Surface):
    def __init__(self, size, *args, **kwargs):
        super().__init__(size, *args, **kwargs)
        self.rect = self.get_rect()

card_images = {}
suits = ['H', 'D', 'C', 'S']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

#for loop to assign rank and suit to each PNG image. Don't change the PNG names are this wont work
for suit in suits:
    for rank in ranks:
        card_name = f"{rank}{suit}"
        image_path = f"assets/front_card/{card_name}.png"
        card_image = pygame.image.load(image_path)
        card_image = pygame.transform.scale(card_image, (card_width, card_height))
        card_images[card_name] = CardImage((card_width, card_height))
        card_images[card_name].blit(card_image, (0, 0))

# Load the card back image
card_back_image = pygame.image.load("assets/back_card/back.png")
card_back_image = pygame.transform.scale(card_back_image, (card_width, card_height))

# Load the foundation image
foundation_image = pygame.image.load("assets/extra/foundation.png")
foundation_image = pygame.transform.scale(foundation_image, (card_width, card_height))

# Load the waste image
waste_image = pygame.image.load("assets/extra/waste.png")
waste_image = pygame.transform.scale(waste_image, (card_width, card_height))

# Define pile dimensions
pile_width = card_width + 20
pile_height = card_height + 20

# Calculate the positions for foundation piles and deck
foundation_start_x = 20
foundation_start_y = 20
foundation_spacing = pile_width
deck_x = screen_width - pile_width - 20
deck_y = 20

# Create rectangle plots for piles
tableau_rects = [[] for _ in range(7)]
foundation_rects = [pygame.Rect(foundation_start_x + i * foundation_spacing, foundation_start_y, card_width, card_height) for i in range(4)]
waste_rect = pygame.Rect(foundation_start_x + 4 * foundation_spacing + 20, foundation_start_y, card_width, card_height)
deck_rect = pygame.Rect(deck_x, deck_y, card_width, card_height)

# animation speed
deal_speed = 5  # Speed of dealer
deal_delay = 10  # Delay between dealing each card

# Function to shuffle and deal cards
def shuffle_and_deal():
    # Shuffle the deck
    deck = list(card_images.keys())
    random.shuffle(deck)

    # For loop to deal cards to each tableaux
    for i in range(7):
        for j in range(i + 1):
            if not deck:
                break  # Break if there are no more cards in the deck
            card = deck.pop()
            card_rect = card_images[card].get_rect(center=waste_rect.center)  # Start from waste pile
            card_images[card].rect = card_rect
            animate_card_deal(card_images[card], i, deal_delay * (i + j))
            tableau_rects[i].append(card)  # Add the card to the tableau pile



# Function to animate card dealing. I followed a youtube video and googled please don't mess with it because it's hard to fix..
def animate_card_deal(card_image, tableau, delay):
    if tableau_rects[tableau]:
        last_card = card_images[tableau_rects[tableau][-1]]
        target_pos = (last_card.rect.centerx, last_card.rect.centery + 20)
    else:
        target_pos = (pile_width * tableau + 20, pile_height + 40)

    dx = (target_pos[0] - card_image.rect.centerx) / deal_speed
    dy = (target_pos[1] - card_image.rect.centery) / deal_speed

    pygame.time.delay(delay)
    for _ in range(deal_speed):
        card_image.rect.move_ip(dx, dy)
        screen.fill(GREEN)
        draw_tableau_piles()
        draw_foundation_piles()
        pygame.draw.rect(screen, WHITE, waste_rect)
        screen.blit(card_image, card_image.rect)
        pygame.display.flip()
        pygame.time.delay(10)  # Adjust animation speed

# Function to draw tableau piles
def draw_tableau_piles():
    for i, pile in enumerate(tableau_rects):
        x = 20 + i * pile_width
        y = 20 + card_height  # Adjust the starting y position
        for j, card in enumerate(pile):
            if j >= len(pile) - 1 or not game_started:
                screen.blit(card_images[card], (x, y))
            else:
                screen.blit(card_back_image, (x, y))  # Display the back image of the card
            y += 20  # Increase the y position

# Function to draw foundation piles
def draw_foundation_piles():
    for i, rect in enumerate(foundation_rects):
        screen.blit(foundation_image, rect)  # Draw foundation image
        if i >= 1 or not game_started:
            pygame.draw.rect(screen, WHITE, rect, 1)  # Draw foundation rectangle border

# Function to handle button click
def handle_button_click(pos):
    global game_started
    if not game_started:
        game_started = True
        shuffle_and_deal()

# Game loop
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            handle_button_click(pos)

    screen.fill(GREEN)

    # Draw tableau piles
    draw_tableau_piles()

    # Draw foundation piles
    draw_foundation_piles()

    # Draw waste pile
    screen.blit(waste_image, waste_rect)

    # Draw deck
    pygame.draw.rect(screen, WHITE, deck_rect)

    # Draw start button
    button_rect = pygame.Rect(300, 540, 100, 50)
    pygame.draw.rect(screen, WHITE, button_rect)
    font = pygame.font.Font(None, 24)
    if not game_started:
        text = font.render("Start", True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()