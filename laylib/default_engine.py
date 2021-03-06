"""
Basic short documentation

The DefaultEngine class is intended to be used as a base class
for your main engine game class, for fast prototyping your engine
and let you focus on the game logic itself. The DefaultEngine contain:

-----------------------------------
A - PUBLIC ATTRIBUTES TO USE:
-----------------------------------

self.running: to control when exit the main loop and the environment.
------------
self.playing: to exit only the main loop and keep tracking event.
------------
self.screen: contain the main screen
------------
self.dt:     the delta time float to control your game latency
------------
self.clock:  to tick FPS and keep tracking time
------------
self.all_sprites: if your game contain Sprites class, use this attribute
------------      to store all your sprites.

self.img, self.snd, self.fnt:
-----------------------------
these variables contain the whole resources data your game need.


-------------------------------
B - PUBLIC METHODS TO OVERRIDE:
-------------------------------

1) - def event_listener():
your game engine class MUST contain this function name
override this function on your engine class
if you need to manage events in your program.

2) - def update():
override this function in your main engine class to update your whole game.

3)- def draw():
override this function in your main engine class to draw the whole graphics.


----------------------------
C - PRIVATE METHODS:
----------------------------

1) - def main_loop():
Is the global loop to manage event, update and draw all stuffs.
this function is called on the main function.

2) - load_game(self, dataFolder, persistenceLayer):
this function is called automatically and
will load all the resources found in the data folder of resources.

3) - load_levels(self, dataFolder, fileLevels):
this function if your game contain file levels or file,
best score or any save.

4)- destroy_game(self):
called by default to destroy all resources.

(see examples folder for some usage example).

"""


import pygame as pg
from laylib.resources import Resources


class DefaultEngine:
    """
    Use it as a base class for your game engine.
    """

    def __init__(self):
        self.running = True
        self.playing = False
        self.screen = pg.display.get_surface()
        self.dt = 0.0
        self.clock = pg.time.Clock()
        self.img = self.snd = self.fnt = None
        self.all_sprites = None

    def main_loop(self):
        while self.running:
            t = pg.time.get_ticks()
            self.event_listener()
            self.update()
            self.draw()
            self.dt = (pg.time.get_ticks() - t) / 1000.0

    def event_listener(self):
        """
        Manage the window quit events
        QUIT / ESCAPE : to exit the program.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.running = False

    def load_game(self, dataFolder, persistenceLayer):
        """ load resources:
        this  function fetch  and  load whatever resources we need.
        - The "dataFolder"  WILL CONTAIN the persistenceLayer file.
        - The environment.py call this method on the main file, if
        a dataFolder  and  a  persistenceLayer are specified on the
        demo.load_complete() function. (see main file examples).
        """
        self.res = Resources(dataFolder)
        data = self.res.get(persistenceLayer)
        self.img = self.res.img.loadGroup(data['imgList'], True)
        self.snd = self.res.snd.loadGroup(data['sndList'])
        self.fnt = self.res.fnt.loadGroup(data['fntList'])
        self.msc = self.res.msc.get_playList(data['mscList'])
        self.res.show()

    def load_levels(self, dataFolder, fileLevels):
        """
        If the prototype contain levels use this function.
        Overload this function.
        """
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def destroy_game(self):
        if self.all_sprites:
            self.all_sprites.empty()
        if self.img:
            del self.img
        if self.snd:
            del self.snd
        if self.fnt:
            del self.fnt
