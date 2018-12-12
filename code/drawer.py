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
        self.spc = 0.1
        self.rect_ud = pygame.Rect(0, 0, self.blk * (1 - 2*self.spc), self.blk)
        self.rect_lr = pygame.Rect(0, 0, self.blk, self.blk * (1- 2*self.spc))
        self.rect_udhalf = pygame.Rect(0, 0, self.blk * (1-2*self.spc), self.blk * (1 - self.spc))
        self.rect_lrhalf = pygame.Rect(0, 0, self.blk * (1 - self.spc), self.blk * (1- 2*self.spc))
    def _basic_draw(self, x, y, color, _type='normal'):
        if _type == 'normal':
            self.rect.topleft = self._toLeftTop(x, y)
            pygame.draw.rect(self.screen, color, self.rect)
        elif _type == 'ud':
            self.rect_ud.topleft = self._toLeftTop(x, y, 'ud')
            pygame.draw.rect(self.screen, color, self.rect_ud)
        elif _type == 'lr':
            self.rect_lr.topleft = self._toLeftTop(x, y, 'lr')
            pygame.draw.rect(self.screen, color, self.rect_lr)
        elif _type in ['ul', 'ur', 'dl', 'dr']:
            self.rect_udhalf.topleft = self._toLeftTop(x, y, _type[0])
            pygame.draw.rect(self.screen, color, self.rect_udhalf)
            self.rect_lrhalf.topleft = self._toLeftTop(x, y, _type[1])
            pygame.draw.rect(self.screen, color, self.rect_lrhalf)
        elif _type in ['uh', 'dh']:
            self.rect_udhalf.topleft = self._toLeftTop(x, y, _type[0])
            pygame.draw.rect(self.screen, color, self.rect_udhalf)
        elif _type in ['lh', 'rh']:
            self.rect_lrhalf.topleft = self._toLeftTop(x, y, _type[0])
            pygame.draw.rect(self.screen, color, self.rect_lrhalf)
        else:
            assert(False)
    def _toLeftTop(self, x, y, _type='normal'):
        if _type == 'normal':
            return (x * self.blk, y * self.blk)
        elif _type == 'ud' or _type == 'u':
            return (x * self.blk + self.blk * self.spc, y * self.blk)
        elif _type == 'lr' or _type == 'l':
            return (x * self.blk, y * self.blk + self.blk * self.spc)
        elif _type == 'd' or _type == 'r':
            return (x * self.blk + self.blk * self.spc, y * self.blk + self.blk *self.spc)
        else:
            assert(False)
        

class SnakeDrawer(Drawer):
    def __init__(self, screen, config, snake):
        Drawer.__init__(self, screen, config)
        self.snake = snake
    def draw(self):
        head = self.snake.head()
        a = SnakeDrawer.relative_pos(head, self.snake.snakebody[1])
        # self.rect.topleft = self._toLeftTop(*head)
        # pygame.draw.rect(self.screen, RED, self.rect)
        self._basic_draw(head[0], head[1], RED, a + 'h')
        print(self.rect.topleft)

        for idx, body in enumerate(self.snake.snakebody[1:]):
            i = idx + 1
            before = self.snake.snakebody[i-1]
            if i + 1 < len(self.snake.snakebody):
                after = self.snake.snakebody[i + 1]
                a = SnakeDrawer.relative_pos(body, before)
                b = SnakeDrawer.relative_pos(body, after)
                if a in 'ud' and b in 'ud':
                    _type = 'ud'
                elif a in 'lr' and b in 'lr':
                    _type = 'lr'
                elif a in ['u', 'd']:
                    _type = '{}{}'.format(a, b)
                else:
                    _type = '{}{}'.format(b, a)
                print(_type)
                self.__draw(*body, _type)
            else:
                a = SnakeDrawer.relative_pos(body, before)
                if a in 'lr':
                    _type = a + 'h'
                elif a in 'ud':
                    _type = a + 'h'
                print(_type)
                self.__draw(*body, _type)

    @staticmethod
    def relative_pos(lhs, rhs):
        lx, ly = lhs
        rx, ry = rhs
        if lx == rx:
            if ly > ry:
                return 'u'
            if ly < ry:
                return 'd'
            assert(False)
        else:
            if lx > rx:
                return 'l'
            else:
                return 'r'

    def next(self):
        # tail = self.snake.tail()
        # self.__remove(*tail)
        # self.__remove(*self.snake.head())
        for body in self.snake.snakebody:
            self.__remove(*body)
        self.snake.next()
        self.draw()
        # x, y = self.snake.head()
        # self._basic_draw(x, y, RED)
    def __remove(self, x, y):
        self._basic_draw(x, y, WHITE, 'normal')
    def __draw(self, x, y, _type='normal'):
        self._basic_draw(x, y, BLACK, _type)

class FruitDrawer(Drawer):
    def __init__(self, screen, config, fruit):
        Drawer.__init__(self, screen, config)
        self.fruit = fruit
        self.width = int(int(config['window-width']) / config['block-size'])
        self.height = int(int(config['window-height']) / config['block-size'])
    def remove(self):
        x, y = self.fruit.where()
        self._basic_draw(x, y, WHITE)
    def draw(self):
        x, y = self.fruit.where()
        self._basic_draw(x, y, GREEN)
