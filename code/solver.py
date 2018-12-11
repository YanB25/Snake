import copy
class PathSolve():
    def __init__(self, snake, fruit, config):
        self.snake = copy.copy(snake)
        self.fruit = copy.copy(fruit)
        self.config = config
        width = int(jsdt['window-width'])
        height = int(jsdt['window-height'])
        blk = int(jsdt['block-size'])
        self.width = WIDTH / BLK
        self.height = HEIGHT / BLK
    def shortest_path(self):
        game_map = 