import pygame
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
class SnakeDrawer():
    def __init__(self, snake, screen, config):
        self.snake = snake
        self.blk = int(config['block-size'])
        self.rect = pygame.Rect(0, 0, self.blk, self.blk)
        self.screen = screen
    def draw(self):
        head = self.snake.head()
        self.rect.topleft = self.toLeftTop(*head)
        pygame.draw.rect(self.screen, RED, self.rect)
        print(self.rect.topleft)

        for body in self.snake.snakebody[1:]:
            self.__draw(*body)
        pygame.display.flip()

    def toLeftTop(self, x, y):
        return (x * self.blk, y * self.blk)
    def next(self):
        tail = self.snake.tail()
        self.__remove(*tail)
        self.snake.next()
        self.draw()
    def __remove(self, x, y):
        self.rect.topleft = self.toLeftTop(x, y)
        pygame.draw.rect(self.screen, WHITE, self.rect)
    def __draw(self, x, y):
        self.rect.topleft = self.toLeftTop(x, y)
        pygame.draw.rect(self.screen, BLACK, self.rect)