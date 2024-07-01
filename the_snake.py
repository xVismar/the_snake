import pygame as py
from random import randint as rand

"""
Автор - Alex Alekseev aka Vismar
Версия - 1.3
Дата - 01.07.2024

Код содержит скрипт игры Змейка, созданной с применением библиотеки Pygame
принципов ООП.

Основной игровой класс - GameObject
    Дочерние классы от GameObject:
        Snake - змея
        Apple - яблоко

Глобальные функции:
self.__init__  - Передаёт параметры класса при созднании нового объекта
self.draw - Отрисовка одной ячейки на сетке поля

Основной цикл игры (main()):
    Змейка постоянно двигается вперед в направлении snake.direciton.
    Проводится проверка с учётом положения self.next_direction и при "поедании"
    яблока - змея увеличивается на одну ячейку.

    Следующая проверка на столкнование головы и тела змеи.
        В случае, если голова == хвост:  змейка обнуляется до первоначальной.
        Если голова == не хвост: змейка двигается на одну ячейку вперед.
"""


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

# Связь клавиш со сменой направления движения змейки:
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

# Цвет тела яблока - красный
APPLE_BG_COLOR = (255, 0, 0)
# Цвет контура яблока
APPLE_FG_COLOR = (200, 55, 55)

# Цвет тела змейки - зеленый
SNAKE_BG_COLOR = (0, 255, 0)
# Цвет контура змейки
SNAKE_FG_COLOR = (45, 200, 45)

# Скорость движения змейки (clock tic-rate):
SPEED = 15

# Настройка игрового окна:
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
py.display.set_caption('Snake.Practikum by Vismar')

# Настройка времени:
clock = py.time.Clock()


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, body_color=None, fg_color=None):
        """Инициализация конструктора классов."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.body_color = body_color
        self.fg_color = fg_color

    def draw(self):
        """Отрисовка одной ячейки."""
        rect = py.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, rect)
        py.draw.rect(screen, self.fg_color, rect, 2)


class Apple(GameObject):
    """Дочерний класс Яблоко от родительского класса GameObject."""

    def __init__(self, body_color=APPLE_BG_COLOR, fg_color=APPLE_FG_COLOR,
                 used_cells=None):
        """Инициализация конструктора класса Apple."""
        super().__init__()
        self.body_color = body_color
        self.fg_color = fg_color
        self.occupied = used_cells
        self.randomize_position()

    def randomize_position(self, used_cell=None):
        """Случайное расположение Яблока на поле."""
        if used_cell is None:
            used_cell = self.occupied or []

        while True:
            new_position = ((rand(0, GRID_WIDTH - 1) * GRID_SIZE),
                            (rand(0, GRID_HEIGHT - 1) * GRID_SIZE))
            if new_position not in used_cell:
                self.position = new_position
                break
        self.position = self.position or used_cell

    def draw(self):
        """Отрисовка Яблока на экране."""
        rect = py.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, rect)
        py.draw.rect(screen, self.fg_color, rect, 1)


class Snake(GameObject):
    """Дочерний класс Змея от родительского класса GameObject."""

    def __init__(self, b_color=SNAKE_BG_COLOR, fg_color=SNAKE_FG_COLOR):
        """Инициализация конструктора класса Snake."""
        super().__init__()
        self.body_color = b_color
        self.fg_color = fg_color
        self.reset()

    def update_direction(self, new_dir=None):
        """Обновление направления движения змейки."""
        if not new_dir:
            return self.direction
        self.direction = new_dir
        self.next_direction = None
        return self.direction

    def get_head_position(self):
        """Получение текущего положения головы змейки."""
        self.head_position = self.positions[0]
        return self.head_position

    def grow(self):
        """Рост змейки при поедании яблока."""
        self.add_body = self.position
        self.positions.insert(1, self.add_body)
        self.length += 1

    def move(self, dir, new_dir, grid_size=GRID_SIZE):
        """Движение змейки."""
        sn_head_x, sn_head_y = self.get_head_position()
        sn_dir_x, sn_dir_y = self.direction
        sn_x_upd = (sn_head_x + (grid_size * sn_dir_x))
        sn_y_upd = (sn_head_y + (grid_size * sn_dir_y))

        # Ограничение движения змейки по границам экрана \ перенос головы
        if sn_x_upd not in range(0, (SCREEN_WIDTH - GRID_SIZE), GRID_SIZE):
            self.positions.insert(0, ((sn_x_upd % SCREEN_WIDTH), sn_y_upd))
        elif sn_y_upd not in range(0, (SCREEN_HEIGHT - GRID_SIZE), GRID_SIZE):
            self.positions.insert(0, (sn_x_upd, (sn_y_upd % SCREEN_HEIGHT)))
        else:
            self.positions.insert(0, (sn_x_upd, sn_y_upd))

        # Затирание хвоста, если он имеется
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка змейки."""
        head_rect = py.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, head_rect)
        py.draw.rect(screen, self.fg_color, head_rect, 2)

        # Затирание хвоста змеи (при его наличии)
        if self.last:
            last_rect = py.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            py.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Обнуление змейки при столкновении с собой."""
        self.head_position = None
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработка нажатий клавиш и кнопки X на окне игры."""
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
        if event.type == py.KEYDOWN:
            for key, dir in DIR_KEYS:
                if event.key == key and game_object.direction != dir:
                    game_object.next_direction = DIR_KEYS[(key, dir)]
                    return game_object.next_direction


def main():
    """Основная функция.
    Инициализирует игровые объекты.
    Запускает игровой цикл.
    Обновляет экран.
    """
    py.init()
    apple = Apple()
    snake = Snake()

    Running = True

    screen.fill(BOARD_BACKGROUND_COLOR)

    # Игровой цикл:
    while Running:
        clock.tick(SPEED)

        # Проверка съедания яблока и рост змеи
        if not snake.get_head_position() == apple.position:
            snake.move(snake.direction,
                       snake.update_direction(handle_keys(snake)))
        else:
            snake.grow()
            snake.move(snake.direction,
                       snake.update_direction(handle_keys(snake)))
            apple.randomize_position(snake.positions)

        # Проверка столкновения головы змеи с собой
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
            snake.reset()

        apple.draw()
        snake.draw()
        # Обновление экрана (отрисовка  элементов)
        py.display.update()
    # Выход из программы
    py.quit()


if __name__ == '__main__':
    main()
