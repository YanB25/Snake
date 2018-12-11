import pygame
import json 
import timeit
import time
from snake import Snake
from drawer import SnakeDrawer
from drawer import FruitDrawer
from fruit import Fruit
if __name__ == '__main__':
    jsdt = None
    with open('config.json', 'r') as f:
        jsdt = json.load(f)
    WIDTH = int(jsdt['window-width'])
    HEIGHT = int(jsdt['window-height'])
    BLK = int(jsdt['block-size'])
    WID_BLK = WIDTH / BLK
    HEI_BLK = HEIGHT / BLK
    if WIDTH % BLK != 0 or HEIGHT % BLK != 0:
        raise Exception('Error block-size should divide window-width and window-height')
    SPEED = float(jsdt['speed'])

    pygame.init()
    logo = pygame.image.load('assets/logo.jpg')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Snake Game!')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    pygame.display.flip()

    snake = Snake()
    snakedrawer = SnakeDrawer(screen, jsdt, snake)
    fruit = Fruit(jsdt)
    fruitdrawer = FruitDrawer(screen, jsdt, fruit)
    
    while snake.at(fruit.where()):
        fruit.generate()

    snakedrawer.draw()
    fruitdrawer.draw()

    running = True
    beg_time = timeit.default_timer()
    while running:
        # time.sleep(SPEED / 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake.turnUp()
                if event.key == pygame.K_s:
                    snake.turnDown()
                if event.key == pygame.K_a:
                    snake.turnLeft()
                if event.key == pygame.K_d:
                    snake.turnRight()
                if event.key == pygame.K_q:
                    running = False
        now_time = timeit.default_timer()
        if now_time - beg_time >= SPEED:
            beg_time = now_time

            # check eat fruit
            if snake.nextHead() == fruit.where():
                snake.eatFruit()
                while snake.at(fruit.where()) or snake.nextHead() == fruit.where():
                    fruit.generate() # TODO:

            snakedrawer.next()
            fruitdrawer.draw()
            if not snake.valid():
                running = False
            x, y = snake.head()
            if x < 0 or x >= WID_BLK or y < 0 or y >= HEI_BLK:
                running = False
            pygame.display.flip()

        # do my work

    