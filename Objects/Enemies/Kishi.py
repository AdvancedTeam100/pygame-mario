import pygame
from pygame.locals import *

import Map
from Main import PyMain

"""
Ghost同様、横方向にまっすぐ進み、ブロックと衝突するとその移動方向を反転させるモンスター
その際、衝突したブロックが「通常ブロック」の場合、そのブロックを破壊される。Hero同様(主人公同様)、「重力」が働いており、床がない箇所では落下する。
self.anime_interval_count  →  フレームカウント用変数
"""
class Kishi(pygame.sprite.Sprite):
    # 騎士
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = 3
        self.sayu = 0
        self.anime_interval_count = 0
        self.subscript = 0
        self.GRAVITY = 0.2
        self.on_floor = False
        self.fpvy = 0
        self.collide = False

    def collision_y(self):
        """Y方向の衝突判定処理"""
        # 騎士のサイズ
        self.width = self.rect.width
        self.height = self.rect.height

        # Y方向の移動先の座標と矩形を求める
        self.newy = self.rect.y + self.fpvy
        if self.fpvy > 0:
            self.newrect = Rect(self.rect.x, self.newy, self.width, self.height)
            print("a")
        elif self.fpvy == 0:
            self.newrect = Rect(self.rect.x, self.newy + 1, self.width, self.height)
            print("b")

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

        print(self.collide)
        print(self.fpvy)

        Map.all.move_to_front(self)        
        self.collision_y()

        # もし自身が床上にいなかったら。落下中、1フレーム毎にy軸方向の速度(落下速度)に重力加速度を加える。
        if self.on_floor == False:
            self.fpvy += self.GRAVITY

        # 移動、及び、歩行アニメ
        if self.on_floor == True:
            self.rect.move_ip(self.speed, 0) 
            if self.anime_interval_count >= 10:
                if self.sayu == 1:
                    if self.subscript == 2:
                        self.subscript = 3
                        self.image = Kishi.hokou[self.subscript]
                        self.anime_interval_count = 0
                    elif self.subscript == 3:
                        self.subscript = 2
                        self.image = Kishi.hokou[self.subscript]
                        self.anime_interval_count = 0
                elif self.sayu == 0:
                    if self.subscript == 0:
                        self.subscript = 1
                        self.image = Kishi.hokou[self.subscript]
                        self.anime_interval_count = 0
                    elif self.subscript == 1:
                        self.subscript = 0
                        self.image = Kishi.hokou[self.subscript]
                        self.anime_interval_count = 0
            self.anime_interval_count += 1

            # ブロックとの衝突判定 衝突したブロックが「通常ブロック」であった場合、そのブロックは破壊される。
            for self.block in Map.blocks:
                self.collide2 = self.rect.colliderect(self.block.rect)
                if self.collide2:  # 衝突するブロックあり
                    if Map.men[int(self.block.rect.y/50)][int(self.block.rect.x/50)] == 3:
                        Map.men[int(self.block.rect.y/50)][int(self.block.rect.x/50)] = 0
                        Map.load()
                    if self.sayu == 0:
                        self.sayu = 1
                        self.subscript = 2
                        self.anime_interval_count = 0
                        self.image = Kishi.hokou[self.subscript]
                    elif self.sayu == 1:
                        self.sayu = 0
                        self.subscript = 0
                        self.anime_interval_count = 0
                        self.image = Kishi.hokou[self.subscript]
                    self.speed = self.speed * -1

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
