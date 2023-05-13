import pygame as pg
from components.Rectangle import Rectangle


class Text(Rectangle):

    def __init__(self, pos_x, pos_y, content, font, text_color, padding_x=0, padding_y=0, background_color="transparent", border_radius=0):
        self.__background_color = background_color

        # Render Text
        self.text = font.render(content, True, text_color)

        # Deal with Text Positioning
        self.__text_rect = self.text.get_rect()
        self.__text_rect.topleft = (pos_x+padding_x//2, pos_y+padding_y//2)

        # Deal with Rectangle Positioning
        text_width, text_height = font.size(content)
        super().__init__(pos_x, pos_y, text_width+padding_x, text_height+padding_y, self.__background_color, border_radius=border_radius)

    def draw(self, screen):
        # Check whether or not to draw Rectangle Background
        if self.__background_color != "transparent":
            super().draw(screen)
        screen.blit(self.text, self.__text_rect)
