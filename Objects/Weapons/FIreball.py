import pygame

import Map
from Main import PyMain
# FireBallクラス
# モンスター「Ghost」を倒すことが出来る。
class FireBall(pygame.sprite.Sprite):
    def __init__(self, pos, muki):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos   # 中心座標をposに
        self.muki = muki # プレーヤーの向き判定
        self.speed = 7           # ミサイルの移動速度
        self.anime_count = 10
        self.switch = 0
        self.first_fireball_anime = 0
        
    def update(self):

        # FireBallのアニメーション処理。
        if self.first_fireball_anime == 0:
            if self.muki == 0:
                self.image = FireBall.right_image
            elif self.muki == 1:
                self.image = FireBall.left_image
            self.first_fireball_anime = 1

        self.anime_count = self.anime_count - 1
        if self.anime_count == 0:       
            if self.muki == 0:
                if self.switch == 0:
                    self.image = FireBall.right_image
                    self.anime_count = 10
                    self.switch = 1
                elif self.switch == 1:
                    self.image = FireBall.right_image2
                    self.anime_count = 10
                    self.switch = 0
                
            elif self.muki == 1:
                if self.switch == 0:
                    self.image = FireBall.left_image
                    self.anime_count = 10
                    self.switch = 1
                elif self.switch == 1:
                    self.image = FireBall.left_image2
                    self.anime_count = 10
                    self.switch = 0

        if self.muki == 0:
            self.rect.move_ip(self.speed, 0)
        elif self.muki == 1:
            self.rect.move_ip(-self.speed, 0)


        # ブロックとミサイルの衝突判定。Fireballはブロックと衝突すると消滅する。
        for block in Map.blocks:
            collide = self.rect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                self.kill()

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
