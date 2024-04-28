import random
import pygame

# Loading Dictionary
def load_dict(file_name):
    with open(file_name) as file:
        words = file.readlines()
    return [word[:5].upper() for word in words]

DICT_GUESSING = load_dict("dictionary_english.txt")
DICT_ANSWERS = load_dict("dictionary_wordle.txt")
ANSWER = random.choice(DICT_ANSWERS)

# Screen parameters
WIDTH = 600
HEIGHT = 700
MARGIN = 10
T_MARGIN = 100
B_MARGIN = 100
LR_MARGIN = 100

# Colors
LIGHT_MODE_BG = (255, 255, 255)
LIGHT_MODE_FG = (70, 70, 80)
DARK_MODE_BG = (30, 30, 30)
DARK_MODE_FG = (200, 200, 200)
GREEN = (6, 214, 160)
YELLOW = (255, 209, 102)

# Placeholders
INPUT = ""
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UNGUESSED = ALPHABET
GAME_OVER = False
DARK_MODE = False

def restart_game():
    global INPUT, GUESSES, UNGUESSED, ANSWER, GAME_OVER
    INPUT = ""
    GUESSES = []
    UNGUESSED = ALPHABET
    ANSWER = random.choice(DICT_ANSWERS)
    GAME_OVER = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle by Arjun")

SQ_SIZE = (WIDTH - 4 * MARGIN - 2 * LR_MARGIN) // 5
FONT = pygame.font.SysFont("freesansbold.ttf", SQ_SIZE)
FONT_SMALL = pygame.font.SysFont("freesansbold.ttf", SQ_SIZE // 2)

# Color the guesses
def determine_color(guess, j):
    letter = guess[j]
    if letter == ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        n_target = ANSWER.count(letter)
        n_correct = 0
        n_occurrence = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_occurrence += 1
                if letter == ANSWER[i]:
                    n_correct += 1

        if n_target - n_correct - n_occurrence >= 0:
            return YELLOW
    return DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Animation loop
animating = True
while animating:
    for event in pygame.event.get():

        # to quit with cross
        if event.type == pygame.QUIT:
            animating = False

        # user types something
        elif event.type == pygame.KEYDOWN:

            # to quit with esc key
            if event.key == pygame.K_ESCAPE:
                animating = False

            # backspace to correct user guess
            elif event.key == pygame.K_BACKSPACE:
                if len(INPUT) > 0:
                    INPUT = INPUT[:len(INPUT) - 1]

            # user types a guess
            elif event.key == pygame.K_RETURN:
                if len(INPUT) == 5 and INPUT in DICT_GUESSING:
                    GUESSES.append(INPUT)
                    UNGUESSED = "".join([letter for letter in ALPHABET if letter not in "".join(GUESSES)])
                    GAME_OVER = True if INPUT == ANSWER or len(GUESSES) >= 6 else False
                    INPUT = ""
                else:
                    # Invalid guess
                    INPUT = ""

            elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                if len(INPUT) < 5:
                    INPUT += chr(event.key).upper()

            # Toggle dark mode when Shift key is pressed
            elif event.key == pygame.K_SPACE:
                DARK_MODE = not DARK_MODE

            # Restart game when Ctrl key is pressed
            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                restart_game()

    # Drawing board
    screen.fill(DARK_MODE_BG if DARK_MODE else LIGHT_MODE_BG)
    letters = FONT_SMALL.render(UNGUESSED, False, DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG)
    surface = letters.get_rect(center=(WIDTH // 2, T_MARGIN // 2))
    screen.blit(letters, surface)

    y = T_MARGIN
    for i in range(6):
        x = LR_MARGIN
        for j in range(5):
            square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG, square, width=2, border_radius=15)

            if i < len(GUESSES) and j < len(GUESSES[i]):
                color = determine_color(GUESSES[i], j)
                pygame.draw.rect(screen, color, square, border_radius=15)
                letter = FONT.render(GUESSES[i][j], False, (255, 255, 255))
                surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                screen.blit(letter, surface)

            # user text input (next guess)
            if i == len(GUESSES) and j < len(INPUT):
                letter = FONT.render(INPUT[j], False, DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG)
                surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                screen.blit(letter, surface)

            x += SQ_SIZE + MARGIN
        y += SQ_SIZE + MARGIN

    # Check if user lost
    if len(GUESSES) >= 6 and not any(guess == ANSWER for guess in GUESSES):
        screen.fill(DARK_MODE_BG if DARK_MODE else LIGHT_MODE_BG)
        lost_text = FONT_SMALL.render("You lost :(  Press Ctrl to restart.", True, DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG)
        screen.blit(lost_text, (LR_MARGIN, HEIGHT // 2))
        answer_text = FONT.render(ANSWER, True, DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG)
        screen.blit(answer_text, (LR_MARGIN, HEIGHT // 2 + 30))

    # Check if user guessed the correct answer
    elif INPUT == ANSWER:
        screen.fill(DARK_MODE_BG if DARK_MODE else LIGHT_MODE_BG)
        win_text = FONT_SMALL.render("You got it :)  Press Ctrl to restart.", True, DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG)
        screen.blit(win_text, (LR_MARGIN, HEIGHT // 2))
        answer_text = FONT.render(ANSWER, True, DARK_MODE_FG if DARK_MODE else LIGHT_MODE_FG)
        screen.blit(answer_text, (LR_MARGIN, HEIGHT // 2 + 30))

    # Update screen
    pygame.display.flip()

pygame.quit()
