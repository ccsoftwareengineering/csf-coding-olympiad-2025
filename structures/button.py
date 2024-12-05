import pygame


class Button():
    def __init__(self, x, y, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        pygame.draw.rect(self.image, (255, 255, 255), self.rect)