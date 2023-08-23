import pygame

from Main import PyMain

# 砂時計。制限時間(ライフ)を増やすアイテム。
class SunaDokei(pygame.sprite.Sprite):
    # 砂時計
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
