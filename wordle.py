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
WHITE = (255, 255, 255)
GREY = (70, 70, 80)
GREEN = (6, 214, 160)
YELLOW = (255, 209, 102)
RED = (255, 0, 0)

# Placeholders
INPUT = ""
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UNGUESSED = ALPHABET
GAME_OVER = False

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
    return GREY

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

    # Drawing board
    screen.fill(WHITE)
    letters = FONT_SMALL.render(UNGUESSED, False, GREY)
    surface = letters.get_rect(center=(WIDTH // 2, T_MARGIN // 2))
    screen.blit(letters, surface)

    y = T_MARGIN
    for i in range(6):
        x = LR_MARGIN
        for j in range(5):
            square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, GREY, square, width=2, border_radius=15)

            if i < len(GUESSES) and j < len(GUESSES[i]):
                color = determine_color(GUESSES[i], j)
                pygame.draw.rect(screen, color, square, border_radius=15)
                letter = FONT.render(GUESSES[i][j], False, (255, 255, 255))
                surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                screen.blit(letter, surface)

            # user text input (next guess)
            if i == len(GUESSES) and j < len(INPUT):
                letter = FONT.render(INPUT[j], False, GREY)
                surface = letter.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
                screen.blit(letter, surface)

            x += SQ_SIZE + MARGIN
        y += SQ_SIZE + MARGIN

    # If game over, display answer
    if GAME_OVER:
        answer_text = FONT.render(ANSWER, True, GREY)
        screen.blit(answer_text, (WIDTH//2.8, (HEIGHT - B_MARGIN)+20))
        pygame.display.flip()
        pygame.time.wait(2000)
        restart_game()

    # Update screen
    pygame.display.flip()

pygame.quit()