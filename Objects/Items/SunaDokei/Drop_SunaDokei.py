import pygame
from pygame.locals import *

import Map
from Main import PyMain

# モンスタードロップの砂時計。制限時間(ライフ)を増やすアイテム。
class Drop_SunaDokei(pygame.sprite.Sprite):
    # 砂時計
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.GRAVITY = 0.2
        self.on_floor = False
        self.fpvy = 0

    def collision_y(self):
        """Y方向の衝突判定処理"""
        # 砂時計のサイズ取得
        self.width = self.rect.width
        self.height = self.rect.height

        # Y方向の移動先の座標と矩形を求める
        self.newy = self.rect.y + self.fpvy
        if self.fpvy > 0:
            self.newrect = Rect(self.rect.x, self.newy, self.width, self.height)
        elif self.fpvy == 0:
            self.newrect = Rect(self.rect.x, self.newy + 1, self.width, self.height)

        # ブロックとの衝突判定
        for self.block in Map.blocks:
            self.collide = self.newrect.colliderect(self.block.rect)
            if self.collide:  # 衝突するブロックあり
                if int(self.block.rect.centery/50) == int(self.rect.centery/50) + 1:
                    if self.fpvy > 0:    # 下に移動中に衝突
                        # めり込まないように調整して速度を0に
                        self.rect.y = self.block.rect.top - self.height
                        self.fpvy = 0
                        # 下に移動中に衝突したなら床の上にいる
                        self.on_floor = True
                        break
                    elif self.fpvy == 0:
                        # めり込まないように調整して速度を0に
                        self.rect.y = self.block.rect.top - self.height
                        # 下に移動中に衝突したなら床の上にいる
                        self.on_floor = True
                        break

                    break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.rect.y = self.newy
                # 衝突ブロックがないなら床の上にいない
                self.on_floor = False

    def update(self):

        self.collision_y()

        # もし自身が床上にいなかったら。落下中、1フレーム毎にy軸方向の速度(落下速度)に重力加速度を加える。
        if self.on_floor == False:
            self.fpvy += self.GRAVITY

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
