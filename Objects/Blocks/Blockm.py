
import pygame
from Main import PyMain

#モノクロブロック。通常ブロックとは異なり、作ったり消すことは出来ない。
class Blockm(pygame.sprite.Sprite):
    # モノクロブロック
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
