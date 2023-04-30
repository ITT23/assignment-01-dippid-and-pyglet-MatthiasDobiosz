import pyglet
from pyglet import shapes
from Config import WINDOW_HEIGHT


class EnemyCar:
    cars = []

    def __init__(self, x, img):
        self.img = img
        self.x = x
        self.y = WINDOW_HEIGHT
        self.sprite_x = self.x + self.img.offset_left
        self.sprite_y = self.y + self.img.offset_bottom
        self.height = self.img.height
        self.width = self.img.width
        self.sprite = pyglet.sprite.Sprite(img=self.img.img, x=self.x,
                                           y=self.y)
        self.color = (55, 55, 255)

    def update(self, speed):
        self.y = self.y - speed
        self.sprite_y = self.sprite_y - speed
        self.sprite = pyglet.sprite.Sprite(img=self.img.img, x=self.x,
                                           y=self.y)

    def draw(self):
        self.sprite.draw()



