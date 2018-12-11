import random
class Fruit:
    def __init__(self, config):
        self.config = config
        self.width = int(int(config['window-width']) / int(config['block-size']))
        self.height = int(int(config['window-height']) / int(config['block-size']))
        self.last_generate = None
    def generate(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.last_generate = (x, y)
        return (x, y)
    def where(self):
        if self.last_generate is None:
            self.generate()
        return self.last_generate
        