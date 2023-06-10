#Code By : Hompushparaj Mehta
#Date : 10-07-2023

import pygame
import random

# Initialing Pygame library
pygame.init()

# This part wil set up the display
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The rabbit")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELL0W=(255,255,0)
RED = (255, 0, 0)
CYAN = (0,255,255)
MAGNETA = (255,0,255)

# Load player image
player_img = pygame.image.load("rabbit.png")
player_size = 50
player_img = pygame.transform.scale(player_img, (player_size, player_size))
player_x = 10
player_y = screen_height - player_size - 10
player_speed = 5

# Let's load the images of food
food_images = []
food_positions = []  # This list will store the food positions
food_size = 30  # Define the food size
max_food_count = 2  # It will display the maximum no of number of food items
food_count = random.randint(1, max_food_count)  # Generate random number of food items
for _ in range(food_count):
    food_image = pygame.image.load("carrot.png") 
    food_image = pygame.transform.scale(food_image, (food_size, food_size))
    food_images.append(food_image)
    food_x = random.randint(0, screen_width - food_size)
    food_y = random.randint(0, screen_height - food_size)
    food_positions.append((food_x, food_y))
food_speed = 1

# Load sound effect
eat_sound = pygame.mixer.Sound("sound_1.wav")

#Load background music
pygame.mixer.music.load("background-music.wav")

# Play background music in loop
pygame.mixer.music.play(-1, 0.0)


# Set up scoring and lives
score = 0
lives = 3
level = 1
consecutive_food = 0
font = pygame.font.Font(None, 48)
font_game_over = pygame.font.Font(None,64)
clock = pygame.time.Clock()

game_over = False

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    #It helps player to move up 
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    #It helps player to move down
    if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
        player_y += player_speed
    #It helps player to move left
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    #It helps player to move right
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed


    screen.fill(BLACK)

    # Update food positions
    for i, (food_x, food_y) in enumerate(food_positions):
        food_x -= food_speed
        if food_x < 0:
            food_x = screen_width - food_size
            food_y = random.randint(0, screen_height - food_size)
            if consecutive_food < 2:
                lives -= 1
                consecutive_food = 0
        food_positions[i] = (food_x, food_y)

        # Print food in the screen 
        screen.blit(food_images[i], (food_x, food_y))

        # Let's check  the collision with food
        if player_x < food_x + food_size and player_x + player_size > food_x and player_y < food_y + food_size and player_y + player_size > food_y:
            consecutive_food += 1
            if consecutive_food == 2:
                consecutive_food = 0
            else:
                score += 1
                consecutive_food = 0
                eat_sound.play()  # It will play the sound effect when player eat the food
            food_positions[i] = (screen_width - food_size, random.randint(0, screen_height - food_size))
        
        # This part will handel the speed of food , player and level upgrading
        if score == 20:
            level = 2
            food_speed = 2
            player_speed = 8
        if score == 40:
            level = 3
            food_speed = 3
            player_speed = 10
        if score == 60:
            level = 4
            food_speed = 4
            player_speed = 11
        if score == 80:
            level = 5
            food_speed = 6
            player_speed = 13
        if score == 100:
            level = 6
            food_speed = 8
            player_speed = 15

    # Let's print the player's image in the screen
    screen.blit(player_img, (player_x, player_y))

    # This part of code will draw score and lives
    score_text = font.render("Score: " + str(score), True, BLUE)
    lives_text = font.render("Lives: " + str(lives), True, GREEN)
    level_text = font.render("Level: " + str(level),True,GREEN)
    
    #This will handel the color combination of the lives
    if lives == 0:
        lives_text = font.render("Lives: " + str(lives), True, RED)
    if lives == 1:
        lives_text = font.render("Lives: " + str(lives), True, RED)
    if lives == 2:
        lives_text = font.render("Lives: " + str(lives), True, YELL0W)
    
    #This will handel the color combination of the level
    if level > 3:
        level_text = font.render("Level: " + str(level),True,YELL0W)
    if level > 6:
        level_text = font.render("Level: " + str(level),True,CYAN)
    if level > 8:
        level_text = font.render("Level: " + str(level),True,RED)

    screen.blit(score_text, (10, 20))
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 20))
    screen.blit(level_text,(400,20))


    # Check if lives are zero
    if lives == 0:
        game_over_text = font_game_over.render("Game Over", True, RED)
        screen.blit(game_over_text,
                    (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(5000)  # show the Game over screen for 2 second
        game_over = True

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
