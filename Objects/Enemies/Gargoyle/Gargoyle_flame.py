import pygame
from Main import PyMain

# ガーゴイルの吐く炎。ブロックに衝突すると消える。
class Gargoyle_flame(pygame.sprite.Sprite):
    def __init__(self, pos, blocks, muki):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.blocks = blocks
        self.gargoyle_muki = muki
        if self.gargoyle_muki == 0:
            self.image = Gargoyle_flame.right_image
            self.speed = 5
        elif self.gargoyle_muki == 1:
            self.image = Gargoyle_flame.left_image
            self.speed = -5

    def update(self):
        self.rect.move_ip(self.speed, 0)
        for block in self.blocks:
            collide = self.rect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                self.kill()

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
