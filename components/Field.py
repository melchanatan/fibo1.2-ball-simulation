import pygame as pg
from components.RigidBody import RigidBody


class Field:
    def __init__(self, pos_x=0, pos_y=0, sizeofwall=0, backfromfront=0, target=0, scaleing=1, background=None,
                 floor=None, canon=None, basket=None, wall=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.scaleing = scaleing
        self.sizeofwall = sizeofwall
        self.backfromfront = backfromfront
        self.target = target
        self.background = background
        self.floor = floor
        self.canon = canon
        self.basket = basket
        self.wall = wall

    def draw(self, screen):
        # อัตราส่วนคือ 960/315
        self.floor = RigidBody(self.pos_x, self.pos_y + (385 * self.scaleing),
                               "graphics/floor.jpg", self.scaleing)
        self.canon = RigidBody(self.pos_x + (151 * self.scaleing - ((self.backfromfront * 960 / 315) * self.scaleing)),
                               self.pos_y + (242 * self.scaleing),
                               "graphics/our_canon.jpg", self.scaleing)
        self.basket = RigidBody(self.pos_x + (853 * self.scaleing), self.pos_y + (278 * self.scaleing),
                                "graphics/basket.jpg", self.scaleing)
        if self.sizeofwall == 100:
            self.wall = RigidBody(self.pos_x + (548.5 * self.scaleing - (8.5 * self.scaleing)),
                                  self.pos_y + (80 * self.scaleing),
                                  "graphics/wall100cm.jpg", self.scaleing)
        if self.sizeofwall == 50:
            self.wall = RigidBody(self.pos_x + (548.5 * self.scaleing - (8.5 * self.scaleing)),
                                  self.pos_y + (232 * self.scaleing),
                                  "graphics/wall50cm.jpg", self.scaleing)

        self.floor.draw(screen)
        self.canon.draw(screen)
        self.wall.draw(screen)
        self.basket.draw(screen)
        pg.draw.rect(screen, (233, 205, 208), (
        self.pos_x + ((853 + ((self.target-6.5) * 960 / 315)) * self.scaleing), self.pos_y + (278 * self.scaleing),
        40 * self.scaleing, 6 * self.scaleing))
