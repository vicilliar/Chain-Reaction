import pyglet
import constants
import shapes


class Game:
    def __init__(self, players, activePlayers, boardSize):
        self.players = players
        self.activePlayers = activePlayers
        self.alivePlayers = [i for i in activePlayers]

        self.playerTurn = 0
        self.round = 1
        self.ongoing = True
        self.board = Board(boardSize, self)

    def takeTurn(self, row, column):
        if self.board.checkFree(row, column, self.players[self.alivePlayers[self.playerTurn]].color):
            self.board.animNewOrb(row, column, self.players[self.alivePlayers[self.playerTurn]].color)
            self.board.addToTileCount(row, column, self.players[self.alivePlayers[self.playerTurn]].color)
            self.nextPlayer()

            # Eliminate players who lost all tiles
            while (not self.board.colorIsLeft(self.players[self.alivePlayers[self.playerTurn]].color)) and self.round > 1:
                print("Removing Player: " + self.players[self.alivePlayers[self.playerTurn]].name)
                self.alivePlayers.pop(self.playerTurn)
                if self.playerTurn == len(self.alivePlayers):
                    self.playerTurn = 0
            # End game if 1 player left
            if len(self.alivePlayers) == 1:
                self.ongoing = False
                self.savePlayerData()
                return True, True, self.players[self.alivePlayers[0]]
            return True, False, self.players[self.alivePlayers[self.playerTurn]]
        else:
            print("Invalid move! Tile occupied.")
            return False, -1

    def nextPlayer(self):
        self.playerTurn += 1
        if self.playerTurn == len(self.alivePlayers):
            self.round += 1
            print("New Round! Round #" + str(self.round))
            self.playerTurn = 0

    def getCurrPlayer(self):
        return self.players[self.alivePlayers[self.playerTurn]]

    def savePlayerData(self):
        # add wins and losses
        for i in range(len(self.activePlayers)):
            if self.activePlayers[i] == self.alivePlayers[0]:
                self.players[self.activePlayers[i]].wins += 1
            else:
                self.players[self.activePlayers[i]].losses += 1
        print("Wins and losses updated.")
        # write to file
        playerData = open("playerdata.txt", "w")
        for player in self.players:
            playerData.write(str(player.id) + "|" + player.name + "|" + player.color + "|" + str(player.wins)
                             + "|" + str(player.losses))
            if self.players.index(player) < len(self.players) - 1:
                playerData.write("\n")
        playerData.close()
        print("Data saved to file.")

class Player:
    def __init__(self, id, name, color, wins, losses):
        self.id = id
        self.name = name
        self.color = color
        self.wins = wins
        self.losses = losses


class Board:
    def __init__(self, boardSize, game):
        self.game = game
        self.boxSize = 80
        self.orbSize = 60
        self.boxPad = 5
        self.boardSize = boardSize
        self.gridBatch = pyglet.graphics.Batch()
        self.orbBatch = pyglet.graphics.Batch()
        self.transferring = 0

        # Drawing Background Rectangle
        bgVertices = (0, 0,
                      self.boxPad + (self.boardSize * (self.boxSize + self.boxPad)), 0,
                      self.boxPad + (self.boardSize * (self.boxSize + self.boxPad)),
                      self.boxPad + (self.boardSize * (self.boxSize + self.boxPad)),
                      0, self.boxPad + (self.boardSize * (self.boxSize + self.boxPad)))
        bgColors = constants.rgbColors[self.game.getCurrPlayer().color]
        self.bgRectangle = shapes.Rectangle(bgVertices, bgColors, self.gridBatch)

        # Drawing Tiles
        self.grid = []
        for i in range(boardSize):
            newRow = []
            for j in range(boardSize):
                if (i == 0 or i == boardSize-1) and (j == 0 or j == boardSize-1):
                    maxHold = 1
                elif (i == 0 or i == boardSize-1) and (0 < j < boardSize-1) or (0 < i < boardSize-1) and (j == 0 or j == boardSize-1):
                    maxHold = 2
                else:
                    maxHold = 3

                vertices = (
                    (i * (self.boxSize + self.boxPad)) + self.boxPad, (j * (self.boxSize + self.boxPad)) + self.boxPad,
                    (i * (self.boxSize + self.boxPad)) + self.boxPad + self.boxSize,
                    (j * (self.boxSize + self.boxPad)) + self.boxPad,
                    (i * (self.boxSize + self.boxPad)) + self.boxPad + self.boxSize,
                    (j * (self.boxSize + self.boxPad)) + self.boxPad + self.boxSize,
                    (i * (self.boxSize + self.boxPad)) + self.boxPad,
                    (j * (self.boxSize + self.boxPad)) + self.boxPad + self.boxSize)
                newRow.append(shapes.Tile(vertices, constants.rgbColors["white"], self.gridBatch, i, j, maxHold))
            self.grid.append(newRow)

    def checkFree(self, row, column, color):
        if self.grid[row][column].color == -1 or self.grid[row][column].color == color:
            return True
        return False

    def colorIsLeft(self, color):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.grid[i][j].color == color:
                    print("Elim check: " + color + " tile at " + str(i) + ", " + str(j))
                    return True
        return False

    def addToTileCount(self, row, column, color):
        # adding by just one (clicking)
        canHold = self.grid[row][column].addCount(color)
        self.grid[row][column].updateOrbs()
        if not canHold:
            self.popTile(row, column, color)
            self.animPopTile(row, column)

    def addByPop(self, row, column, color):
        # adding by popping
        canHold = self.grid[row][column].addCount(color)
        if not canHold:
            self.grid[row][column].schedPopAnim = True
            self.popTile(row, column, color)
            print("Pop animation scheduled at " + str(row) + ", " + str(column) + ".")

    def popTile(self, row, column, color):
        # empty popped tile
        self.grid[row][column].emptyCount()
        print("Popping: " + str(row) + ", " + str(column) + "! Now holds: " + str(self.grid[row][column].holding))
        # addToTile above, below, left, right, if possible
        # Weird direction convention, but it works
        if row-1 >= 0:
            self.addByPop(row-1, column, color)
        if row+1 < self.boardSize:
            self.addByPop(row+1, column, color)
        if column-1 >= 0:
            self.addByPop(row, column-1, color)
        if column+1 < self.boardSize:
            self.addByPop(row, column+1, color)

    def animNewOrb(self, row, column, color):
        self.grid[row][column].addOrb(color, self.orbSize, self.orbBatch)

    def animPopTile(self, row, column):
        # remove pop animation schedule
        self.grid[row][column].schedPopAnim = False
        print("Starting pop animation at " + str(row) + ", " + str(column) + ".")
        # addToTile above, below, left, right, if possible
        # Weird direction convention, but it works
        if row - 1 >= 0:
            self.transferOrb(self.grid[row][column], self.grid[row - 1][column], "left")
        if row + 1 < self.boardSize:
            self.transferOrb(self.grid[row][column], self.grid[row + 1][column], "right")
        if column - 1 >= 0:
            self.transferOrb(self.grid[row][column], self.grid[row][column - 1], "down")
        if column + 1 < self.boardSize:
            self.transferOrb(self.grid[row][column], self.grid[row][column + 1], "up")

    def transferOrb(self, giver, receiver, direction):
        orb = giver.orbs[0]
        if direction == "up":
            orb.ydir = direction
            orb.xdir = -1
            orb.dx = 0
            orb.dy = 200
        elif direction == "down":
            orb.ydir = direction
            orb.xdir = -1
            orb.dx = 0
            orb.dy = -200
        elif direction == "left":
            orb.ydir = -1
            orb.xdir = direction
            orb.dx = -200
            orb.dy = 0
        elif direction == "right":
            orb.ydir = -1
            orb.xdir = direction
            orb.dx = 200
            orb.dy = 0

        orb.leftBound = receiver.leftBound
        orb.rightBound = receiver.rightBound - orb.size
        orb.lowerBound = receiver.lowerBound
        orb.upperBound = receiver.upperBound - orb.size

        if not orb.transfer:
            self.transferring += 1
            orb.transfer = True

        receiver.orbs.append(giver.orbs.pop(0))

    def update(self, dt):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                for orb in self.grid[i][j].orbs:
                    gotThere = orb.move(dt)
                    if gotThere:
                        print("Orb just arrived at " + str(i) + ", " + str(j) + ". Contains " + str(len(self.grid[i][j].orbs)) + ".")
                        self.transferring -= 1
                        self.grid[i][j].updateOrbs()
                        # only pop once scheduled, AND all orbs are appended to lists
                        if len(self.grid[i][j].orbs) > self.grid[i][j].maxHold:
                            self.animPopTile(i, j)

