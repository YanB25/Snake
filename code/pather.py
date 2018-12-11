import json
from snake import Snake
from fruit import Fruit
import queue
import copy
class PathSolve():
    def __init__(self, snake, fruit, config):
        self.snake = copy.deepcopy(snake)
        self.fruit = copy.deepcopy(fruit)
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
    def shortest_path(self, target):
        '''
        find the shortest path. snake body is blocked.
        @param target tuple of size 2. the x-y pair of destination
        @ret Tuple(Boolean, List[Str]). first element tells you whether
            it has a shortest path. Second element tells you the path from 
            SNAKE HEAD to target. Empty list if no path.
        '''
        # print('target', target)
        # print('snake', self.snake.head())
        game_map = [
            ['O' for i in range(self.width)]
            for j in range(self.height)
        ]
        dir_map = copy.deepcopy(game_map)

        for x, y in self.snake.snakebody[1:]:
            game_map[y][x] = 'X' # block
        # PathSolve.printList(game_map)
        x, y = target
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
                    return True, self.__findPath(dir_map, target)
                if game_map[ny][nx] != 'O':
                    continue
                q.put((nx, ny))
                # print('put', nx, ny)
                dir_map[ny][nx] = self.rev_dir[i]
        return False, []
    def longest_path(self, target):
        y, sp = self.shortest_path(target)
        if not y:
            return False, []

        game_map = [
            ['O' for i in range(self.width)]
            for j in range(self.height)
        ]
        for x, y in self.snake.snakebody:
            game_map[y][x] = 'X'
        
        idx = 0
        cur = self.snake.head()
        while True:
            extended = False
            direction = sp[idx]                    
            if direction in ['U', 'D']:
                test_extend = ['L', 'R']
            else:
                assert(direction in ['L', 'R'])
                test_extend = ['U', 'D']
            
            next_cur = self.pos_move(cur[0], cur[1], direction)
            for d in test_extend:
                t1 = self.pos_move(cur[0], cur[1], d)
                t2 = self.pos_move(next_cur[0], next_cur[1], d)
                if self.__exstendable(*t1, game_map) and self.__exstendable(*t2, game_map):
                    extended = True
                    sp.insert(idx, d)
                    sp.insert(idx + 2, self.rev_map[d])
                    x, y = t1
                    game_map[y][x] = 'X'
                    x, y = t2
                    game_map[y][x] = 'X'
                    break
            if not extended:
                cur = next_cur
                idx += 1
                if idx >= len(sp):
                    break
        return True, sp





    def __findPath(self, dir_map, target):
        '''
        inner function called by shortest path
        '''
        # PathSolve.printList(dir_map)

        x, y = target
        ret = []
        while dir_map[y][x] != 'O':
            ret.append(self.rev_map[dir_map[y][x]])
            i = self.dir.index(dir_map[y][x])
            # print('step', dir_map[y][x], i)
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
    def __exstendable(self, x, y, game_map):
        return self.isValid(x, y) and game_map[y][x] == 'O'
    def pos_move(self, x, y, d):
        i = self.dir.index(d)
        delX = self.delX[i]
        delY = self.delY[i]
        return (x + delX, y + delY)
    def shortest_path_fruit(self):
        return self.shortest_path(self.fruit.where())
    def longest_path_tail(self):
        return self.longest_path(self.snake.snakebody[-1])
        

if __name__ == '__main__':
    dt = None
    with open('config.json', 'r') as f:
        dt = json.load(f)

    with open ('output_9223372036568707794.log', 'r') as flog:
        data = flog.read()
    data = data.strip().split('\n')

    snake = Snake()
    snake.snakebody = []
    for d in data:
        x, y = d.split(' ')
        x = int(x)
        y = int(y)
        snake.snakebody.append((x, y))


    fruit = Fruit(dt)
    fruit.last_generate = (3, 8)
    solver = PathSolve(snake, fruit, dt)
    # print(solver.longest_path(fruit.where()))
    print(solver.longest_path(snake.snakebody[-1]))