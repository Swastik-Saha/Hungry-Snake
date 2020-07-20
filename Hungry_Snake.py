import pygame
import random
import sys

pygame.mixer.init()

pygame.init()


# Colors
black = (0, 0, 0)

# Creating Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hungry Snake")
pygame.display.update()

playground_img = pygame.image.load("playground.jpg")
playground_img = pygame.transform.scale(playground_img, (screen_width, screen_height)).convert_alpha()

welcome_img = pygame.image.load("welcome_img.jpg")
welcome_img = pygame.transform.scale(welcome_img, (screen_width, screen_height)).convert_alpha()

game_over_img = pygame.image.load("game_over_img.jpg")
game_over_img = pygame.transform.scale(game_over_img, (screen_width, screen_height)).convert_alpha()

food_color_list = [(136, 0, 204), (255, 255, 0), (102, 26, 0), (128, 255, 255), (200, 100, 10),
                   (230, 0, 230), (255, 128, 255), (255, 0, 102), (255, 0, 0), (153, 0, 51)]

clock = pygame.time.Clock()
font = pygame.font.SysFont("Cooper Black", 55)
fps = 60


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(game_window, color_head, color_body, snake_body_list, snake_size):
    for x, y in snake_body_list:
        if [x, y] == snake_body_list[-1]:
            pygame.draw.rect(game_window, color_head, [x, y, snake_size, snake_size])

        else:
            pygame.draw.rect(game_window, color_body, [x, y, snake_size, snake_size])


def welcome():
    gameWindow.blit(welcome_img, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(fps)


# Game Loop
def gameloop():

    # Game Specific Variables
    game_over = False

    snake_x = 200
    snake_y = 200

    velocity_x = 0
    velocity_y = 0

    snake_list = []
    snake_length = 1

    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    food_color = random.choice(food_color_list)

    snake_size = 20
    snake_velocity = 5
    snake_body_color = black
    snake_face_color = food_color

    score = 0

    try:
        with open("High_Score.txt", 'r') as f:
            high_score = int(f.read())
    except:
        high_score = 0

    while True:

        if game_over:
            gameWindow.blit(game_over_img, (0, 0))
            text_screen(f"High Score: {high_score}", (138, 255, 138), 5, 5)
            text_screen(f"Your Score: {score}", (138, 255, 138), 5, 60)

            with open("High_Score.txt", 'w') as f_obj:
                f_obj.write(str(high_score))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if velocity_x != -snake_velocity:
                            velocity_x = snake_velocity
                            velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        if velocity_x != snake_velocity:
                            velocity_x = - snake_velocity
                            velocity_y = 0

                    if event.key == pygame.K_UP:
                        if velocity_y != snake_velocity:
                            velocity_x = 0
                            velocity_y = - snake_velocity

                    if event.key == pygame.K_DOWN:
                        if velocity_y != -snake_velocity:
                            velocity_x = 0
                            velocity_y = snake_velocity

                    if event.key == pygame.K_q:  # Cheat Code
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:    # If Snake eats food
                pygame.mixer.music.load("apple_eating.mp3")
                pygame.mixer.music.play()
                food_color = random.choice(food_color_list)
                snake_face_color = food_color
                score += 10
                if score > high_score:
                    high_score = score
                snake_length += 5

                food_x = random.randint(50, screen_width - 50)
                food_y = random.randint(50, screen_height - 50)

            gameWindow.blit(playground_img, (0, 0))
            text_screen(f"High Score: {high_score}", (0, 0, 121), 5, 5)
            text_screen(f"Your Score: {score}", (0, 0, 121), 5, 60)
            pygame.draw.circle(gameWindow, food_color, (food_x, food_y), 12)  # Creating food

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("game_lose.mp3")
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("game_lose.mp3")
                pygame.mixer.music.play()

            # Creating our Snake
            plot_snake(gameWindow, snake_face_color, snake_body_color, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    welcome()
