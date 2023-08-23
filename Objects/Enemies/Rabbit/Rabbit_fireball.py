import pygame
import Map
from Main import PyMain

# ボスモンスター「Rabbit」の使う魔法 通常ブロックと衝突すると双方消える。
"""
ブロックオブジェクトを一つずつ取り出し、Rabbit_fireballとの衝突を調べる。
もし衝突があった場合は自身(Rabbit_fireball)を消去し、もし衝突相手のブロックが通常ブロックであった場合は
その衝突した通常ブロックを消去する。
"""   
class Rabbit_fireball(pygame.sprite.Sprite):
    # ボスの魔法
    def __init__(self, pos, sokudo, blocks):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.fire_sokudo = sokudo
        self.blocks = blocks
 
    def update(self):
        self.rect.move_ip(self.fire_sokudo) 
        for self.block in self.blocks:
            collide = self.rect.colliderect(self.block.rect)
            if collide:  # 衝突するブロックあり
                self.kill()
                if Map.men[int(self.block.rect.centery/50)][int(self.block.rect.centerx/50)] == 3:
                    Map.men[int(self.block.rect.centery/50)][int(self.block.rect.centerx/50)] = 0
                    self.block.kill()
                    Map.load()

        # statusが面間状態にある場合、自身を削除する。
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
