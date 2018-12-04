import pyglet
import constants
import engine
from pyglet.window import mouse


class Button:
    def __init__(self, pic, x, y, width, height, opacity, batch):
        self.pic = pic
        self.sprite = pyglet.sprite.Sprite(pic, x, y, batch=batch)
        self.sprite.opacity = opacity

        self.leftBound = x
        self.rightBound = x + width
        self.lowerBound = y
        self.upperBound = y + height

    def highlight(self):
        self.sprite.opacity = 255

    def unhighlight(self):
        self.sprite.opacity = 100


class StartWindow(pyglet.window.Window):
    def __init__(self):
        self.owidth = 805
        self.oheight = 600
        self.buttonPad = 5
        self.xPad = 20
        self.yPad = 20
        self.botBatch = pyglet.graphics.Batch()
        self.midBatch = pyglet.graphics.Batch()
        self.topBatch = pyglet.graphics.Batch()
        super().__init__(width=self.owidth, height=self.oheight)

        self.players = []
        self.numPlayers = 2
        self.boardSize = 5
        self.readPlayerData()
        self.activePlayers = [0, 1]

        pic = constants.bg
        self.bgSprite = pyglet.sprite.Sprite(pic, 0, 0, batch=self.botBatch)

        pic = constants.title
        self.titleSprite = pyglet.sprite.Sprite(pic, 200, 520, batch=self.topBatch)
        pic = constants.devnames
        self.devSprite = pyglet.sprite.Sprite(pic, 190, 510, batch=self.topBatch)

        pic = constants.selectgamesize
        self.selectgamesizeSprite = pyglet.sprite.Sprite(pic, 80, 420, batch=self.topBatch)
        pic = constants.chooseplayer
        self.chooseplayerSprite = pyglet.sprite.Sprite(pic, 320, 420, batch=self.topBatch)
        pic = constants.winrecord
        self.winrecordSprite = pyglet.sprite.Sprite(pic, 550, 100, batch=self.midBatch)

        pic = constants.startbutton
        self.startButton = Button(pic, self.xPad, self.yPad, pic.texture.width, pic.texture.height, 255, self.topBatch)
        pic = constants.exitbutton
        self.exitButton = Button(pic, self.owidth - (self.xPad + pic.texture.width), self.yPad, pic.texture.width, pic.texture.height, 255, self.topBatch)

        self.numButtons = []
        for i in range(5):
            pic = constants.numOptionPics[4 - i]
            if pic == constants.numOptionPics[0]:
                opacity = 255
            else:
                opacity = 100
            self.numButtons.append(Button(pic, self.xPad + 65, 140 + self.yPad + ((pic.texture.height + self.buttonPad) * i),
                                          pic.texture.width, pic.texture.height, opacity, self.topBatch))

        self.playerButtons = []
        self.winLabels = []
        self.lossLabels = []
        for i in range(len(self.players)):
            pic = constants.playerPics[self.players[i].id]
            if pic == constants.playerPics[0] or pic == constants.playerPics[1]:
                opacity = 255
            else:
                opacity = 100
            self.playerButtons.append(Button(pic, self.xPad + 300, 88 + self.yPad + ((pic.texture.height + self.buttonPad) * (5-i)),
                                          pic.texture.width, pic.texture.height, opacity, self.topBatch))
            self.winLabels.append(pyglet.text.Label(str(self.players[i].wins), font_name='Arial', font_size=27,
                                                    bold=True, batch=self.topBatch,
                                                    x = self.xPad + 547,
                                                    y = 95 + self.yPad + ((pic.texture.height + self.buttonPad) * (5-i))))
            self.lossLabels.append(pyglet.text.Label(str(self.players[i].losses), font_name='Arial', font_size=27,
                                                     bold=True, batch=self.topBatch,
                                                     x=self.xPad + 627,
                                                     y=95 + self.yPad + ((pic.texture.height + self.buttonPad) * (5 - i))))

    def on_draw(self):
        self.clear()
        self.botBatch.draw()
        self.midBatch.draw()
        self.topBatch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.checkNumButtons(x, y)
            self.checkPlayerButtons(x, y)
            self.highlightPlayerButtons()
            self.checkMiscButtons(x, y)

    def readPlayerData(self):
        playerFile = open("playerdata.txt", "r")
        for line in playerFile:
            playerData = line.split("|")
            self.players.append(engine.Player(int(playerData[0]), playerData[1], playerData[2], int(playerData[3]), int(playerData[4])))
        playerFile.close()

    def checkNumButtons(self, x, y):
        # check num buttons
        for button in self.numButtons:
            if button.leftBound <= x <= button.rightBound and button.lowerBound <= y <= button.upperBound:
                self.numPlayers = 6 - self.numButtons.index(button)
                print(str(self.numPlayers) + " player game selected!")

                if self.numPlayers < 5:
                    self.boardSize = 5
                else:
                    self.boardSize = 6

                # highlight selected num button
                for allButt in self.numButtons:
                    if allButt == button:
                        allButt.highlight()
                    else:
                        allButt.unhighlight()

    def checkPlayerButtons(self, x, y):
        # check player buttons
        for button in self.playerButtons:
            if button.leftBound <= x <= button.rightBound and button.lowerBound <= y <= button.upperBound:
                playerInd = self.playerButtons.index(button)

                # add selected player to list
                if playerInd not in self.activePlayers:
                    self.activePlayers.append(playerInd)
                    print(self.players[playerInd].name + " selected!")

    def checkMiscButtons(self, x, y):
        # check start button
        button = self.startButton
        if button.leftBound <= x <= button.rightBound and button.lowerBound <= y <= button.upperBound:
            # start a new game
            game = engine.Game(self.players, self.activePlayers, self.boardSize)
            mainWindow = GameWindow(game)
            pyglet.clock.schedule_interval(mainWindow.update, 1 / 60)
            self.close()
        # check exit button
        button = self.exitButton
        if button.leftBound <= x <= button.rightBound and button.lowerBound <= y <= button.upperBound:
            pyglet.app.exit()

    def highlightPlayerButtons(self):
        # remove players if extra
        while len(self.activePlayers) > self.numPlayers:
            self.activePlayers.pop(0)
        i = 0
        # add more players if missing
        while len(self.activePlayers) < self.numPlayers:
            if i not in self.activePlayers:
                self.activePlayers.append(i)
            i += 1
        # highlight appropriate buttons
        for i in range(len(self.playerButtons)):
            if i in self.activePlayers:
                self.playerButtons[i].highlight()
            else:
                self.playerButtons[i].unhighlight()


class GameWindow(pyglet.window.Window):
    def __init__(self, game):
        self.game = game
        self.owidth = (self.game.board.boxPad * (self.game.board.boardSize + 1)) + \
                      (self.game.board.boxSize * self.game.board.boardSize)
        self.oheight = (self.game.board.boxPad * (self.game.board.boardSize + 1)) + \
                      (self.game.board.boxSize * self.game.board.boardSize)
        self.botBatch = pyglet.graphics.Batch()
        self.midBatch = pyglet.graphics.Batch()
        self.topBatch = pyglet.graphics.Batch()
        super().__init__(width=self.owidth, height=self.oheight + 120)

        pic = constants.bg
        self.bgSprite = pyglet.sprite.Sprite(pic, 0, self.oheight, batch=self.botBatch)

        pic = constants.title
        self.titleSprite = pyglet.sprite.Sprite(pic, (self.owidth / 2) - (pic.texture.width/2), self.oheight + 50, batch=self.midBatch)
        pic = constants.devnames
        self.devSprite = pyglet.sprite.Sprite(pic, (self.owidth / 2) - (pic.texture.width/2), self.oheight + 40, batch=self.midBatch)

        pic = constants.playerPics[self.game.getCurrPlayer().id]
        self.currSprite = pyglet.sprite.Sprite(pic, 0, self.oheight, batch=self.midBatch)

        self.buttons = []
        pic = constants.quitbutton
        self.quitButton = Button(pic, self.owidth - (pic.texture.width), self.oheight, pic.texture.width,
                                 pic.texture.height, 255, self.midBatch)
        self.buttons.append(self.quitButton)

        self.gameOverSprite = -1
        self.winSprite = -1
        self.plusSprite = -1

    def on_draw(self):
        self.clear()
        self.botBatch.draw()
        self.game.board.gridBatch.draw()
        self.game.board.orbBatch.draw()
        self.midBatch.draw()
        self.topBatch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.game.ongoing and self.game.board.transferring == 0:
                self.checkGrid(x, y)
            self.checkButtons(x, y)

    def checkGrid(self, x, y):
        for row in self.game.board.grid:
            for rec in row:
                if rec.leftBound <= x <= rec.rightBound and rec.lowerBound <= y <= rec.upperBound:
                    turnResult = self.game.takeTurn(rec.row, rec.column)
                    if turnResult[0]:
                        # turn successfully made
                        if turnResult[1]:
                            # game is over
                            print("Game Over! Winner: " + turnResult[2].name)
                            self.gameOverSprite = pyglet.sprite.Sprite(constants.gameover,
                                                                       self.owidth / 65,
                                                                       self.oheight / 4, batch=self.midBatch)
                            self.gameOverSprite.opacity = 200
                            self.gameOverSprite.scale = self.owidth / 2000

                            pic = constants.pluswin
                            self.plusSprite = pyglet.sprite.Sprite(pic,
                                                                   self.owidth / 65,
                                                                   self.oheight / 4, batch=self.topBatch)
                            self.plusSprite.scale = self.owidth / 300

                            pic = constants.playerPics[self.game.getCurrPlayer().id]
                            self.winSprite = pyglet.sprite.Sprite(pic,
                                                                  self.owidth / 3,
                                                                  self.oheight / 4.5, batch=self.topBatch)
                            self.winSprite.scale = self.owidth / 500

                            self.quitButton.sprite.image = constants.menu
                        else:
                            self.currSprite.image = constants.playerPics[turnResult[2].id]
                            self.game.board.bgRectangle.changeColor(turnResult[2].color)

    def checkButtons(self, x, y):
        for button in self.buttons:
            if button.leftBound <= x <= button.rightBound and button.lowerBound <= y <= button.upperBound:
                # go back to main menu
                self.preWindow = StartWindow()
                self.close()

    def update(self, dt):
        self.game.board.update(dt)