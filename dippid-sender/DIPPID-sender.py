import socket
import time
import random
import numpy as np

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

buttonClicked = True
timeSinceLastButtonEvent = time.time()

# segment sinewave into 100 samples
num_samples = 1000
sinetime = np.arange(0, 1, 1/num_samples)

# Create 3 different Sinewaves
sinewave1 = np.sin(2 * np.pi * 1 * sinetime)
sinewave2 = np.sin(2 * np.pi * 1.3 * sinetime)
sinewave3 = np.sin(2 * np.pi * 1.6 * sinetime)

sincount = 0

while True:
    buttonTime = random.uniform(0.1, 3.0)
    buttonMessage = ''
    accMessage = {}

    # if random time has passed switch the button value and update global timer
    if time.time() > buttonTime + timeSinceLastButtonEvent:
        if buttonClicked:
            buttonMessage = '{"button_1" : ' + str(0) + '}'
            buttonClicked = False
            timeSinceLastButtonEvent = time.time()
        else:
            buttonMessage = '{"button_1" : ' + str(1) + '}'
            buttonClicked = True
            timeSinceLastButtonEvent = time.time()

    accMessage = '{"accelerometer": ' + '{"x": ' + str(sinewave1[sincount]) + ', "y": ' + str(sinewave2[sincount]) + ',"z": ' + str(sinewave3[sincount]) + '}}'

    # print(accMessage)

    sock.sendto(buttonMessage.encode(), (IP, PORT))
    sock.sendto(accMessage.encode(), (IP, PORT))

    # reset sinewave if num of samples reached
    if sincount < num_samples-1:
        sincount += 1
    else:
        sincount = 0

    time.sleep(0.01)

