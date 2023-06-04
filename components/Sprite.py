import pygame as pg


# Object class
class Sprite(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path, scaling=1):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.scaling = scaling
        self.image_path = image_path
        self.render()

    def draw(self, screen):
        self._rect.topleft = (self.pos_x, self.pos_y)
        screen.blit(self.image, self._rect)

    def scale_image(self, scale):
        self.height = self.default_image.get_rect().height
        self.width = self.default_image.get_rect().width

        self.image = pg.transform.scale(self.default_image, (self.width * scale, self.height * scale))

    def render(self):
        self.default_image = pg.image.load(self.image_path).convert_alpha()
        self.width = self.default_image.get_rect().width
        self.height = self.default_image.get_rect().height
        self.image = pg.transform.scale(self.default_image, (self.width * self.scaling, self.height * self.scaling))
        self._rect = self.image.get_rect()