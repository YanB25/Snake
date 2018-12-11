import json
from snake import Snake
from fruit import Fruit
import queue
import copy
class PathSolve():
    def __init__(self, snake, fruit, config):
        self.snake = copy.copy(snake)
        self.fruit = copy.copy(fruit)
        self.config = config
        width = int(config['window-width'])
        height = int(config['window-height'])
        blk = int(config['block-size'])
        self.width = int(width / blk)
        self.height = int(height / blk)
        self.delX = [0, 0, -1, 1]
        self.delY = [-1, 1, 0, 0]
        self.dir = ['U', 'D', 'L', 'R']
        self.rev_dir = ['D', 'U', 'R', 'L']
        self.rev_map = {
            'U': 'D',
            'D': 'U',
            'L': 'R', 
            'R': 'L'
        }
    def shortest_path(self):
        print('fruit', self.fruit.where())
        print('snake', self.snake.head())
        game_map = [
            ['O' for i in range(self.width)]
            for j in range(self.height)
        ]
        dir_map = copy.deepcopy(game_map)

        for x, y in self.snake.snakebody[1:]:
            game_map[y][x] = 'X' # block
        PathSolve.printList(game_map)
        x, y = self.fruit.where()
        game_map[y][x] = 'F'

        q = queue.Queue()
        q.put(self.snake.head())

        while not q.empty():
            x, y = q.get()
            # print(x, y, game_map[y][x])
            if game_map[y][x] != 'O':
                continue
            # print(x, y)
            game_map[y][x] = 'X'
            for i in range(4):
                nx = x + self.delX[i]
                ny = y + self.delY[i]
                if not self.isValid(nx, ny):
                    continue
                if game_map[ny][nx] == 'F':
                    dir_map[ny][nx] = self.rev_dir[i]
                    return True, self.__findPath(dir_map)
                if game_map[ny][nx] != 'O':
                    continue
                q.put((nx, ny))
                # print('put', nx, ny)
                dir_map[ny][nx] = self.rev_dir[i]
        return False, []
    def __findPath(self, dir_map):
        PathSolve.printList(dir_map)

        x, y = self.fruit.where()
        ret = []
        while dir_map[y][x] != 'O':
            ret.append(self.rev_map[dir_map[y][x]])
            i = self.dir.index(dir_map[y][x])
            print('step', dir_map[y][x], i)
            nx = self.delX[i]
            ny = self.delY[i]
            x, y = x + nx, y + ny
        return ret[::-1]
    @staticmethod
    def printList(ls):
        for i in ls:
            print(i)
        print()
                
    def isValid(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

if __name__ == '__main__':
    dt = None
    with open('config.json', 'r') as f:
        dt = json.load(f)

    snake = Snake()
    fruit = Fruit(dt)
    fruit.last_generate = (8, 5)
    solver = PathSolve(snake, fruit, dt)
    print(solver.shortest_path())