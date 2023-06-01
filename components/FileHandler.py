import pygame as pg
from components.Rectangle import Rectangle


class FileHandler(Rectangle):

    def __init__(self, pos_x, pos_y, width, height):
        super().__init__(pos_x, pos_y, width, height)
        self.file_path = None

    def check_is_image_file(self, path):
        if path is not None and path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.file_path = path
        else:
            return False

    def handle_drop(self, event):
        if event.type == pg.DROPFILE:
            file_path = event.file
            return file_path


