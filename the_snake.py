from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 5

DIRECTION = {(LEFT, pg.K_UP): UP,
             (RIGHT, pg.K_UP): UP,
             (UP, pg.K_LEFT): LEFT,
             (DOWN, pg.K_LEFT): LEFT,
             (DOWN, pg.K_RIGHT): RIGHT,
             (UP, pg.K_RIGHT): RIGHT,
             (LEFT, pg.K_DOWN): DOWN,
             (RIGHT, pg.K_DOWN): DOWN,
             }

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка. Выход: крестик или esc. + скорость: '
                       'enter. - скорость: space.')

clock = pg.time.Clock()


class GameObject:
    """The base class from which other game objects inherit."""

    def __init__(self):
        self.body_color = None
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Peparation of a method for
        drawing an object on the playing field.
        """
        raise NotImplementedError('You forgot to override the draw method in '
                                  'the child class.')

    def create_rect(self, position, body_color):
        """Responsible for creating a Rect and drawing the cell."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        if body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Describes the snake and its behavior: controls its movement,
    drawing, and also processes user actions.
    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Updates the direction of the snake's movement."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Updates the position of the snake by adding a new head to
        the beginning of the 'positions' list and removing the last
        element if the length of the snake has not increased.
        """
        head_position_1, head_position_2 = self.get_head_position()
        direction_1, direction_2 = self.direction
        self.position = (
            (head_position_1 + direction_1 * GRID_SIZE) % SCREEN_WIDTH,
            (head_position_2 + direction_2 * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Draws the snake on the screen, erasing the trace."""
        self.create_rect(self.positions[0], self.body_color)

        if self.last:
            self.create_rect(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state after
        colliding with itself.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


class Apple(GameObject):
    """Describes the apple and actions with it: position
    randomization and drawing.
    """

    def __init__(self, occupied_cells=[]):
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """Sets a random position of the apple on the playing field."""
        while True:
            position = (
                randint(0, (SCREEN_WIDTH - 20) // GRID_SIZE) * GRID_SIZE,
                randint(0, (SCREEN_HEIGHT - 20) // GRID_SIZE) * GRID_SIZE)
            if position not in occupied_cells:
                self.position = position
                break

    def draw(self):
        """Draws the apple on the screen."""
        self.create_rect(self.position, self.body_color)


def handle_keys(game_object):
    """Processes keystrokes to change the direction of the snake's movement."""
    global SPEED
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            elif event.key == pg.K_RETURN and SPEED < 51:
                SPEED += 5
            elif event.key == pg.K_SPACE and SPEED > 5:
                SPEED -= 5
            else:
                game_object.next_direction = DIRECTION.get(
                    (game_object.direction, event.key), game_object.direction)


def main():
    """Contains the main game loop."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.position in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
