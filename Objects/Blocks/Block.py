
import pygame
from Main import PyMain


#--------------------------------------------------
#通常ブロック。主人公が作ったり、消したり出来るブロック。
class Block(pygame.sprite.Sprite):
    # 通常ブロック
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
