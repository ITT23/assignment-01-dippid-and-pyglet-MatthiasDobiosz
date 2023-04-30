import pyglet
from pyglet import shapes
from Config import WINDOW_WIDTH


class Player:

    def __init__(self, img):
        self.img = img
        self.width = img.width
        self.height = img.height
        self.startX = WINDOW_WIDTH / 2 - img.img.width / 2
        self.startY = -img.offset_bottom
        self.spriteX = self.startX + img.offset_left
        self.sprite = pyglet.sprite.Sprite(img=self.img.img, x=self.startX,
                                           y=self.startY)
        self.color = (55, 55, 255)
        self.lives = 3
        self.freeze = False
        self.label = pyglet.text.Label('Lives: ' + str(self.lives),
                                       font_name='Times New Roman',
                                       font_size=18,
                                       x=50, y=50,
                                       anchor_x='center', anchor_y='center')

    def draw(self):
        self.sprite.draw()

    def update_movement(self, acc_x, button_1):
        if acc_x < 0:
            if self.spriteX < WINDOW_WIDTH - self.width:
                self.move(10)
        else:
            if self.spriteX > 0:
                self.move(-10)

        if int(button_1) == 1:
            self.freeze = True
        elif int(button_1) == 0:
            self.freeze = False

    def move(self, dt):
        if not self.freeze:
            self.startX = self.startX + dt
            self.spriteX = self.spriteX + dt
            self.sprite = pyglet.sprite.Sprite(img=self.img.img, x=self.startX,
                                               y=self.startY)

    def display_labels(self):
        self.label = pyglet.text.Label('Lives: ' + str(self.lives),
                                       font_name='Times New Roman',
                                       font_size=18,
                                       x=50, y=50,
                                       anchor_x='center',
                                       anchor_y='center')

    def checkLives(self):
        if self.lives > 0:
            self.lives -= 1
            self.display_labels()

    def reset(self):
        self.lives = 3
        self.display_labels()
        self.startX = WINDOW_WIDTH / 2 - self.img.img.width / 2
        self.startY = -self.img.offset_bottom
        self.spriteX = self.startX + self.img.offset_left
