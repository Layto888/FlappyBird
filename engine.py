import pygame as pg
from pygame.math import Vector2 as vect2d
from laylib import DefaultEngine
from random import randint
from settings import *


class FlappyBird(DefaultEngine):
    # main engine example

    def __init__(self):
        super().__init__()
        self.all_sprites = pg.sprite.Group()
        self.pipe = []
        self.ground = []
        self.bird = None
        self.score = 0

    def new_demo(self):
        """ remove old sprites if necessary """
        if self.all_sprites:
            self.all_sprites.empty()
        self.score = 0
        # create two pipes: 2 x (top+bottom)
        self.pipe.append(self.new_pipes(950))
        self.pipe.append(self.new_pipes(1400))
        self.bird = Bird(self.img[0:3], self.snd[FX_WING])
        for i in range(2):
            self.ground.append(Ground(self.img[GROUND_IMG], GRND_POS[i]))
        # set the sprites
        self.all_sprites.add(Background(self.img[BACKGRND_IMG]))
        self.all_sprites.add(self.pipe)
        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.bird)
        # play music
        pg.mixer.music.play()
        self.playing = True

    def new_pipes(self, pos_x):
        pipe = []
        pipe.append(Pipe(self.img[PIPE_DOWN_IMG]))
        pipe.append(Pipe(self.img[PIPE_UP_IMG]))
        self.reset_pipe(pipe, pos_x)
        return pipe

    def draw(self):
        self.all_sprites.draw(self.screen)
        self.res.fnt.render(self.fnt[SKETCH], str(self.score), FONT_POS)
        pg.display.flip()

    def update(self):
        if not self.playing and self.running:
            self.new_demo()
        # recycle the pipes
        if self.pipe[0][DOWN].x < 0:
            self.reset_pipe(self.pipe[0], PIPE_X)
        if self.pipe[1][DOWN].x < 0:
            self.reset_pipe(self.pipe[1], PIPE_X)
        # see if the bird hurt any pipe
        if self.collide(self.bird, self.pipe[0]):
            self.game_over()
        # when the bird hit the ground
        if self.collide(self.bird, self.ground):
            self.bird.vel = vect2d(0.0, 0.0)
            self.bird.acc = vect2d(0.0, 0.0)
            self.game_over()
        self.check_score(self.bird, self.pipe)
        self.all_sprites.update(self.dt)

    def game_over(self):
        pg.mixer.music.stop()
        if self.bird.alive:
            self.snd[FX_HIT].play()
            self.bird.alive = False
        # stop the scrolling
        for i in range(2):
            self.ground[i].vel = vect2d(0.0, 0.0)
            self.pipe[i][0].vel = vect2d(0.0, 0.0)
            self.pipe[i][1].vel = vect2d(0.0, 0.0)

    def check_score(self, bird, pipe):
        for i in range(2):
            if bird.rect.left >= pipe[i][0].rect.left \
                    and bird.rect.right <= pipe[i][0].rect.right:
                if bird.alive and pipe[i][0].new_pipe:
                    self.score += 1
                    self.snd[FX_WIN].play()
                    pipe[i][0].new_pipe = False

    @staticmethod
    def reset_pipe(pipe, pos_x):
        pipe[0].pos = vect2d(pos_x, randint(*PIPE_POS))
        pipe[1].pos = vect2d(pos_x, pipe[0].y + PIPES_DIST)
        pipe[0].new_pipe = True
        pipe[1].new_pipe = True

    @staticmethod
    def collide(body1, body2, k1=False, k2=False):
        """ test groupe sprites collision"""
        return pg.sprite.spritecollide(body1, body2, k1, k2)


class BasicBody(pg.sprite.Sprite):
    def __init__(self, image, pos=(0.0, 0.0)):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = vect2d(pos)
        self.rect.center = vect2d(pos)


class Background(BasicBody):
    def __init__(self, image, pos=vect2d(BKGRND_POS)):
        super().__init__(image, pos)


class Ground(BasicBody):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.vel = vect2d(GRND_VEL, 0.0)

    def update(self, dt):
        if self.pos.x < 0:
            self.pos.x = GRND_START_POS
        self.pos.x -= self.vel.x * dt
        self.rect.center = self.pos


class Pipe(BasicBody):
    def __init__(self, image, pos=(0.0, 0.0)):
        super().__init__(image, pos)
        self.vel = vect2d(PIPE_VEL, 0.0)
        self.new_pipe = False

    def update(self, dt):
        self.pos.x -= self.vel.x * dt
        self.rect.center = self.pos

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @x.setter
    def x(self, value):
        self.rect.x = value

    @y.setter
    def y(self, value):
        self.rect.y = value


class Bird(pg.sprite.Sprite):
    def __init__(self, image, fx):
        super().__init__()
        self.frame = 0
        self.image_group = image
        self.image = image[0]
        self.pos = vect2d(WIDTH / 2.0, HEIGHT / 2.0)
        self.rect = self.image.get_rect()
        self.rect.center = vect2d(self.pos)
        self.vel = vect2d(0.0, 0.0)
        self.acc = vect2d(0.0, BIRD_GRAVITY)
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 120
        self.alive = True
        self.wing = fx

    def update(self, dt):
        # fly and fall
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        # anim sprites
        if self.alive:
            self.image = self.image_group[self.frame]
            now = pg.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                self.frame %= 3
                if self.frame == 2:
                    self.wing.play()
            # keys
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                self.fly()

    def fly(self):
        self.vel.y = FLY_VEL
