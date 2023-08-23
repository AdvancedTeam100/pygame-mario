import pygame
import Map
from Main import PyMain

# リッチの放つ魔法弾。通常ブロック、モノクロブロックは通り抜ける。枠ブロックに衝突する消える。
class Lich_fireball(pygame.sprite.Sprite):
    # リッチ_ファイヤーボール
    def __init__(self, pos, fire_sokudo):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.fire_sokudo = fire_sokudo

    def update(self):
        Map.all.move_to_front(self)
        self.rect.move_ip(self.fire_sokudo)
        for self.block in Map.blocksw:
            collide = self.rect.colliderect(self.block.rect)
            if collide:  # 衝突するブロックあり
                self.kill()

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
