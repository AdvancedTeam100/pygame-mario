import pygame

import Map
import Monster_dead
from Main import PyMain

# モンスター「Ghost」x軸方向に移動し、ブロックに衝突すると移動方向を反転させる。主人公の魔法「FireBall」で倒す事が出来る。
class Ghost(pygame.sprite.Sprite):

    def __init__(self, pos, shoki_muki, speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = speed
        self.ghost_muki = shoki_muki
    
    def update(self):
        self.rect.move_ip(self.speed, 0) 
        
        for self.block in Map.blocks:
            self.collide = self.rect.colliderect(self.block.rect)
            if self.collide:
                if self.ghost_muki == 0:
                    self.image = self.left_image
                    self.ghost_muki = 1
                elif self.ghost_muki == 1:
                    self.image = self.right_image
                    self.ghost_muki = 0
                self.speed = self.speed * -1

        # 魔法「FireBall」に衝突すると自身を削除し、Monster_deadオブジェクトを生成する。
        for self.fireball in Map.fireball:
            self.collide = self.rect.colliderect(self.fireball.rect)
            if self.collide:
                self.kill()
                Monster_dead((self.rect.topleft))

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
