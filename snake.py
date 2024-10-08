import pygame
import random
import time

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

width, height = 600, 500
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

snake_block = 15  
snake_speed = 15

apple = pygame.image.load('apple.png')  
apple = pygame.transform.scale(apple, (25, 25))

bonus_apple_size = 40  
bonus_apple = pygame.image.load('apple.png')
bonus_apple = pygame.transform.scale(bonus_apple, (bonus_apple_size, bonus_apple_size))
bonus_points = 5  

def draw_apple(x, y):
    display.blit(apple, (x, y))

def draw_bonus_apple(x, y):
    display.blit(bonus_apple, (x, y))

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(display, red, [segment[0], segment[1], snake_block, snake_block])

font_style = pygame.font.SysFont("Arial", 25)
score_font = pygame.font.SysFont("Times New Roman", 35)

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    display.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    bonus_active = False
    bonus_start_time = 0
    bonus_lifetime = 3  
    bonus_interval = 10  
    bonusx, bonusy = 0, 0  

    score = 0  

    while not game_over:

        while game_close:
            display.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", white)
            your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        display.fill(black)

        draw_apple(foodx, foody)

        if score % bonus_interval == 0 and score > 0 and not bonus_active:
            bonus_active = True
            bonus_start_time = time.time()
            bonusx = round(random.randrange(0, width - bonus_apple_size) / 10.0) * 10.0
            bonusy = round(random.randrange(0, height - bonus_apple_size) / 10.0) * 10.0

        if bonus_active:
            draw_bonus_apple(bonusx, bonusy)
            if time.time() - bonus_start_time > bonus_lifetime:
                bonus_active = False

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_list)
        your_score(score)

        pygame.display.update()

        if (foodx <= x1 <= foodx + 25) and (foody <= y1 <= foody + 25):
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1  
            score += 1  

        if bonus_active and (bonusx <= x1 <= bonusx + bonus_apple_size) and (bonusy <= y1 <= bonusy + bonus_apple_size):
            length_of_snake += 2  
            score += bonus_points  
            bonus_active = False  

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
