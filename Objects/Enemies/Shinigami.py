import pygame
from pygame.locals import *
import time
import math
import threading

import Map
import Hero
import Light_circle
from Main import PyMain

# 主人公の後を絶えず追尾してくるちょっぴり嫌なモンスター。倒すことは出来ないが魔法「lightcircle」により一時的に遠ざける事が出来る。
"""
collide_switch この変数に1が入る場合、向きの通常代入。通常移動が起こらない。
"""
class Shinigami(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = speed
        self.sayu = 0
        self.collide = False
        self.collide_switch = 0
        self.waku_collide = 0
    
    # 主人公の魔法「light_circle」に死神が接触した場合に呼び出されるメソッド。
    # light_circleに接触した死神は「外枠ブロック」に当たるまで-self.sokudox,-self.sokudoyの速度で接触したlight_circleから遠ざかるように移動する。
    def escape(self):
        self.collide_switch = 1
        if self.sokudox >= 0:
            self.image = Shinigami.left_image
        elif self.sokudox <= 0:
            self.image = Shinigami.right_image
        while self.waku_collide == 0:
            time.sleep(0.02)
            self.rect.move_ip(-self.sokudox,-self.sokudoy)
            for self.block in Map.blocksw:
                self.collide2 = self.rect.colliderect(self.block.rect)
                if self.collide2:
                    self.waku_collide = 1
        self.collide_switch = 0
        self.waku_collide = 0

    def update(self):

        Map.all.move_to_front(self)
        self.shinigami_sax = int(Hero.posx) - self.rect.x
        self.shinigami_say = int(Hero.posy) - self.rect.y

        self.angle = math.atan2(self.shinigami_say,self.shinigami_sax)
        self.sokudox = self.speed * math.cos(self.angle)
        self.sokudoy = self.speed * math.sin(self.angle)

        if self.collide_switch == 0:
            if self.sokudox >= 0:
                self.image = Shinigami.right_image
            elif self.sokudox < 0:
                self.image = Shinigami.left_image

        self.sokudo = (self.sokudox,self.sokudoy)

        self.width = self.rect.width
        self.height = self.rect.height

        # 移動先のrect値を求めている。
        self.newrect = Rect(self.rect.x + self.sokudox, self.rect.y + self.sokudoy, self.width, self.height)        
        for self.light_circle in Map.light_circle:
            # 移動先のrect値とlight_circleに衝突があるか無いか。
            self.collide = self.newrect.colliderect(self.light_circle.rect)
        
        # light_circleがマップ上にない場合は無衝突状態にする。
        if Light_circle.switch == False:
            self.collide = False

        # 衝突があった場合、escape関数を呼び出す。
        if self.collide == True:
            th7 = threading.Thread(target=self.escape)
            th7.start()

        # light_circleとの衝突が無い場合。
        if self.collide == False:
            # escape中でない場合。
            if self.collide_switch == 0:
                self.rect.move_ip(self.sokudo)

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
