import pygame as pg
from components.Rectangle import Rectangle


class Text(Rectangle):

    def __init__(self, pos_x, pos_y, content, font, text_color, padding_x=0, padding_y=0, background_color="transparent", border_radius=0):
        self.__background_color = background_color
        self.font = font
        self.content = content
        self.text_color = text_color
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.border_radius = border_radius

        # Render Text
        self.text = font.render(content, True, text_color)
        self.render()

    def render(self):
        # Deal with Text Positioning
        self.__text_rect = self.text.get_rect()
        self.__text_rect.topleft = (self.pos_x + self.padding_x // 2, self.pos_y + self.padding_y // 2)

        # Deal with Rectangle Positioning
        self.text_width, text_height = self.font.size(self.content)
        super().__init__(self.pos_x, self.pos_y, self.text_width + self.padding_x, text_height + self.padding_y, self.__background_color,
                         border_radius=self.border_radius)

    def set_content(self, new_content):
        self.content = new_content
        self.text = self.font.render(self.content, True, self.text_color)

    def draw(self, screen):
        # Check whether or not to draw Rectangle Background
        if self.__background_color != "transparent":
            super().draw(screen)
        screen.blit(self.text, self.__text_rect)
