import pyglet
from pyglet import shapes
from Config import WINDOW_HEIGHT, NUM_STRINGS_PER_LANE


# Road class that updates the segments
class RoadString:

    def __init__(self, x, y):
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.width = 10
        self.height = WINDOW_HEIGHT / NUM_STRINGS_PER_LANE / 2
        self.shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                      height=self.height, color=self.color)

    def update(self, speed):
        self.y = self.y - speed
        updated_shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                         height=self.height, color=self.color)
        self.shape = updated_shape

        if self.y < -self.height * 2:
            self.y = WINDOW_HEIGHT

        self.draw()

    def draw(self):
        self.shape.draw()
