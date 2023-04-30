import random
from ImageWithBoundingBox import ImageWithBoundingBox
from Player import Player
from EnemyCar import EnemyCar
from RoadString import RoadString
from DIPPID import SensorUDP
import pyglet
from pyglet import clock
from Config import WINDOW_WIDTH, WINDOW_HEIGHT, NUM_LANES, \
    NUM_STRINGS_PER_LANE, RAISE_SPEED_TIME

PORT = 5700
sensor = SensorUDP(PORT)

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# load images and adjust bounding boxes
# Images taken from https://opengameart.org/content/free-top-down-car-sprites-by-unlucky-studio

playerImage = pyglet.image.load('assets/Audi.png')
playerImageWithBoundingBox = ImageWithBoundingBox(playerImage, 80, 80, 10, 27)

enemyImage = pyglet.image.load('assets/taxi.png')
enemyImageWithBoundingBox = ImageWithBoundingBox(enemyImage, 80, 80, 20, 10)


# Game class that handles updates and creation of all components
class Game:

    def __init__(self):

        self.player = Player(playerImageWithBoundingBox)
        self.enemyCars = []
        self.strips = []
        self.score = 0
        self.isGameOver = False
        self.currentSpeed = 2
        self.levelTimer = 0

        # Create Road once when game is initialized
        self.create_road()

    def draw(self):
        if self.player.lives == 0:
            self.isGameOver = True
            self.drawGameOverScreen()
            self.checkForRestart()
        else:
            self.update_road(self.currentSpeed)
            self.draw_cars()
            self.player.draw()
            self.drawLabels()

    def drawGameOverScreen(self):
        pyglet.text.Label('Game Over',
                          font_name='Times New Roman',
                          font_size=36,
                          x=WINDOW_WIDTH / 2,
                          y=WINDOW_HEIGHT / 2,
                          anchor_x='center',
                          anchor_y='center').draw()
        pyglet.text.Label(
            'final Score: ' + str(self.score),
            font_name='Times New Roman',
            font_size=18,
            x=WINDOW_WIDTH / 2,
            y=WINDOW_HEIGHT / 2 - 50,
            anchor_x='center',
            anchor_y='center').draw()
        pyglet.text.Label('Press button_2 to reset the game',
                          font_name='Times New Roman',
                          font_size=18,
                          x=WINDOW_WIDTH / 2,
                          y=WINDOW_HEIGHT / 2 - 100,
                          anchor_x='center',
                          anchor_y='center').draw()

    # Reset Game if button_2 clicked in gameOver screen
    def checkForRestart(self):
        if sensor.has_capability('button_2'):
            button_data = sensor.get_value('button_2')
            if int(button_data) == 1:
                self.reset()

    def update(self, delta_time):
        # update cars
        self.update_cars(self.currentSpeed)

        # update global speed level
        if self.levelTimer == RAISE_SPEED_TIME:
            self.update_speed()
        else:
            self.levelTimer += 1

        # update player movement
        if sensor.has_capability('accelerometer') and sensor.has_capability(
                'button_1'):
            acc_x = float(sensor.get_value('accelerometer')['x'])
            button_1 = sensor.get_value('button_1')
            self.player.update_movement(acc_x, button_1)

        self.check_collision()

        if not self.isGameOver:
            self.score += 1

    def update_speed(self):
        if self.currentSpeed == 2:
            self.currentSpeed = 4
        elif self.currentSpeed == 4:
            self.currentSpeed = 8
        self.levelTimer = 0

    # Check if Player and EnemyCars collide
    def check_collision(self):
        for car in self.enemyCars:
            if car.sprite_y <= self.player.height:
                x1_player = self.player.spriteX
                x2_player = self.player.spriteX + self.player.width
                x1_enemy = car.sprite_x
                x2_enemy = car.sprite_x + car.width
                if (x1_player <= x2_enemy) and (x2_player >= x1_enemy):
                    self.enemyCars.remove(car)
                    self.player.checkLives()

    def reset(self):
        self.currentSpeed = 2
        self.levelTimer = 0
        self.score = 0
        self.isGameOver = False
        self.enemyCars = []
        self.player.reset()

    # display current Level and Score
    def drawLabels(self):
        level = '1' if self.currentSpeed == 2 else '2' if self.currentSpeed == 4 else '3'
        self.player.label.draw()
        pyglet.text.Label(
            'Level: ' + str(level),
            font_name='Times New Roman',
            font_size=18,
            x=10, y=100,
            anchor_x='left', anchor_y='center').draw()
        pyglet.text.Label(
            'Score: ' + str(self.score),
            font_name='Times New Roman',
            font_size=18,
            x=10, y=150,
            anchor_x='left', anchor_y='center').draw()

    def update_cars(self, speed):
        for car in self.enemyCars:
            car.update(speed)
            if car.sprite_y < -car.height:
                self.enemyCars.remove(car)

    # only create a car if it doesnt overlap with existing
    def no_overlap(self, new_car):
        for car in self.enemyCars:
            if car.y + car.height > new_car.y:
                return False
        return True

    def draw_cars(self):
        for car in self.enemyCars:
            car.draw()

    # Create car in random position
    def create_car(self, delta_time):
        if random.randint(0, 10) == 0:
            x = random.randint(0, WINDOW_WIDTH - enemyImageWithBoundingBox.width - enemyImageWithBoundingBox.offset_left)
            new_car = EnemyCar(x, enemyImageWithBoundingBox)
            if self.no_overlap(new_car):
                self.enemyCars.append(EnemyCar(x, enemyImageWithBoundingBox))

    def update_road(self, speed):
        for strip in self.strips:
            strip.update(speed)

    # Create initial road layout
    def create_road(self):
        for x in range(1, NUM_LANES):
            string_x = (WINDOW_WIDTH / NUM_LANES) * x
            for y in range(0, NUM_STRINGS_PER_LANE + 1):
                string_y = ((WINDOW_HEIGHT / NUM_STRINGS_PER_LANE) * y)
                self.strips.append(RoadString(string_x, string_y))


# initialize new Game
game = Game()


@window.event
def on_draw():
    window.clear()
    game.draw()


clock.schedule_interval(game.update, 0.01)
clock.schedule_interval(game.create_car, 0.1)

pyglet.app.run()
