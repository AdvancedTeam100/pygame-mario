import pygame
from pygame.locals import *
import random
import Hero
import math

import Map
import Lich_fireball
import Monster_dead 
from Main import PyMain

"""
マップ内をランダムでワープ移動するモンスター
「主人公に向け」ブロックをすり抜ける魔法弾を放ってくる。倒すことは出来ない。
shot_interval_time  →  モンスター「リッチ」が魔法弾を放つ時間間隔。
warp_interval_time  →  モンスター「リッチ」がワープ移動する時間間隔。
shot_speed  →  モンスター「リッチ」が放つ魔法弾の速さ。
lichsax  →  主人公とリッチの位置の差(X軸方向の差)を格納する。
lichsay  →  主人公とリッチの位置の差(Y軸方向の差)を格納する。
"""
class Lich(pygame.sprite.Sprite):
    # リッチ
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.shot_interval_time = 200
        self.shot_speed = 5
        self.warp_interval_time = 300

    def update(self):
        Map.all.move_to_front(self)
        # 一定時間間隔でワープする。出現場所はランダム。ただし、主人公と衝突が起こる座標にはワープしない。
        self.warp_interval_time -= 1
        if self.warp_interval_time <= 0:
            
            # 出現位置はランダム。
            self.rect.x = random.randint(50,850)
            self.rect.y = random.randint(50,600)
            self.warp_interval_time = 300

            # もし主人公と同座標にワープしようとしたら、ワープ位置を修正する。 (画面を四分割した場合) 主人公のいる位置の対角に現れる。
            self.HeroRect = Rect(Hero.posx, Hero.posy, 40, 40)
            collide3 = self.rect.colliderect(self.HeroRect)
            if collide3:
                if Hero.posx <= 400 and Hero.posy <= 300:
                    self.rect.x = 600
                    self.rect.y = 450
                elif Hero.posx <= 400 and Hero.posy > 301:
                    self.rect.x = 600
                    self.rect.y = 150
                elif Hero.posx > 401 and Hero.posy <= 300:
                    self.rect.x = 200
                    self.rect.y = 450
                elif Hero.posx > 401 and Hero.posy > 301:
                    self.rect.x = 200
                    self.rect.y = 150

        # 一定時間間隔で主人公のいる座標に向けてmonster魔法「Lich_fireball」を放ってくる。
        self.shot_interval_time -= 1
        if self.shot_interval_time  <= 0:
            self.lichsax = int(Hero.center_pos_x) - self.rect.x
            self.lichsay = int(Hero.center_pos_y) - self.rect.y

            self.angle = math.atan2(self.lichsay,self.lichsax)
            self.sokudox = self.shot_speed * math.cos(self.angle)
            self.sokudoy = self.shot_speed * math.sin(self.angle)

            self.fire_sokudo = (self.sokudox,self.sokudoy)
            Lich_fireball(self.rect.topleft,self.fire_sokudo)
            self.shot_interval_time = 200

        # 魔法「FireBall」に衝突すると自身を削除し、Monster_deadオブジェクトを生成する。
        for self.fireball in Map.fireball:
            self.collide = self.rect.colliderect(self.fireball.rect)
            if self.collide:
                self.kill()
                Monster_dead((self.rect.topleft))

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
