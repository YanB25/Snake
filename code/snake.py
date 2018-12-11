UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3
class Snake():
    def __init__(
        self, 
        snakebody = [(5, 5), (6, 5), (7, 5)],
        direction = LEFT
        ):
        self.snakebody = snakebody
        self.direction = direction
        self.hasFruit = False
    def length(self):
        return len(self.snakebody)
    def head(self):
        return self.snakebody[0]
    def tail(self):
        return self.snakebody[-1]
    def direction(self):
        return self.direction
    def turnLeft(self):
        if self.direction != RIGHT:
            self.direction = LEFT
    def turnRight(self):
        if self.direction != LEFT:
            self.direction = RIGHT
    def turnUp(self):
        if self.direction != DOWN:
            self.direction = UP
    def turnDown(self):
        if self.direction != UP:
            self.direction = DOWN
    def nextHead(self):
        '''
        返回下一步蛇头会处于的位置
        '''
        if self.direction == UP:
            delX = 0
            delY = -1
        elif self.direction == DOWN:
            delX = 0
            delY = 1
        elif self.direction == LEFT:
            delX = -1
            delY = 0
        elif self.direction == RIGHT:
            delX = 1
            delY = 0
        else:
            assert(False)
        x, y = self.snakebody[0]
        return (x + delX, y + delY)
    def next(self):
        '''
        让蛇前进一步
        '''
        head = self.nextHead()
        self.snakebody.insert(0, head)
        if not self.hasFruit:
            self.snakebody.pop()
        self.hasFruit = False
        print(self.snakebody)
    def eatFruit(self):
        self.hasFruit = True
    def valid(self):
        for i in range(len(self.snakebody)):
            for j in range(0, i):
                if self.snakebody[i] == self.snakebody[j]:
                    return False
        return True
    def at(self, position):
        assert(type(position) == tuple)
        assert(len(position) == 2)
        for item in self.snakebody:
            if item == position:
                return True
        return False
    def dump(self, filename):
        wrs = ''
        for x, y in self.snakebody:
            wrs += '{} {}\n'.format(str(x), str(y))
        with open(filename, 'w') as f:
            f.write(wrs)
