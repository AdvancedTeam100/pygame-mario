
import pygame
import time
import math
import threading

import Map
import Hero
import Rabbit_fireball
from Main import PyMain

# ボスモンスター「Rabbit」クラス
"""
ボスモンスター「Rabbit」の攻撃について
一定の間隔(時間)で主人公に向かって魔法火弾を放ってくる。

ボスモンスター「Rabbit」の倒し方について
主人公の魔法「ファイヤーボール」を5回当てる事で倒すことが出来る。

Rabbitは主人公のその位置により二通りの(X)位置を取ります。(左位置・右位置とする)
左位置はX100 右位置はX500である。
「主人公のX位置 >= RabbitのX位置」となった場合、Rabbitは右を向き、左位置に移動し
「主人公のX位置 < RabbitのX位置」となった場合は、Rabbitは左を向き、右位置に移動します。
"""
class Rabbit(pygame.sprite.Sprite):

    def __init__(self, pos, fire_ball):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.fire_balls = fire_ball

        self.muki = 0
        self.speed = 5
        self.rabbit_hp = 5
        self.rabbit_fireball_interval_time = 300

    # ボスモンスター「Rabbit」にダメージを与えた際の処理をまとめた関数。
    # 主人公の魔法「ファイヤーボール」が当たると、設定したhpが1減少する。減少した時点でのHPが0になる場合、「ゲームクリア」となる。
    def rabbit_damage_dead_process(self):
        self.rabbit_hp -= 1
        if self.rabbit_hp > 0:
            if self.muki == 0:
                self.image = Rabbit.damage_left_image
                time.sleep(0.5)
                self.image = Rabbit.left_image
            elif self.muki == 1:
                self.image = Rabbit.damage_right_image
                time.sleep(0.5)
                self.image = Rabbit.right_image

        elif self.rabbit_hp == 0:
            if self.muki == 0:
                self.image = Rabbit.damage_left_image
                time.sleep(0.5)
                self.image = Rabbit.left_image
            elif self.muki == 1:
                self.image = Rabbit.damage_right_image
                time.sleep(0.5)
                self.image = Rabbit.right_image
            self.kill()
            PyMain.men_clear = 1
            PyMain.status = 5

    # 衝突判定関数。衝突がある場合Trueを返し、無い場合Falseを返す。
    def collision(self, top1, bottom1, left1, right1, top2, bottom2, left2, right2):
        if left1 < right2 and top1 < bottom2 and right1 > left2 and bottom1 > top2:
            return True
        else:
            return False
        

    def update(self):
        # 主人公の現在位置により、自らの位置を変える。(左位置rect.x == 100 と右位置rect.x == 500 の二通り)
        if Hero.center_pos_x >= self.rect.centerx:
            self.image = Rabbit.right_image
            self.muki = 1
            if self.rect.x >= 100: 
                self.rect.move_ip(-5,0)
                
        elif Hero.center_pos_x < self.rect.centerx:
            self.image = Rabbit.left_image
            self.muki = 0
            if self.rect.x <= 500: 
                self.rect.move_ip(5,0)

        self.rabbit_fireball_interval_time -= 1

        #ループで書き直す
        if self.rabbit_fireball_interval_time <= 0:
            # 左向きの場合
            if self.muki == 0:
                # 主人公のいる方向に飛んでくる魔法弾の速度を求めている。
                # 工程1：主人公の位置と魔法弾の位置との差を求めている。
                self.boss_fireball_sax = int(Hero.center_pos_x) - (self.rect.x - 100)
                self.boss_fireball_say = int(Hero.center_pos_y) - (self.rect.y + 200)

                self.boss_fireball_sax2 = int(Hero.center_pos_x) - (self.rect.x -100)
                self.boss_fireball_say2 = int(Hero.center_pos_y) - (self.rect.y +300)

                self.boss_fireball_sax3 = int(Hero.center_pos_x) - (self.rect.x -100)
                self.boss_fireball_say3 = int(Hero.center_pos_y) - (self.rect.y +400)
                
                # 定めた魔法弾の速さからx方向の速度とy方向の速度を個別に求めている。
                self.angle = math.atan2(self.boss_fireball_say,self.boss_fireball_sax)
                self.sokudox = self.speed * math.cos(self.angle)
                self.sokudoy = self.speed * math.sin(self.angle)

                self.angle2 = math.atan2(self.boss_fireball_say2,self.boss_fireball_sax2)
                self.sokudox2 = self.speed * math.cos(self.angle2)
                self.sokudoy2 = self.speed * math.sin(self.angle2)

                self.angle3 = math.atan2(self.boss_fireball_say3,self.boss_fireball_sax3)
                self.sokudox3 = self.speed * math.cos(self.angle3)
                self.sokudoy3 = self.speed * math.sin(self.angle3)
                
                # 求めたx方向の速度とy方向の速度をまとめている。
                self.fire_sokudo = (self.sokudox,self.sokudoy)
                self.fire_sokudo2 = (self.sokudox2,self.sokudoy2)
                self.fire_sokudo3 = (self.sokudox3,self.sokudoy3)
                
                # ボスモンスター「ラビット」の放つ魔法弾を実体化している。
                Rabbit_fireball((self.rect.x -100, self.rect.y + 200),self.fire_sokudo,Map.blocks)
                Rabbit_fireball((self.rect.x -100, self.rect.y + 300),self.fire_sokudo2,Map.blocks)
                Rabbit_fireball((self.rect.x -100, self.rect.y + 400),self.fire_sokudo3,Map.blocks)
                self.rabbit_fireball_interval_time = 300

            # 右向きの場合
            elif self.muki == 1:
                self.boss_fireball_sax = int(Hero.center_pos_x) - (self.rect.x + 300)
                self.boss_fireball_say = int(Hero.center_pos_y) - (self.rect.y + 200)

                self.boss_fireball_sax2 = int(Hero.center_pos_x) - (self.rect.x +300)
                self.boss_fireball_say2 = int(Hero.center_pos_y) - (self.rect.y +300)

                self.boss_fireball_sax3 = int(Hero.center_pos_x) - (self.rect.x +300)
                self.boss_fireball_say3 = int(Hero.center_pos_y) - (self.rect.y +400)

                self.angle = math.atan2(self.boss_fireball_say,self.boss_fireball_sax)
                self.sokudox = self.speed * math.cos(self.angle)
                self.sokudoy = self.speed * math.sin(self.angle)

                self.angle2 = math.atan2(self.boss_fireball_say2,self.boss_fireball_sax2)
                self.sokudox2 = self.speed * math.cos(self.angle2)
                self.sokudoy2 = self.speed * math.sin(self.angle2)

                self.angle3 = math.atan2(self.boss_fireball_say3,self.boss_fireball_sax3)
                self.sokudox3 = self.speed * math.cos(self.angle3)
                self.sokudoy3 = self.speed * math.sin(self.angle3)


                self.fire_sokudo = (self.sokudox,self.sokudoy)
                self.fire_sokudo2 = (self.sokudox2,self.sokudoy2)
                self.fire_sokudo3 = (self.sokudox3,self.sokudoy3)

                Rabbit_fireball((self.rect.x +300, self.rect.y + 200),self.fire_sokudo,Map.blocks)
                Rabbit_fireball((self.rect.x +300, self.rect.y + 300),self.fire_sokudo2,Map.blocks)
                Rabbit_fireball((self.rect.x +300, self.rect.y + 400),self.fire_sokudo3,Map.blocks)
                self.rabbit_fireball_interval_time = 300

        for self.fire_ball in self.fire_balls:
            self.collide = self.collision(self.rect.top,self.rect.bottom,self.rect.left,self.rect.right,self.fire_ball.rect.top,self.fire_ball.rect.bottom,self.fire_ball.rect.left,self.fire_ball.rect.right)
            if self.collide:
                self.fire_ball.kill()
                th5 = threading.Thread(target=self.rabbit_damage_dead_process)
                th5.start()

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
