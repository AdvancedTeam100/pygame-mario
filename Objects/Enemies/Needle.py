import pygame

from Main import PyMain

# 触れると死亡してしまう痛い針。スプライトグループはMap.monstersのグループに属している。(モンスター扱いになっている)
class Needle(pygame.sprite.Sprite):
    # 針
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
