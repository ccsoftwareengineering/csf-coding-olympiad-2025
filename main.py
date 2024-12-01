import pygame
import sys

# Initialize PyGame
pygame.init()

# Define Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Window size
FPS = 60  # Frames per second

# Set up Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen/window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Power Island Game")

# Set up the font for text rendering
font = pygame.font.SysFont("Arial", 36)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main Menu Function
def main_menu():
    """Display the main menu and start the game."""
    running = True
    while running:
        screen.fill(WHITE)  # Fill screen with white

        # Render title text
        title_text = font.render("Power Island - Press Enter to Start", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))  # Position it in the center

        # Draw Start Game Button
        start_button = draw_button("Start Game", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 200, 50)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False  # Exit menu and start the game loop
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    running = False  # Exit menu and start the game loop

        # Update the screen
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(FPS)

# Function to draw buttons
def draw_button(text, x, y, width, height):
    """Draw a clickable button with text."""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLACK, button_rect)  # Draw button
    text_surface = font.render(text, True, WHITE)  # Create text
    screen.blit(text_surface, (x + 20, y + 10))  # Position the text inside button
    return button_rect  # Return the button rectangle to detect clicks

# Game Loop Function
def game_loop():
    """Main game loop for the actual gameplay."""
    running = True
    while running:
        screen.fill(WHITE)  # Fill the screen with white background

        # Event handling (for quitting or interacting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop

        # Game updates and rendering go here (like updating the island's stats, etc.)

        # Example of a simple message showing up during gameplay:
        game_text = font.render("Welcome to Power Island!", True, BLACK)
        screen.blit(game_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))  # Centered on the screen

        # Update the screen with new frame
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Start the game by calling the main menu
main_menu()
game_loop()
