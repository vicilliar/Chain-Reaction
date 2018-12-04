import pyglet


scale = 0.35
bg = pyglet.image.load('assets/background.png')
bg.texture.width *= scale
bg.texture.height *= scale

scale = 0.50
title = pyglet.image.load('assets/title.png')
title.texture.width = title.texture.width * scale
title.texture.height = title.texture.height * scale

scale = 0.45
devnames = pyglet.image.load('assets/devnames.png')
devnames.texture.width *= scale
devnames.texture.height *= scale

scale = 0.35
selectgamesize = pyglet.image.load('assets/selectgamesize.png')
selectgamesize.texture.width *= scale
selectgamesize.texture.height *= scale

scale = 0.35
chooseplayer = pyglet.image.load('assets/chooseplayer.png')
chooseplayer.texture.width *= scale
chooseplayer.texture.height *= scale

scale = 0.35
winrecord = pyglet.image.load('assets/winrecord.png')
winrecord.texture.width *= scale
winrecord.texture.height *= scale

scale = 0.3
startbutton = pyglet.image.load('assets/startbutton.png')
startbutton.texture.width = startbutton.texture.width * scale
startbutton.texture.height = startbutton.texture.height * scale

scale = 0.3
exitbutton = pyglet.image.load('assets/exitbutton.png')
exitbutton.texture.width = exitbutton.texture.width * scale
exitbutton.texture.height = exitbutton.texture.height * scale

scale = 0.22
quitbutton = pyglet.image.load('assets/quitbutton.png')
quitbutton.texture.width = quitbutton.texture.width * scale
quitbutton.texture.height = quitbutton.texture.height * scale

scale = 0.22
menu = pyglet.image.load('assets/menu.png')
menu.texture.width *= scale
menu.texture.height *= scale

scale = 0.35
pluswin = pyglet.image.load('assets/pluswin.png')
pluswin.texture.width *= scale
pluswin.texture.height *= scale

gameover = pyglet.image.load('assets/gameover.png')

numOptionPics = [pyglet.image.load('assets/2p.png'), pyglet.image.load('assets/3p.png'),
                 pyglet.image.load('assets/4p.png'), pyglet.image.load('assets/5p.png'),
                 pyglet.image.load('assets/6p.png')]
scale = 0.22
for pic in numOptionPics:
    pic.texture.width = pic.width * scale
    pic.texture.height = pic.height * scale

playerPics = [pyglet.image.load('assets/playerred.png'), pyglet.image.load('assets/playerorange.png'),
              pyglet.image.load('assets/playeryellow.png'), pyglet.image.load('assets/playergreen.png'),
              pyglet.image.load('assets/playerblue.png'), pyglet.image.load('assets/playerpurple.png')]
scale = 0.33
for pic in playerPics:
    pic.texture.width = pic.width * scale
    pic.texture.height = pic.height * scale

colorPics = {
    "red": pyglet.image.load('assets/red.png'),
    "orange": pyglet.image.load('assets/orange.png'),
    "yellow": pyglet.image.load('assets/yellow.png'),
    "green": pyglet.image.load('assets/green.png'),
    "blue": pyglet.image.load('assets/blue.png'),
    "purple": pyglet.image.load('assets/purple.png')
}

rgbColors = {
    "red": (234, 24, 19, 255,
            234, 24, 19, 255,
            234, 24, 19, 255,
            234, 24, 19, 255),
    "orange": (244, 110, 0, 255,
               244, 110, 0, 255,
               244, 110, 0, 255,
               244, 110, 0, 255),
    "yellow": (255, 215, 10, 255,
               255, 215, 10, 255,
               255, 215, 10, 255,
               255, 215, 10, 255),
    "green": (19, 204, 79, 255,
              19, 204, 79, 255,
              19, 204, 79, 255,
              19, 204, 79, 255),
    "blue": (19, 57, 204, 255,
             19, 57, 204, 255,
             19, 57, 204, 255,
             19, 57, 204, 255),
    "purple": (184, 15, 208, 255,
               184, 15, 208, 255,
               184, 15, 208, 255,
               184, 15, 208, 255),
    "white": (255, 255, 255, 0,
              255, 255, 255, 0,
              255, 255, 255, 0,
              255, 255, 255, 0),
    "black": (0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0)
}