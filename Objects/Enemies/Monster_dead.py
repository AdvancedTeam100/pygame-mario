import pygame
import random

import Drop_SunaDokei
import Drop_Takarabako
from Main import PyMain

# モンスター「Ghost」「Lich」を倒した場合の処理をまとめたクラス。倒すとアイテムをドロップする。
class Monster_dead(pygame.sprite.Sprite):
    # モンスター消失クラス
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = 100

    def update(self):
        self.count -= 1
        if self.count == 80:
            self.image = Monster_dead.honou_anime[1]
        elif self.count == 60:
            self.image = Monster_dead.honou_anime[0]
        elif self.count == 40:
            self.image = Monster_dead.honou_anime[1]
        elif self.count == 20:
            self.image = Monster_dead.honou_anime[0]
            self.kill()
            self.x = random.randint(0,1)
            if self.x == 0:
                Drop_SunaDokei((self.rect.topleft))
            elif self.x == 1:
                Drop_Takarabako((self.rect.topleft))

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
