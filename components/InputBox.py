import pygame as pg

class TextInputBox(pg.sprite.Sprite):
    def __init__(self, x, y, w, font, color=(0, 0, 0)):
        super().__init__()
        self.color = color
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""

        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pg.Surface((max(self.width, t_surf.get_width()+50), t_surf.get_height()+4), pg.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (25, 3))
        pg.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 3, border_radius=30)
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self, event_list):
        for event in event_list:
            if self.active and event.type == pg.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(pg.mouse.get_pos())
            if event.type == pg.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()

    def draw(self, screen):
        screen.blit(self.image, self.rect)