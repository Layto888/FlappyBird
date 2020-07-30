import math
import pygame as pg
from pygame.math import Vector2 as vect2d


"""
util Desc file: n° (0.2):
lib for rapid prototyping games,
contain some useful functions like dstance between two vectors.
TODO:
            - unittest module.
            - optimization
            - add description of how to parse data and creat persistence layer

Date:       12/07/2017
Author:     Amardjia Amine (Goutted)
"""


def dist(v1: vect2d, v2: vect2d) -> float:
    """ distance between two vectors. """
    d = ((v2.x - v1.x)**2 + (v2.y - v1.y)**2) ** 0.5
    return d


def rad2deg(rad: float) -> float:
    """ from radian to degree """
    return rad * 180.0 / math.pi()


def deg2rad(deg: float) -> float:
    """ from degree to radian """
    return deg * 3.14 / 180.0


def rotate(v: vect2d, angle: float) -> vect2d:
    """ rotates a point p around the point origin."""
    vector = ((v.x * math.cos(angle) - v.y * math.sin(angle)),
              (v.x * math.sin(angle) + v.x * math.cos(angle)))
    return vector


def rotate2p(v1: vect2d, v2: vect2d, angle: float) -> vect2d:
    """
    this function rotates a point p1
    around the point p0 with a certain angle."""
    dx = v2.x - v1.x
    dy = v2.y - v1.y
    vector = vect2d((dx * math.cos(angle) - dy * math.sin(angle)),
                    (dx * math.sin(angle) + dx * math.cos(angle)))
    vector += v1

    return vector


# graphics stuffs : to test

def rotateDeg(image, angle):
    """ rotate an image while keeping its center and size"""
    angle %= 360.0
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    orig_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(orig_rect).copy()
    return rot_image


def xIntersect(body1: pg.Rect, body2: pg.Rect) -> bool:
    """ x Intersection between two Rects: """
    return (body1.x + body1.w) < (body2.x + body2.w) * 0.5 or \
        (body1.x + body1.w) >= (body2.x + body2.w) * 0.5


def yIntersect(body1: pg.Rect, body2: pg.Rect) -> bool:
    """ y Intersection between two Rects: """
    return (body1.y + body1.h) < (body2.y + body2.h) or \
        (body1.y + body1.h) >= (body2.y + body2.h)
