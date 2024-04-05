import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 10

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        self.score = 0

    def move(self):
        head = (self.body[0][0] + self.direction[0] * 20, self.body[0][1] + self.direction[1] * 20)
        self.body.insert(0, head)
        if self.body[0][0] >= WIDTH:
            self.body[0] = (0, self.body[0][1])
        elif self.body[0][0] < 0:
            self.body[0] = (WIDTH - 20, self.body[0][1])
        elif self.body[0][1] >= HEIGHT:
            self.body[0] = (self.body[0][0], 0)
        elif self.body[0][1] < 0:
            self.body[0] = (self.body[0][0], HEIGHT - 20)
        self.body.pop()

    def change_direction(self, direction):
        if direction[0] * -1 != self.direction[0] or direction[1] * -1 != self.direction[1]:
            self.direction = direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], 20, 20))

class Food:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], 20, 20))

# Функция вывода текста на экран
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

snake = Snake()
food = Food()

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1, 0))

    snake.move()

    # Проверка на столкновение с едой
    if snake.body[0] == food.position:
        snake.body.append(snake.body[-1])
        food.position = (random.randint(0, (WIDTH - 20) // 20) * 20, random.randint(0, (HEIGHT - 20) // 20) * 20)
        snake.score += 1

    # После отрисовки всего, переворачиваем экран
    screen.fill(BLACK)
    snake.draw(screen)
    food.draw(screen)
    draw_text(screen, "Score: {}".format(snake.score), 18, WIDTH // 2, 10)
    pygame.display.flip()

pygame.quit()
