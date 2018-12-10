import pygame
import json 
import time
from snake import Snake
from drawer import SnakeDrawer
if __name__ == '__main__':
    jsdt = None
    with open('config.json', 'r') as f:
        jsdt = json.load(f)
    WIDTH = int(jsdt['window-width'])
    HEIGHT = int(jsdt['window-height'])
    BLK = int(jsdt['block-size'])
    if WIDTH % BLK != 0 or HEIGHT % BLK != 0:
        raise Exception('Error block-size should divide window-width and window-height')
    SPEED = int(jsdt['speed'])

    pygame.init()
    logo = pygame.image.load('assets/logo.jpg')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Snake Game!')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    pygame.display.flip()

    snake = Snake()
    drawer = SnakeDrawer(snake, screen, jsdt)
    drawer.draw()

    drawer.next()
    snake.turnUp()
    drawer.next()
    drawer.next()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # do my work

    