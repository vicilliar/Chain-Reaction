import pyglet
import constants
import random


class Orb:
    def __init__(self, x, y, leftBound, rightBound, lowerBound, upperBound, size, color, batch):
        self.size = size
        self.leftBound = leftBound
        self.rightBound = rightBound - self.size
        self.lowerBound = lowerBound
        self.upperBound = upperBound - self.size

        self.color = color
        self.pic = constants.colorPics[color]
        self.sprite = pyglet.sprite.Sprite(self.pic, x-(self.size/2), y-(self.size/2), batch=batch)
        self.sprite.scale = 0.1
        self.sprite.opacity = 215

        self.transfer = False
        self.xdir = "right"
        self.ydir = "up"
        self.dx = 0
        self.dy = 0

    def move(self, dt):
        self.sprite.x += self.dx * dt
        self.sprite.y += self.dy * dt
        return self.checkCollision()

    def checkCollision(self):
        gotThere = False
        if self.xdir == "right" and self.sprite.x >= self.rightBound:
            self.dx *= -1
            self.xdir = "left"
            if self.transfer:
                gotThere = True
            self.transfer = False
        if self.xdir == "left" and self.sprite.x <= self.leftBound:
            self.dx *= -1
            self.xdir = "right"
            if self.transfer:
                gotThere = True
            self.transfer = False
        if self.ydir == "up" and self.sprite.y >= self.upperBound:
            self.dy *= -1
            self.ydir = "down"
            if self.transfer:
                gotThere = True
            self.transfer = False
        if self.ydir == "down" and self.sprite.y <= self.lowerBound:
            self.dy *= -1
            self.ydir = "up"
            if self.transfer:
                gotThere = True
            self.transfer = False
        return gotThere

    def updateSpeed(self, speed):
        if not self.transfer:
            if self.dx < 0:
                self.dx = (-1 * speed) + random.randint(-20, 20)
                self.xdir = "left"
            if self.dx >= 0:
                self.dx = speed + random.randint(-20, 20)
                self.xdir = "right"
            if self.dy < 0:
                self.dy = -1 * speed + random.randint(-20, 20)
                self.ydir = "down"
            if self.dy >= 0:
                self.dy = speed + random.randint(-20, 20)
                self.ydir = "up"


class Rectangle:
    def __init__(self, vertices, colors, batch):
        self.vertices = vertices
        self.leftBound = vertices[0]
        self.rightBound = vertices[2]
        self.lowerBound = vertices[1]
        self.upperBound = vertices[5]

        self.colors = colors
        self.batch = batch
        self.rect = batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', vertices), ('c4B', colors))

    def changeColor(self, color):
        self.rect.colors = constants.rgbColors[color]


class Tile(Rectangle):
    def __init__(self, vertices, colors, batch, row, column, maxHold):
        super().__init__(vertices, colors, batch)
        self.row = row
        self.column = column
        self.orbs = []
        self.schedPopAnim = False

        self.color = -1
        self.lastColor = -1
        self.holding = 0
        self.maxHold = maxHold

    def updateOrbs(self):
        diff = self.maxHold - self.holding
        if diff == 2:
            orbSpeed = 20
        elif diff == 1:
            orbSpeed = 45
        elif diff == 0:
            orbSpeed = 140
        else:
            orbSpeed = 0
        for orb in self.orbs:
            orb.updateSpeed(orbSpeed)
            if self.color == -1:
                orb.color = self.lastColor
            else:
                orb.color = self.color
            orb.sprite.image = constants.colorPics[orb.color]

    def addOrb(self, color, size, batch):
        self.orbs.append(Orb((self.rightBound + self.leftBound)/2 - 6, (self.upperBound + self.lowerBound)/2 - 6,
                             self.leftBound, self.rightBound, self.lowerBound, self.upperBound, size, color, batch))

    def addCount(self, color):
        self.color = color
        self.holding += 1

        print("Add to: " + str(self.row) + ", " + str(self.column) + ". Now holds: " + str(self.holding) + ". Color: " + self.color)
        # if False, the tile pops
        if self.holding > self.maxHold:
            return False
        return True

    def emptyCount(self):
        self.lastColor = self.color
        self.color = -1
        self.holding = 0