import pygame
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
class Drawer():
    def __init__(self, screen, config):
        self.blk = int(config['block-size'])
        self.rect = pygame.Rect(0, 0, self.blk, self.blk)
        self.screen = screen
    def _basic_draw(self, x, y, color):
        self.rect.topleft = self._toLeftTop(x, y)
        pygame.draw.rect(self.screen, color, self.rect)
    def _toLeftTop(self, x, y):
        return (x * self.blk, y * self.blk)

class SnakeDrawer(Drawer):
    def __init__(self, screen, config, snake):
        Drawer.__init__(self, screen, config)
        self.snake = snake
    def draw(self):
        head = self.snake.head()
        self.rect.topleft = self._toLeftTop(*head)
        pygame.draw.rect(self.screen, RED, self.rect)
        print(self.rect.topleft)

        for body in self.snake.snakebody[1:]:
            self.__draw(*body)

    def next(self):
        tail = self.snake.tail()
        self.__remove(*tail)
        self.snake.next()
        self.draw()
    def __remove(self, x, y):
        self._basic_draw(x, y, WHITE)
    def __draw(self, x, y):
        self._basic_draw(x, y, BLACK)

class FruitDrawer(Drawer):
    def __init__(self, screen, config, fruit):
        Drawer.__init__(self, screen, config)
        self.fruit = fruit
        self.width = int(int(config['window-width']) / config['block-size'])
        self.height = int(int(config['window-height']) / config['block-size'])
    def draw(self):
        x, y = self.fruit.where()
        self._basic_draw(x, y, GREEN)
