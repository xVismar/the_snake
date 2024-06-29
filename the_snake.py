import pygame as py
from random import randint as rand


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

# Соотношение клавиш\реверса направления и значением изменения:
DIR_KEYS = {
    (py.K_UP, DOWN): UP,
    (py.K_DOWN, UP): DOWN,
    (py.K_LEFT, RIGHT): LEFT,
    (py.K_RIGHT, LEFT): RIGHT
}

# Границы поля по высоте(H) и ширине(W):
EDGE_H = {(DOWN, 1): SCREEN_HEIGHT, (UP, -1): 0}
EDGE_W = {(LEFT, -1): 0, (RIGHT, 1): SCREEN_WIDTH}


# Цвет фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока - красный
APPLE_BG_COLOR = (255, 0, 0)
APPLE_FG_COLOR = (200, 55, 55)

# Цвет змейки - зеленый
SNAKE_FG_COLOR = (45, 200, 45)
SNAKE_BG_COLOR = (0, 255, 0)

# Скорость движения змейки (clock tic-rate):
SPEED = 15

# Настройка игрового окна:
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
py.display.set_caption('Snake.Practikum by Vismar')

# Настройка времени:
clock = py.time.Clock()


class GameObject:
    """Базовый класс объектов игры"""

    def __init__(self, body_color=None, fg_color=None):
        self.body_color = body_color
        self.fg_color = fg_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self, pos=None, body_color=None, fg_color=None):
        """Отрисовка одной ячейки"""
        if pos is None:
            pos = self.position
        if body_color is None:
            body_color = self.body_color
        if fg_color is None:
            fg_color = self.fg_color

        rect = py.Rect(pos, (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, rect)
        py.draw.rect(screen, self.fg_color, rect, 2)


class Apple(GameObject):
    """Дочерний класс Яблоко от родительского класса GameObject"""

    def __init__(self, body_color=APPLE_BG_COLOR, fg_color=APPLE_FG_COLOR):
        super().__init__()
        self.body_color = body_color
        self.fg_color = fg_color
        self.randomize_position()

    def randomize_position(self, snake_pos=None):
        """Случайное расположение Яблока на поле"""
        self.position = ((rand(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (rand(0, GRID_HEIGHT - 1) * GRID_SIZE))
        if snake_pos is not None:
            while self.position in snake_pos:
                self.position = ((rand(0, GRID_WIDTH - 1) * GRID_SIZE),
                                 (rand(0, GRID_HEIGHT - 1) * GRID_SIZE))

    def draw(self):
        """Отрисовка Яблока на экране"""
        rect = py.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, rect)
        py.draw.rect(screen, self.fg_color, rect, 1)


class Snake(GameObject):
    """Дочерний класс Змея от родительского класса GameObject"""

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
        """Обновление направления движения змейки"""
        self.next_direction = new_dir
        if not self.next_direction:
            return self.direction
        self.direction = self.next_direction
        self.next_direction = None
        return self.direction

    def get_head_position(self):
        """Получение текущего положения головы змейки"""
        self.head_position = self.positions[0]
        return self.head_position

    def grow(self):
        """Рост змейки при поедании яблока"""
        self.add_body = self.get_head_position()
        self.positions.insert(1, self.add_body)
        self.length += 1

    def move(self, dir=RIGHT, new_dir=None, grid_size=GRID_SIZE):
        """Движение змейки"""
        snake_head = self.get_head_position()
        sn_head_x = snake_head[0]
        sn_head_y = snake_head[1]
        sn_dir_x, sn_dir_y = self.direction
        sn_x_upd = (sn_head_x + (grid_size * sn_dir_x))
        sn_y_upd = (sn_head_y + (grid_size * sn_dir_y))
        self.positions.insert(0, (sn_x_upd, sn_y_upd))

        # Затирание хвоста если длинна змеи больше одной ячейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

        # Обновление позиции змеи при достижении края экрана на противоположную
        if sn_head_y >= SCREEN_HEIGHT:
            self.positions.pop(0)
            self.positions.insert(0, (sn_head_x, 0))
        if sn_head_y < 0:
            self.positions.pop(0)
            self.positions.insert(0, (sn_head_x, (SCREEN_HEIGHT - grid_size)))
        if sn_head_x >= SCREEN_WIDTH:
            self.positions.pop(0)
            self.positions.insert(0, (0, sn_head_y))
        if sn_head_x < 0:
            self.positions.pop(0)
            self.positions.insert(0, ((SCREEN_WIDTH - grid_size), sn_head_y))

    def draw(self):
        """Отрисовка змейки"""
        head_rect = py.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, head_rect)
        py.draw.rect(screen, self.fg_color, head_rect, 2)

        if self.last:
            last_rect = py.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            py.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Обнуление змейки при столкновении с собой"""
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.__init__()


def handle_keys(game_object):
    """Обработка нажатий клавиш и кнопки X на окне игры"""
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
        if event.type == py.KEYDOWN:
            for key, dir in DIR_KEYS:
                if event.key == key and game_object.direction != dir:
                    game_object.next_direction = DIR_KEYS[(key, dir)]
                    return game_object.next_direction


def main():
    """Основной цикл игры"""
    py.init()
    apple = Apple()
    snake = Snake()

    Running = True

    screen.fill(BOARD_BACKGROUND_COLOR)

    while Running:
        clock.tick(SPEED)
        snake_head = snake.get_head_position()
        snake.move(snake.direction, snake.update_direction(handle_keys(snake)))

        # Проверка съедания яблока и рост змеи
        if snake_head == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        # Проверка столкновения головы змеи с собой
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        apple.draw()
        snake.draw()

        py.display.update()

    py.quit()


if __name__ == '__main__':
    main()
