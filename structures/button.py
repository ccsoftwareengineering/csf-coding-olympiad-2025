import pygame

from structures.game import Game


class Button:
    # Press Events
    on_press_start = False
    on_press_end = False
    pressing = False

    # Hover Events
    on_hover_start = False
    on_hover_end = False
    hovering = False

    def __init__(self, game: Game, pos: (int, int), image: pygame.Surface, scale=1):
        self.game = game
        self.image = pygame.transform.scale_by(image, scale)
        self.darker_image = self.image.copy()
        mask = pygame.mask.from_surface(self.image).to_surface(setcolor=(0, 0, 0), unsetcolor=(255, 255, 255))
        mask.set_colorkey((255, 255, 255))
        mask.set_alpha(int(255 * 0.15))
        self.darker_image.blit(mask, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0], pos[1])

    def draw(self):
        pos = pygame.mouse.get_pos()
        to_draw = self.image

        if self.rect.collidepoint(pos):
            self.on_hover_start = not self.hovering
            self.hovering = True

            if pygame.mouse.get_pressed()[0]:
                self.on_press_start = not self.pressing
                self.pressing = True
            else:
                self.on_press_end = self.pressing
                self.pressing = False
                to_draw = self.darker_image
        else:
            self.on_hover_end = self.hovering
            self.hovering = False

        self.game.screen.blit(to_draw, (self.rect.x, self.rect.y))
