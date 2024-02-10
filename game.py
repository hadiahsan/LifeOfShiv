import pygame
import sys

# Initialize Pygame
pygame.init()

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Life of Shiv Simulator')
player_image = pygame.image.load('images/player_front_still.png').convert_alpha()
player_size = player_image.get_size()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 200, 0)
DARK_BLUE = (0, 0, 200)
BABY_BLUE = (137, 207, 240)  # Baby blue background

# Load custom font
font_path = "fonts/Blomberg.otf"  # Ensure this points to the correct .otf font file
title_font = pygame.font.Font(font_path, 72)  # Adjusted size for 1080p resolution
button_font = pygame.font.Font(font_path, 40)  # Adjusted size for button text

# Function to draw buttons, centered and stacked
def draw_button(screen, text, position, size, color, hover_color, font):
    x = screen_width / 2 - size[0] / 2  # Center horizontally
    rect = pygame.Rect((x, position[1]), size)
    mouse_pos = pygame.mouse.get_pos()
    button_color = color if not rect.collidepoint(mouse_pos) else hover_color

    pygame.draw.rect(screen, button_color, rect)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=rect.center)
    screen.blit(text_render, text_rect)
    return rect

# Title screen function, with buttons centered and stacked
def title_screen():
    screen.fill(BABY_BLUE)
    title_text = 'Life of Shiv Simulator'
    title = title_font.render(title_text, True, WHITE)
    title_rect = title.get_rect(center=(screen_width / 2, 150))  # Adjusted for 1080p

    screen.blit(title, title_rect)

    button_vertical_spacing = 20  # Space between buttons
    button_height = 60  # Button height
    first_button_y = 300  # Y position of the first button

    # Calculate positions based on spacing and height
    new_game_button_y = first_button_y
    continue_button_y = new_game_button_y + button_height + button_vertical_spacing
    settings_button_y = continue_button_y + button_height + button_vertical_spacing
    help_button_y = settings_button_y + button_height + button_vertical_spacing

    new_game_button = draw_button(screen, 'New Game', (0, new_game_button_y), (300, button_height), GREEN, DARK_GREEN, button_font)
    continue_button = draw_button(screen, 'Continue', (0, continue_button_y), (300, button_height), BLUE, DARK_BLUE, button_font)
    settings_button = draw_button(screen, 'Settings', (0, settings_button_y), (300, button_height), GREEN, DARK_GREEN, button_font)
    help_button = draw_button(screen, 'Help', (0, help_button_y), (300, button_height), BLUE, DARK_BLUE, button_font)

    return new_game_button, continue_button, settings_button, help_button

# Placeholder for customization screen
def customization_screen():
    screen.fill(BABY_BLUE)
    customization_text = title_font.render('Customization Settings', True, WHITE)
    screen.blit(customization_text, (screen_width / 2 - customization_text.get_width() / 2, 100))
    # Further customization options can be added here


# Game state
state = 'title'
tree_positions = [(100, 200), (400, 300), (800, 500), (1200, 400), (1400, 200), (550, 700), (450, 900)]  # Example positions
tree_image = pygame.image.load('images/tree.png').convert_alpha()  # convert_alpha() for transparent background



def draw_trees(screen, tree_positions):
    for pos in tree_positions:
        screen.blit(tree_image, pos)

def start_game():
    clock = pygame.time.Clock()
    player_pos = [screen_width // 2, screen_height // 2]  # Starting position of the player
    player_size = 50  # Assuming a square player for simplicity
    player_speed = 3  # Speed at which the player moves

    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                sys.exit()

        dx, dy = 0, 0  # Movement deltas

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx -= 1  # Move left
        if keys[pygame.K_d]:
            dx += 1  # Move right
        if keys[pygame.K_w]:
            dy -= 1  # Move up
        if keys[pygame.K_s]:
            dy += 1  # Move down

        # Check if moving diagonally and normalize movement
        if dx != 0 and dy != 0:
            factor = (2 ** 0.5) / 2  # Equivalent to 1/sqrt(2)
            dx *= factor
            dy *= factor

        # Apply movement speed and check boundaries
        new_x = player_pos[0] + dx * player_speed
        new_y = player_pos[1] + dy * player_speed

        # Ensure the player's position is within the horizontal bounds of the screen
        if 0 <= new_x <= screen_width - player_size:
            player_pos[0] = new_x
        # Ensure the player's position is within the vertical bounds of the screen
        if 0 <= new_y <= screen_height - player_size:
            player_pos[1] = new_y

        # Render game objects
        screen.fill(DARK_GREEN)  # Clear the screen with background color
        draw_trees(screen, tree_positions)
        screen.blit(player_image, (player_pos[0], player_pos[1]))
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit the frame rate to 60 frames per second

    global state
    state = 'title'

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and state == 'title':
            # Check which button was clicked and change state accordingly
            new_game_button, continue_button, settings_button, help_button = title_screen()
            mouse_pos = pygame.mouse.get_pos()
            if new_game_button.collidepoint(mouse_pos):
                state = 'game'
            if settings_button.collidepoint(pygame.mouse.get_pos()):
                state = 'settings'  # Placeholder for settings state
            elif help_button.collidepoint(pygame.mouse.get_pos()):
                state = 'help'  # Placeholder for help state

    if state == 'title':
        title_screen()
    elif state == 'game':
        start_game()
    elif state == 'customization':
        customization_screen()
    # Implement screens for settings and help as needed
        
    pygame.display.flip()

pygame.quit()
sys.exit()
