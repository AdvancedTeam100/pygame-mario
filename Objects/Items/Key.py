import pygame

from Main import PyMain

# 1面に必ず一つ落ちているアイテム。このアイテムを取得しないとドアに接触してもclearにはならない。
class Key(pygame.sprite.Sprite):
    # 鍵
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
