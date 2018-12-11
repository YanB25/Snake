import json
from snake import Snake 
from fruit import Fruit
from pather import PathSolve
import copy
class GreedySolver:
    def __init__(self, snake, fruit, config):
        self.snake = copy.deepcopy(snake)
        self.fruit = copy.deepcopy(fruit)
        self.pathsolver = PathSolve(snake, fruit, config)
        self.config = config
        width = int(config['window-width'])
        height = int(config['window-height'])
        blk = int(config['block-size'])
        self.width = int(width / blk)
        self.height = int(height / blk)
    def nextDirection(self):
        # step 1: compute shortest path
        hasPath, shortestPath = self.pathsolver.shortest_path_fruit()
        if hasPath:
            print('has path to eat fruit')
            # step 2: move virtual snake to the fruit
            virtual_snake = copy.deepcopy(self.snake)
            for d in shortestPath:
                virtual_snake.turn(d)
                virtual_snake.next()
            # step 3: compute the longest from virtual snake head to tail
            virtual_pather = PathSolve(virtual_snake, self.fruit, self.config)
            has_longest_path_tail, _ = virtual_pather.longest_path_tail()
            if has_longest_path_tail:
                # ok, great.
                print('can eat fruit and go out to my tail')
                print(shortestPath)
                return shortestPath[0]
            else:
                # step 4: no, I can not eat it.
                print('dangerous to eat fruit. ')
                hp3, lp3 = self.pathsolver.longest_path_tail()
                if hp3:
                    return lp3[0]
                # else, to case 5
        else:
            # step 4. compute longest from head to tail
            print('NO path to eat fruit')
            hp3, lp3 = self.pathsolver.longest_path_tail()
            if hp3:
                print('can touch my tail')
                return lp3[0]
            # else, to case 5
        

        # worst case, case 5
        print('fall back to worst case')
        hx, hy = self.snake.head()
        fx, fy = self.fruit.where()
        if hx > fx:
            return 'R'
        else:
            return 'L'

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
    fruit.last_generate = (8, 0)
    solver = GreedySolver(snake, fruit, dt)
    print(solver.nextDirection())