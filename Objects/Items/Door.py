import pygame

from Main import PyMain

# 面をクリアする手順:アイテム「key」を取得した後、扉(Door)へと到達すると面クリアとなる。
class Door(pygame.sprite.Sprite):
    # ドア
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    
    def update(self):
        # 鍵を取得するとドアが開く。
        if PyMain.key_flag == 1:
            self.image = Door.open_image

        # statusにより、自身を削除する。
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
