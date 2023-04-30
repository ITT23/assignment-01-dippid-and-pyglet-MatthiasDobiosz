import random

from DIPPID import SensorUDP
import pyglet
from pyglet import shapes, clock
import numpy as np
import sys

PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

player = pyglet.image.load('../assets/Audi.png')


class Game:

    def __init__(self):
        self.player = Player(100, 200)
        self.road = Road()
        self.currentSpeed = 1
        self.levelTimer = 0

    def update(self, delta_time):
        update_cars(self.currentSpeed)

    def update_speed(self, delta_time):
        if self.road.diff == 80 and self.levelTimer == self.currentSpeed * 10:
            if self.currentSpeed == 1:
                self.currentSpeed = 2
            elif self.currentSpeed == 2:
                self.currentSpeed = 4
            self.road.update_speed(self.currentSpeed)
            self.levelTimer = 0
        elif self.road.diff == 80:
            self.levelTimer += 1

    def check_collision(self, delta_time):
        for car in Car.cars:
            if car.y <= self.player.height:
                if ((car.x + car.width >= self.player.x) and (
                        car.x + car.width <= self.player.x + self.player.width)) or (
                        (car.x <= self.player.x + self.player.width) and (
                        car.x > self.player.x)):
                    car.destroy()
                    self.player.checkLives()

    def reset(self):
        self.currentSpeed = 1
        Car.cars = []
        self.player.reset()
        self.road.reset()


def update_cars(speed):
    for car in Car.cars:
        car.update(speed)


def no_overlap(new_car, new_car_width):
    for car in Car.cars:
        if (car.y + car.height > new_car.y) and (
                (car.x <= new_car.x <= (car.x + car.width)) or (
                car.x <= new_car.x + new_car_width <= (car.x + car.width))):
            return False
    return True


class Car:
    cars = []

    def __init__(self, x, width):
        self.x = x
        self.y = WINDOW_HEIGHT
        self.height = 100
        self.width = width
        self.color = (55, 55, 255)
        self.shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                      height=self.height, color=self.color)

    def update(self, speed):
        self.y = self.y - speed
        updated_shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                         height=self.height, color=self.color)
        self.shape = updated_shape

        if self.y < -self.height:
            Car.cars.remove(self)

    def draw(self):
        self.shape.draw()

    def destroy(self):
        Car.cars.remove(self)


def draw_cars():
    for car in Car.cars:
        car.draw()


def create_car(delta_time):
    if random.randint(0, 10) == 0:
        width = 50
        x = random.randint(0, WINDOW_WIDTH - width)
        new_car = Car(x, width)
        if no_overlap(new_car, width):
            Car.cars.append(Car(x, width))


class Road:

    def __init__(self):
        self.lanes = 4
        self.strings = 10
        self.color = (255, 255, 255)
        self.diff = 0
        self.speed = 1

    def draw(self):
        for x in range(1, self.lanes):
            block_x = (WINDOW_WIDTH / self.lanes) * x
            for y in range(0, self.strings + 1):
                block_y = ((WINDOW_HEIGHT / self.strings) * y) - self.diff
                block = shapes.Rectangle(x=block_x, y=block_y, width=10,
                                         height=40, color=self.color)
                block.draw()
        if self.diff >= (WINDOW_HEIGHT / self.strings):
            self.diff = 0
        else:
            self.diff += self.speed

    def update_speed(self, speed):
        self.speed = speed

    def reset(self):
        self.diff = 0
        self.speed = 1


class Player:

    def __init__(self, width, height):
        self.x = WINDOW_WIDTH / 2 - width / 2
        self.y = 0
        self.width = width
        self.height = height
        self.color = (55, 55, 255)
        self.shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                      height=self.height, color=self.color)
        self.sprite = pyglet.sprite.Sprite(img=player, x=self.x, y=self.y)
        self.lives = 3
        self.label = pyglet.text.Label('Lives: ' + str(self.lives),
                                       font_name='Times New Roman',
                                       font_size=18,
                                       x=50, y=50,
                                       anchor_x='center', anchor_y='center')

    def draw(self):
        self.shape.draw()

    def update_movement(self, delta_time):
        if sensor.has_capability('accelerometer'):
            acc_x = float(sensor.get_value('accelerometer')['x'])
            if acc_x < 0:
                if self.x < WINDOW_WIDTH - self.width:
                    self.move(10)
            else:
                if self.x > 0:
                    self.move(-10)

            if sensor.has_capability('button_1'):
                button_data = sensor.get_value('button_1')
                if int(button_data) == 1:
                    if acc_x < 0:
                        self.move(-(WINDOW_WIDTH - self.x + self.width))

    def move(self, dt):
        self.x = self.x + dt
        self.shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                      height=self.height, color=self.color)
        self.sprite = pyglet.sprite.Sprite(img=player, x=self.x, y=self.y)

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


# initialize new GameState
game = Game()


@window.event
def on_draw():
    window.clear()
    if game.player.lives == 0:
        pyglet.text.Label('Game Over',
                          font_name='Times New Roman',
                          font_size=36,
                          x=WINDOW_WIDTH / 2,
                          y=WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center').draw()
    else:
        game.player.label.draw()
        game.road.draw()
        game.player.draw()
        draw_cars()
        game.update(game.currentSpeed)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.E:
        game.reset()


clock.schedule_interval(game.player.update_movement, 0.01)
clock.schedule_interval(create_car, 0.1)
clock.schedule_interval(game.check_collision, 0.1)
clock.schedule_interval(game.update_speed, 0.01)

pyglet.app.run()
