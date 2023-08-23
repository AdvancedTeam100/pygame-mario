import pygame
from Main import PyMain

# 枠ブロック 外枠のブロック。死神がLight_circleに触れescapeする場合、この枠ブロックに接触するまで逃げる。
# また、Lichの魔法弾は通常ブロックとモノクロブロックは通り抜け、この枠ブロックと衝突するまで消えない。
class Waku_Block(pygame.sprite.Sprite):
    # 外枠のブロック
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
