import random
from sprite import SpriteWithBbox
from DIPPID import SensorUDP
import pyglet
from pyglet import shapes, clock

PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

NUM_LANES = 5
NUM_STRINGS_PER_LINE = 10
RAISE_SPEED_TIME = 1000

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

playerimg = pyglet.image.load('../assets/Audi.png')
player = SpriteWithBbox(playerimg, 80, 80, 10, 10)

enemyimg = pyglet.image.load('../assets/taxi.png')
enemy = SpriteWithBbox(enemyimg, 70, 80, 20, 10)


class Game:

    def __init__(self):
        self.player = Player(player)
        self.currentSpeed = 2
        self.levelTimer = 0
        self.speedLevelLabel = pyglet.text.Label(
            'Level: 1',
            font_name='Times New Roman',
            font_size=18,
            x=50, y=100,
            anchor_x='center', anchor_y='center')
        self.gameOverLabel = pyglet.text.Label('Game Over',
                          font_name='Times New Roman',
                          font_size=36,
                          x=WINDOW_WIDTH / 2,
                          y=WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
        create_road()

    def draw(self):
        if self.player.lives == 0:
            self.gameOverLabel.draw()
            self.checkForRestart()
        else:
            self.player.label.draw()
            self.speedLevelLabel.draw()
            self.update(game.currentSpeed)
            draw_cars()
            self.player.draw()

    def checkForRestart(self):
        if sensor.has_capability('button_2'):
            button_data = sensor.get_value('button_2')
            if int(button_data) == 1:
                self.reset()

    def update(self, delta_time):
        update_cars(self.currentSpeed)
        update_road(self.currentSpeed)

    def update_speed(self, delta_time):
        if self.levelTimer == RAISE_SPEED_TIME:
            if self.currentSpeed == 2:
                self.currentSpeed = 4
            elif self.currentSpeed == 4:
                self.currentSpeed = 8
            self.levelTimer = 0
            self.update_speedLabel()
        else:
            self.levelTimer += 1

    def check_collision(self, delta_time):
        for car in Car.cars:
            if car.sprite_y <= self.player.height:
                if ((car.sprite_x + car.width >= self.player.spriteX) and (
                        car.sprite_x + car.width <= self.player.spriteX + self.player.width)) or (
                        (car.sprite_x <= self.player.spriteX + self.player.width) and (
                        car.sprite_x > self.player.spriteX)):
                    car.destroy()
                    self.player.checkLives()

    def reset(self):
        self.currentSpeed = 2
        self.levelTimer = 0
        Car.cars = []
        self.player.reset()
        self.update_speedLabel()

    def update_speedLabel(self):
        if self.currentSpeed == 2:
            self.speedLevelLabel = pyglet.text.Label(
                'Level: 1',
                font_name='Times New Roman',
                font_size=18,
                x=50, y=100,
                anchor_x='center', anchor_y='center')
        elif self.currentSpeed == 4:
            self.speedLevelLabel = pyglet.text.Label(
                'Level: 2',
                font_name='Times New Roman',
                font_size=18,
                x=50, y=100,
                anchor_x='center', anchor_y='center')
        else:
            self.speedLevelLabel = pyglet.text.Label(
                'Level: 3',
                font_name='Times New Roman',
                font_size=18,
                x=50, y=100,
                anchor_x='center', anchor_y='center')


def update_cars(speed):
    for car in Car.cars:
        car.update(speed)


def no_overlap(new_car, new_car_width):
    for car in Car.cars:
        if car.y + car.height > new_car.y:
            return False
    return True


class Car:
    cars = []

    def __init__(self, x):
        self.x = x
        self.y = WINDOW_HEIGHT
        self.sprite_x = self.x + enemy.offset_left
        self.sprite_y = self.y + enemy.offset_bottom
        self.height = enemy.height
        self.width = enemy.width
        self.sprite = pyglet.sprite.Sprite(img=enemy.img, x=self.x,
                                           y=self.y)
        self.color = (55, 55, 255)
        self.shape = shapes.Rectangle(x=self.sprite_x, y=self.sprite_y, width=self.width,
                                      height=self.height, color=self.color)

    def update(self, speed):
        self.y = self.y - speed
        self.sprite_y = self.sprite_y - speed
        updated_shape = shapes.Rectangle(x=self.sprite_x, y=self.sprite_y, width=self.width,
                                         height=self.height, color=self.color)
        self.shape = updated_shape
        self.sprite = pyglet.sprite.Sprite(img=enemy.img, x=self.x,
                                           y=self.y)
        if self.sprite_y < -self.height:
            Car.cars.remove(self)

    def draw(self):
        self.shape.draw()
        self.sprite.draw()

    def destroy(self):
        Car.cars.remove(self)


def draw_cars():
    for car in Car.cars:
        car.draw()


def create_car(delta_time):
    if random.randint(0, 10) == 0:
        x = random.randint(0, WINDOW_WIDTH - enemy.width-enemy.offset_left)
        new_car = Car(x)
        if no_overlap(new_car, new_car.width):
            Car.cars.append(Car(x))


def update_road(speed):
    for strip in Road.strips:
        strip.update(speed)


def create_road():
    for x in range(1, NUM_LANES):
        block_x = (WINDOW_WIDTH / NUM_LANES) * x
        for y in range(0, NUM_STRINGS_PER_LINE + 1):
            block_y = ((WINDOW_HEIGHT / NUM_STRINGS_PER_LINE) * y)
            Road.strips.append(Road(block_x, block_y))


class Road:
    strips = []

    def __init__(self, x, y):
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.width = 10
        self.height = WINDOW_HEIGHT / NUM_STRINGS_PER_LINE / 2
        self.shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                      height=self.height, color=self.color)

    def update(self, speed):
        self.y = self.y - speed
        updated_shape = shapes.Rectangle(x=self.x, y=self.y, width=self.width,
                                         height=self.height, color=self.color)
        self.shape = updated_shape

        if self.y < -self.height*2:
            self.y = WINDOW_HEIGHT

        self.draw()

    def draw(self):
        self.shape.draw()


class Player:

    def __init__(self, img):
        self.img = img
        self.width = img.width
        self.height = img.height
        self.startX = WINDOW_WIDTH / 2 - img.img.width/2
        self.startY = -img.offset_bottom
        self.spriteX = self.startX + img.offset_left
        self.sprite = pyglet.sprite.Sprite(img=player.img, x=self.startX, y=self.startY)
        self.color = (55, 55, 255)
        self.shape = shapes.Rectangle(x=self.spriteX, y=self.startY, width=self.width,
                                      height=self.height, color=self.color)
        self.lives = 3
        self.freeze = False
        self.label = pyglet.text.Label('Lives: ' + str(self.lives),
                                       font_name='Times New Roman',
                                       font_size=18,
                                       x=50, y=50,
                                       anchor_x='center', anchor_y='center')

    def draw(self):
        self.shape.draw()
        self.sprite.draw()

    def update_movement(self, delta_time):
        if sensor.has_capability('accelerometer'):
            acc_x = float(sensor.get_value('accelerometer')['x'])
            if acc_x < 0:
                if self.spriteX < WINDOW_WIDTH - self.width:
                    self.move(10)
            else:
                if self.spriteX > 0:
                    self.move(-10)

            if sensor.has_capability('button_1'):
                button_data = sensor.get_value('button_1')
                if int(button_data) == 1:
                    self.freeze = True
                elif int(button_data) == 0:
                    self.freeze = False

    def move(self, dt):
        if not self.freeze:
            self.startX = self.startX + dt
            self.spriteX = self.spriteX + dt
            self.shape = shapes.Rectangle(x=self.spriteX, y=self.startY, width=self.width,
                                          height=self.height, color=self.color)
            self.sprite = pyglet.sprite.Sprite(img=player.img, x=self.startX, y=self.startY)

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


# initialize new GameState
game = Game()


@window.event
def on_draw():
    window.clear()
    game.draw()


clock.schedule_interval(game.player.update_movement, 0.01)
clock.schedule_interval(create_car, 0.1)
clock.schedule_interval(game.check_collision, 0.1)
clock.schedule_interval(game.update_speed, 0.01)

pyglet.app.run()
