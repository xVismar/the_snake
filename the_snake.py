import pygame
from random import randint


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока - красный
APPLE_BG_COLOR = (255, 0, 0)
APPLE_FG_COLOR = (220, 0, 0)

# Цвет змейки - зеленый
SNAKE_FG_COLOR = (0, 225, 0)
SNAKE_BG_COLOR = (0, 255, 0)

# Цвет сообщения - желтый
MSG_COLOR = (255, 255, 102)
# Скорость движения змейки (clock tic-rate):
SPEED = 15


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, b_color=None, fg_color=None):
        self.body_color = b_color
        self.fg_color = fg_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self, surface):
        pass


class Apple(GameObject):
    def __init__(self, b_color=APPLE_BG_COLOR, fg_color=APPLE_FG_COLOR):
        super().__init__()
        self.body_color = b_color
        self.fg_color = fg_color
        self.position = self.randomize_position()

    def randomize_position(self):
        self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
        return self.position

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, self.fg_color, rect, 1)


class Snake(GameObject):
    def __init__(self, b_color=SNAKE_BG_COLOR, fg_color=SNAKE_FG_COLOR):
        super().__init__()
        self.body_color = b_color
        self.fg_color = fg_color
        self.head_position = None
        self.positions = [self.position]

        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self, new_dir=None):
        self.next_direction = new_dir
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        return self.direction

    def get_head_position(self):
        self.head_position = self.positions[0]
        return self.head_position

    def grow(self):
        self.add_body = self.get_head_position()
        self.positions.insert(1, self.add_body)
        self.length += 1

    def move(self, dir=RIGHT, new_dir=None, grid_size=GRID_SIZE):
        snake_head = self.get_head_position()
        if self.direction == UP:
            self.positions.insert(0,
                                  (snake_head[0], (snake_head[1] - grid_size)))

        elif self.direction == DOWN:
            self.positions.insert(0,
                                  (snake_head[0], (snake_head[1] + grid_size)))

        elif self.direction == LEFT:
            self.positions.insert(0,
                                  ((snake_head[0] - grid_size), snake_head[1]))

        elif self.direction == RIGHT:
            self.positions.insert(0,
                                  ((snake_head[0] + grid_size), snake_head[1]))

        self.last = self.positions.pop()

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, self.fg_color, rect, 2)

            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, head_rect)
            pygame.draw.rect(surface, self.fg_color, head_rect, 2)

            if self.last:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def snake_reset(self):
        global Running
        global Game_Over
        screen.fill(BORDER_COLOR)
        message('GAME OVER!  Нажмите  C  -  попробовать снова'
                '  или  Q  -  покинуть программу')

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Running = False
                    Game_Over = False
                    pygame.quit()
                if event.key == pygame.K_c:
                    Running = True
                    Game_Over = False
                    main()


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            return game_object.next_direction


def message(msg, color=MSG_COLOR):
    font_style = pygame.font.SysFont("bahnschrift", 16)
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH // 16, SCREEN_HEIGHT // 5])


def main():
    pygame.init()
    apple = Apple()
    snake = Snake()

    Running = True
    Game_Over = False

    while Running:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        snake_head = snake.get_head_position()
        while Game_Over:
            snake.snake_reset()

        snake.move(snake.direction, snake.update_direction(handle_keys(snake)))
        pygame.display.update()

        if snake_head == apple.position:
            snake.grow()
            apple.randomize_position()
            pygame.display.update()
        elif snake.positions[0] in snake.positions[1:]:
            Game_Over = True
        elif snake_head[0] == SCREEN_WIDTH or snake_head[0] < 0:
            Game_Over = True
        elif snake_head[1] == SCREEN_HEIGHT or snake_head[1] < 0:
            Game_Over = True

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
