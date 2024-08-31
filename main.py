import pygame
import random
import time
import os

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Python Snake Game')

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_green = (0, 100, 0)  # Темно-зеленый цвет для цифр

# Параметры игры
snake_block = 20
snake_speed = 15

# Шрифт
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Путь для сохранения рекорда
record_file = "record.txt"

# Функция для отображения сообщения на экране
def message(msg, color, position, angle=0):
    mesg = font_style.render(msg, True, color)
    rotated_mesg = pygame.transform.rotate(mesg, angle)
    rect = rotated_mesg.get_rect(center=(position[0] + snake_block // 2, position[1] + snake_block // 2))
    screen.blit(rotated_mesg, rect.topleft)

# Функция для отображения очков
def show_score(score, record):
    value = score_font.render("Score: " + str(score), True, white)
    record_value = score_font.render("Record: " + str(record), True, white)
    screen.blit(value, [0, 0])
    screen.blit(record_value, [screen_width - 200, 0])

# Функция для проверки столкновения
def is_collision(snake_pos, food_pos):
    snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], snake_block, snake_block)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], snake_block, snake_block)
    return snake_rect.colliderect(food_rect)

# Функция для чтения рекорда из файла
def load_record():
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            return int(f.read())
    return 0

# Функция для сохранения рекорда в файл
def save_record(record):
    with open(record_file, "w") as f:
        f.write(str(record))

# Главное меню
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

# Основная функция игры
def game_loop(record):
    # Начальные параметры змейки
    snake_pos = [100, 50]
    snake_body = [['P', snake_pos[0], snake_pos[1], 0]]  # Сегмент: буква, x, y, угол
    snake_direction = 'RIGHT'
    change_to = snake_direction
    score = 0

    # Буквы-еда
    food_list = ['y', 't', 'h', 'o', 'n']
    food_index = 0
    food_pos = [random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                random.randint(0, (screen_height - snake_block) // snake_block) * snake_block]

    # Хаотичный огонь
    fire_list = [['~', random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                  random.randint(0, (screen_height - snake_block) // snake_block) * snake_block]]

    game_over = False
    game_continued = False

    # Таймеры для цифр
    food_timer = []

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

        # Движение головы змейки
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

        # Проверка на выход за границы экрана и телепортация
        if snake_pos[0] >= screen_width:
            snake_pos[0] = 0
        elif snake_pos[0] < 0:
            snake_pos[0] = screen_width - snake_block
        if snake_pos[1] >= screen_height:
            snake_pos[1] = 0
        elif snake_pos[1] < 0:
            snake_pos[1] = screen_height - snake_block

        # Обновление позиции тела змейки
        new_body = []
        for i in range(len(snake_body)):
            if i == 0:
                new_body.append([snake_body[i][0], snake_pos[0], snake_pos[1], angle])  # Угол для головы
            else:
                prev_segment = snake_body[i - 1]
                new_body.append([snake_body[i][0], prev_segment[1], prev_segment[2], prev_segment[3]])

        snake_body = new_body

        if game_continued:
            # Генерация новых "цифр-еды" если еще не на экране
            if not food_pos:
                food_pos = []
                food_timer = []
                for _ in range(random.randint(1, 3)):
                    food_pos.append([random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                                     random.randint(0, (screen_height - snake_block) // snake_block) * snake_block,
                                     random.choice("123456789")])
                    # Устанавливаем таймер для каждой цифры
                    food_timer.append(time.time() + random.randint(3, 5))

            # Проверка на столкновение с цифрами
            for i, food in enumerate(food_pos[:]):
                if is_collision(snake_pos, food[:2]):
                    score += int(food[2]) * 100  # Добавляем очки
                    food_pos.pop(i)  # Убираем съеденную еду
                    food_timer.pop(i)  # Убираем соответствующий таймер

            # Удаление еды по истечении времени
            current_time = time.time()
            food_pos = [food for i, food in enumerate(food_pos) if current_time < food_timer[i]]
            food_timer = [timer for timer in food_timer if current_time < timer]

        # Проверка на столкновение с "едой"
        if not game_continued and is_collision(snake_pos, food_pos):
            # Добавляем новый сегмент с углом головы
            snake_body.append([food_list[food_index], food_pos[0], food_pos[1], angle])
            score += 1000  # Начисляем 1000 очков за каждую букву
            food_index += 1

            if food_index < len(food_list):
                food_pos = [random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                            random.randint(0, (screen_height - snake_block) // snake_block) * snake_block]
                # Добавляем новый огонь только в первой фазе
                fire_list.append(['~', random.randint(0, (screen_width - snake_block) // snake_block) * snake_block,
                                  random.randint(0, (screen_height - snake_block) // snake_block) * snake_block])
            else:
                game_continued = True  # Начало второй фазы игры
                food_pos = []

        # Обновление огня
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

            # Проверка на выход за границы экрана и телепортация
            if fire[1] >= screen_width:
                fire[1] = 0
            elif fire[1] < 0:
                fire[1] = screen_width - snake_block
            if fire[2] >= screen_height:
                fire[2] = 0
            elif fire[2] < 0:
                fire[2] = screen_height - snake_block

            # Проверка на столкновение с огнем
            if is_collision(snake_pos, fire[1:]):
                game_over = True

        screen.fill(black)

        # Рисуем змейку
        for segment in snake_body:
            letter, x, y, angle = segment
            message(letter, white, [x + snake_block // 2, y + snake_block // 2], angle=angle)

        # Рисуем текущую "еду"
        if game_continued:
            for food in food_pos:
                message(food[2], dark_green, [food[0] + snake_block // 2, food[1] + snake_block // 2])
        else:
            message(food_list[food_index], white, [food_pos[0] + snake_block // 2, food_pos[1] + snake_block // 2])

        # Рисуем огонь
        for fire in fire_list:
            message('~', red, [fire[1] + snake_block // 2, fire[2] + snake_block // 2])

        # Рисуем очки
        show_score(score, record)

        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

    # Обновляем рекорд, если текущий счет больше
    if score > record:
        save_record(score)

    # Завершение игры
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

# Запуск меню
main_menu()
