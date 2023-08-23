import pygame
import Map
import Gargoyle_flame
from Main import PyMain


#--------------------------------------------------
"""
火を弾を定期的に吐くモンスター。倒せない仕様。
shot_interval_time  →  火弾を吐く時間間隔
gargoyle_muki  →  ガーゴイルの向き
"""
class Gargoyle(pygame.sprite.Sprite):
    # ガーゴイル
    def __init__(self, pos, muki):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.shot_interval_time = 0
        self.gargoyle_muki = muki
        if self.gargoyle_muki == 0:
            self.image = Gargoyle.right_image
        elif self.gargoyle_muki == 1:
            self.image = Gargoyle.left_image

    def update(self):
        self.shot_interval_time += 1
        if self.shot_interval_time  >= 200:
            Gargoyle_flame((self.rect.topleft), Map.blocks, self.gargoyle_muki)
            self.shot_interval_time = 0

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
