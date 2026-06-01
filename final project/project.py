import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.set_num_channels(1)

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse and Cat Game")

# Colors
BLACK = (0, 0, 0)

# Load images
mouse_img = pygame.transform.scale(pygame.image.load("mouse.png"), (80, 80))
cat_img = pygame.transform.scale(pygame.image.load("cat.png"), (100, 100))
cheese_img = pygame.transform.scale(pygame.image.load("cheese.png"), (70, 70))

front_page_img = pygame.transform.scale(pygame.image.load("frontpage.png"), (WIDTH, HEIGHT))
gameover_img   = pygame.transform.scale(pygame.image.load("gameover.png"), (WIDTH, HEIGHT))

# Sounds
cheeseeaten_sfx = pygame.mixer.Sound("cheeseEaten_sfx.wav")
cat_sfx = pygame.mixer.Sound("cat_sfx.wav")
bg_sound = pygame.mixer.Sound("bg_sound.mp3")
bg_sound.set_volume(0.3)
bg_sound.play(-1)

# Font
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Track highest score
highest_score = 0

# --- FRONT PAGE ---
def show_front_page():
    start_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 200, 200, 60)

    while True:
        screen.blit(front_page_img, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "start"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "start"

# --- GAME OVER SCREEN ---
def show_gameover_screen(final_score):
    global highest_score
    restart_button_rect = pygame.Rect(250, 450, 150, 60)
    quit_button_rect    = pygame.Rect(450, 450, 150, 60)

    # Update highest score if beaten
    if final_score > highest_score:
        highest_score = final_score

    while True:
        screen.blit(gameover_img, (0, 0))

        # Show current score
        score_text = font.render(f"Score: {final_score}", True, BLACK)
        screen.blit(score_text, (WIDTH//2 - 50, HEIGHT//2 - 40))

        # Show highest score
        highscore_text = font.render(f"Highest: {highest_score}", True, BLACK)
        screen.blit(highscore_text, (WIDTH//2 - 50, HEIGHT//2 + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return "restart"
                elif quit_button_rect.collidepoint(event.pos):
                    return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    return "quit"

# --- MAIN GAME LOOP ---
def game_loop():
    mouse_x, mouse_y = WIDTH // 4, HEIGHT // 4
    cat_x, cat_y = WIDTH // 2, HEIGHT // 8
    mouse_speed = 5
    cat_speed = 1
    cheese_x = random.randint(50, WIDTH-100)
    cheese_y = random.randint(50, HEIGHT-100)
    score = 0

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # Mouse controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and mouse_x > 0:
            mouse_x -= mouse_speed
        if keys[pygame.K_RIGHT] and mouse_x < WIDTH - 60:
            mouse_x += mouse_speed
        if keys[pygame.K_UP] and mouse_y > 0:
            mouse_y -= mouse_speed
        if keys[pygame.K_DOWN] and mouse_y < HEIGHT - 60:
            mouse_y += mouse_speed

        # Cat chases mouse
        if cat_x < mouse_x: cat_x += cat_speed
        if cat_x > mouse_x: cat_x -= cat_speed
        if cat_y < mouse_y: cat_y += cat_speed
        if cat_y > mouse_y: cat_y -= cat_speed

        # Collision detection
        mouse_rect = pygame.Rect(mouse_x, mouse_y, 60, 60)
        cheese_rect = pygame.Rect(cheese_x, cheese_y, 50, 50)
        cat_rect = pygame.Rect(cat_x, cat_y, 80, 80)

        if mouse_rect.colliderect(cheese_rect):
            score += 1
            cheese_x = random.randint(50, WIDTH-100)
            cheese_y = random.randint(50, HEIGHT-100)
            cheeseeaten_sfx.play()
            cat_speed += 0.2  # Difficulty scaling

        if mouse_rect.colliderect(cat_rect):
            cat_sfx.play()
            action = show_gameover_screen(score)
            return action

        # Drawing
        screen.fill((255, 105, 180))
        screen.blit(mouse_img, (mouse_x, mouse_y))
        screen.blit(cat_img, (cat_x, cat_y))
        screen.blit(cheese_img, (cheese_x, cheese_y))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Show highest score during gameplay too
        highscore_text = font.render(f"Highest: {highest_score}", True, BLACK)
        screen.blit(highscore_text, (10, 40))

        pygame.display.update()

# --- START GAME FLOW ---
while True:
    action = show_front_page()
    if action == "quit":
        break
    elif action == "start":
        result = game_loop()
        if result == "quit":
            break
        elif result == "restart":
            continue

pygame.quit()
exit()
