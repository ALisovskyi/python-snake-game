import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Python Snake Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_green = (0, 100, 0)  # Dark green color for digits

# Game parameters
snake_block = 20
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Path for saving the high score
record_file = "record.txt"


# Function to display a message on the screen
def message(msg, color, position, angle=0):
    mes = font_style.render(msg, True, color)
    rotated_msg = pygame.transform.rotate(mes, angle)
    rect = rotated_msg.get_rect(center=(position[0] + snake_block // 2, position[1] + snake_block // 2))
    screen.blit(rotated_msg, rect.topleft)


# Function to display the score
def show_score(score, record):
    value = score_font.render("Score: " + str(score), True, white)
    record_value = score_font.render("Record: " + str(record), True, white)
    screen.blit(value, [0, 0])
    screen.blit(record_value, [screen_width - 200, 0])


# Function to check collision
def is_collision(snake_pos, food_pos):
    snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], snake_block, snake_block)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], snake_block, snake_block)
    return snake_rect.colliderect(food_rect)


# Function to load the high score from file
def load_record():
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            content = f.read().strip()  # Удаляем пробельные символы
            if content:  # Если файл не пустой
                return int(content)
            else:  # Если файл пустой
                return 0
    return 0



# Function to save the high score to file
def save_record(record):
    with open(record_file, "w") as f:
        f.write(str(record))


# Main menu
def main_menu():
    record = load_record()
    menu = True

    while menu:
        screen.fill(black)
        message("Python Snake Game", white, [screen_width // 2, screen_height // 4])
        message("Press ENTER to Start", white, [screen_width // 2, screen_height // 2])
        message(f"Record: {record}", white, [screen_width // 2, screen_height // 2 + 50])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                    game_loop(record)


# Main game function
def game_loop(record):
    # Initial snake parameters
    snake_pos = [100, 50]
    snake_body = [['P', snake_pos[0], snake_pos[1], 0]]  # Segment: letter, x, y, angle
    snake_direction = 'RIGHT'
    change_to = snake_direction
    score = 0

    # Food letters
    food_list = ['y', 't', 'h', 'o', 'n']
    food_index = 0
    food_pos = [random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                random.randint(0, (screen_height - snake_block) // snake_block) * snake_block]

    # Random fire
    fire_list = [['~', random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                  random.randint(0, (screen_height - snake_block) // snake_block) * snake_block]]

    game_over = False
    game_continued = False

    # Timers for digits
    food_timer = []

    # Initialize angle
    angle = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'

        snake_direction = change_to

        # Move the snake's head
        if snake_direction == 'LEFT':
            snake_pos[0] -= snake_block
            angle = 90
        elif snake_direction == 'RIGHT':
            snake_pos[0] += snake_block
            angle = -90
        elif snake_direction == 'UP':
            snake_pos[1] -= snake_block
            angle = 0
        elif snake_direction == 'DOWN':
            snake_pos[1] += snake_block
            angle = 180

        # Check boundaries and teleport
        if snake_pos[0] >= screen_width:
            snake_pos[0] = 0
        elif snake_pos[0] < 0:
            snake_pos[0] = screen_width - snake_block
        if snake_pos[1] >= screen_height:
            snake_pos[1] = 0
        elif snake_pos[1] < 0:
            snake_pos[1] = screen_height - snake_block

        # Update the snake's body position
        new_body = []
        for i in range(len(snake_body)):
            if i == 0:
                new_body.append([snake_body[i][0], snake_pos[0], snake_pos[1], angle])  # Head angle
            else:
                prev_segment = snake_body[i - 1]
                new_body.append([snake_body[i][0], prev_segment[1], prev_segment[2], prev_segment[3]])

        snake_body = new_body

        if game_continued:
            # Generate new "digit-food" if not on screen
            if not food_pos:
                food_pos = []
                food_timer = []
                for _ in range(random.randint(1, 3)):
                    food_pos.append([random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                                     random.randint(0, (screen_height - snake_block) // snake_block) * snake_block,
                                     random.choice("123456789")])
                    # Set timer for each digit
                    food_timer.append(time.time() + random.randint(3, 5))

            # Check collision with digits
            for i, food in enumerate(food_pos[:]):
                if is_collision(snake_pos, food[:2]):
                    score += int(food[2]) * 100  # Add points
                    food_pos.pop(i)  # Remove eaten food
                    food_timer.pop(i)  # Remove corresponding timer

            # Remove food after timer expires
            current_time = time.time()
            food_pos = [food for i, food in enumerate(food_pos) if current_time < food_timer[i]]
            food_timer = [timer for timer in food_timer if current_time < timer]

        # Check collision with "food"
        if not game_continued and is_collision(snake_pos, food_pos):
            # Add new segment with head angle
            snake_body.append([food_list[food_index], food_pos[0], food_pos[1], angle])
            score += 1000  # Award 1000 points for each letter
            food_index += 1

            if food_index < len(food_list):
                food_pos = [random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                            random.randint(0, (screen_height - snake_block) // snake_block) * snake_block]
                # Add new fire only in the first phase
                fire_list.append(['~', random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                                  random.randint(0, (screen_height - snake_block) // snake_block) * snake_block])
            else:
                game_continued = True  # Start the second phase of the game
                food_pos = []

        # Update fire
        for fire in fire_list:
            direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
            if direction == 'LEFT':
                fire[1] -= snake_block
            elif direction == 'RIGHT':
                fire[1] += snake_block
            elif direction == 'UP':
                fire[2] -= snake_block
            elif direction == 'DOWN':
                fire[2] += snake_block

            # Check boundaries and teleport
            if fire[1] >= screen_width:
                fire[1] = 0
            elif fire[1] < 0:
                fire[1] = screen_width - snake_block
            if fire[2] >= screen_height:
                fire[2] = 0
            elif fire[2] < 0:
                fire[2] = screen_height - snake_block

            # Check collision with fire
            if is_collision(snake_pos, fire[1:]):
                game_over = True

        screen.fill(black)

        # Draw the snake
        for segment in snake_body:
            letter, x, y, angle = segment
            message(letter, white, [x + snake_block // 2, y + snake_block // 2], angle=angle)

        # Draw current "food"
        if game_continued:
            for food in food_pos:
                message(food[2], dark_green, [food[0] + snake_block // 2, food[1] + snake_block // 2])
        else:
            message(food_list[food_index], white, [food_pos[0] + snake_block // 2, food_pos[1] + snake_block // 2])

        # Draw fire
        for fire in fire_list:
            message('~', red, [fire[1] + snake_block // 2, fire[2] + snake_block // 2])

        # Draw the score
        show_score(score, record)

        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

    # Update high score if current score is higher
    if score > record:
        save_record(score)

    # Game over
    screen.fill(black)
    message("Game Over", white, [screen_width // 2, screen_height // 3])
    message(f"Score: {score}", white, [screen_width // 2, screen_height // 2])
    message("Press ENTER to Play Again", white, [screen_width // 2, screen_height // 2 + 50])
    pygame.display.update()

    game_restart = False
    while not game_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_restart = True
                    game_loop(load_record())




# Start the menu
main_menu()
