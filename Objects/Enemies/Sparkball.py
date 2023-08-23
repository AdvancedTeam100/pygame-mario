import pygame
import math

import Map
from Main import PyMain

# ブロック(通常ブロック・モノクロブロック)の周りを回るモンスター。倒すことは出来ない。
class Sparkball(pygame.sprite.Sprite):
    # 受け取る引数は((x,y),速度,初期の移動方向)
    def __init__(self,pos,speed,shoki_muki):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = speed
        self.shoki_muki = shoki_muki

        # 初期の移動方向
        if self.shoki_muki == 0:
            self.speedx = 0
            self.speedy = -self.speed
            self.sparkball_muki = 0
        elif self.shoki_muki == 1:
            self.speedx = self.speed
            self.speedy = 0
            self.sparkball_muki = 1
        elif self.shoki_muki == 2:
            self.speedx = -self.speed
            self.speedy = 0
            self.sparkball_muki = 2
        elif self.shoki_muki == 3:
            self.speedx = 0
            self.speedy = self.speed
            self.sparkball_muki = 3

        self.sparkball_collision_switch = 0
        self.sparkball_first_calc_swtich = 0
        self.sparkball_turn_point = 0
        self.turning_pointx = 0
        self.turning_pointy = 0

        # ブロック情報、通常、モノクロ、枠ブロックいずれかのブロックがあった場合1となる。ポイズンボールはこの値を参照し移動する。
        self.back = ([
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ])

    def update(self):
        Map.all.move_to_front(self) 
        self.rect.move_ip(self.speedx, self.speedy)

        # ポイズンボールが現在いる座標を格納している。
        self.sparkball_squares_number_x = math.floor(self.rect.x/50)
        self.sparkball_squares_number_y = math.floor(self.rect.y/50)

        self.sparkball_squares_number_x2 = math.floor(self.rect.right/50)
        self.sparkball_squares_number_y2 = math.floor(self.rect.bottom/50)
        # mapdataの1変換
        # ポイズンボールは「通常ブロック」「モノクロブロック」「枠風ブロック」の周りを回るモンスターである。コードを簡略化する為、self.backに通常・モノクロ・枠ブロックの位置情報をまとめる。
        # いずれかのブロックがある箇所には1を、いずれのブロックもない箇所には0を格納する。
        for i in range(15):
            for j in range(19):
                if Map.men[i][j] == 1:
                    self.back[i][j] = 1
                elif Map.men[i][j] == 2:
                    self.back[i][j] = 1
                elif Map.men[i][j] == 3:
                    self.back[i][j] = 1
                elif Map.men[i][j] == 0:
                    self.back[i][j] = 0

        # 上に進んでいる場合の処理
        if self.sparkball_muki == 0:
            
            # self.turning_pointx self.turning_pointy にはポイズンボールがその進行方向を変化させた時の座標が収まっている。ポイズンボールがその座標にいる限り続けて2回以上の方向転換は起こらない。(例外在り)三方がブロックに囲まれているマスでは続けての方向転換が起こる。
            if (self.turning_pointx != self.sparkball_squares_number_x or self.turning_pointy != self.sparkball_squares_number_y) or (self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == 1):
                # 上に進んでいる時、ポイズンボールが左右どちらのブロックに接しているかを判定している。
                self.right_squares_number_x = math.floor((self.rect.right +3)/50)
                self.left_squares_number_x = math.floor((self.rect.left -3)/50)

                # 右に接地している場合
                if self.right_squares_number_x == self.sparkball_squares_number_x + 1:
                    self.adhesion = 1
                # 左に接地している場合
                elif self.left_squares_number_x == self.sparkball_squares_number_x - 1:
                    self.adhesion = 2

                if self.adhesion == 1:
                    # ただ右に接地しながら上に進んでいるだけ
                    if self.right_squares_number_x == self.sparkball_squares_number_x + 1 and self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1:
                        self.adhesion = 1
                        #print("右に接地しています")
                    
                    # 上に進んでいる途中、接地していた右側のブロックが途切れ、右方向に曲がる場合。
                    elif self.right_squares_number_x == self.sparkball_squares_number_x + 1 and self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 0 and self.sparkball_squares_number_y*50 + 15 >= self.rect.y:
                        # 移動方向を変えた時の座標を保存している。
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)
                        #print("右方向に進みます")
                        self.speedx = self.speed
                        self.speedy = 0
                        self.sparkball_muki = 1

                    # ブロックに衝突して左に曲がる。ブロックがある方向　右と上
                    if self.right_squares_number_x == self.sparkball_squares_number_x + 1 and self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == 1:
                        #print("左に曲がりたいでごわす")。衝突する上ブロックに接近したら。
                        self.top_squares_number_y = math.floor((self.rect.top -3)/50)
                        if self.top_squares_number_y == self.sparkball_squares_number_y - 1:
                            # 座標修正。
                            self.rect.top = (self.sparkball_squares_number_y)*50
                            self.speedx = -self.speed
                            self.speedy = 0
                            self.sparkball_muki = 2
                            self.turning_pointx = math.floor(self.rect.x/50)
                            self.turning_pointy = math.floor(self.rect.y/50)                            
                # 左にあるブロックに接地している場合
                elif self.adhesion == 2:
                    # 左にあるブロックに接地しながら、上方向に進んでいたが、左ブロックが途切れ、左に曲がる場合。
                    # 左にあったブロックが途切れ　且つ、自座標が次の条件を満たしたら曲がる。self.sparkball_squares_number_y*50 + 15 >= self.rect.top
                    if self.left_squares_number_x == self.sparkball_squares_number_x - 1 and self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == 0 and self.sparkball_squares_number_y*50 + 15 >= self.rect.top:
                        #print("左に曲がりたいだわさ～")
                        self.speedx = -self.speed
                        self.speedy = 0
                        self.sparkball_muki = 2
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)
                    # 左のブロックに接地している。且つ、上マスにブロックがある場合、右に曲がる。
                    if self.left_squares_number_x == self.sparkball_squares_number_x - 1 and self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == 1:
                        # rect.top-3 のマス座標が現自座標y-1と等しくなるまで上ブロックに接近したら右に曲がる。
                        self.top_squares_number_y = math.floor((self.rect.top -3)/50)
                        if self.top_squares_number_y == self.sparkball_squares_number_y - 1:
                            self.rect.top = (self.sparkball_squares_number_y)*50
                            self.speedx = self.speed
                            self.speedy = 0
                            self.sparkball_muki = 1
                            self.turning_pointx = math.floor(self.rect.x/50)
                            self.turning_pointy = math.floor(self.rect.y/50)


        # 右に進んでいる場合の処理    
        elif self.sparkball_muki == 1:
            if (self.turning_pointx != self.sparkball_squares_number_x or self.turning_pointy != self.sparkball_squares_number_y) or (self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1) or (self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1):
                # 前半はボールと下マスとが近いということ。後半はマス番号。
                self.bottom_squares_number_y = math.floor((self.rect.bottom + 3)/50)
                self.top_squares_number_y_2 = math.floor((self.rect.top - 3)/50)

                # 下に接地している場合
                if self.bottom_squares_number_y == self.sparkball_squares_number_y + 1:
                    self.adhesion = 1

                # 上に接地している場合
                elif self.top_squares_number_y_2 == self.sparkball_squares_number_y - 1:
                    self.adhesion = 2

                if self.adhesion == 1:
                    if self.bottom_squares_number_y == self.sparkball_squares_number_y + 1 and self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == 1:
                        #print("下に接地しています")
                        if self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1:
                            self.right_squares_number_x_2 = math.floor((self.rect.right +3)/50)
                            if self.right_squares_number_x_2 == self.sparkball_squares_number_x + 1:
                                self.rect.left = (self.sparkball_squares_number_x + 1)*50 - 35
                                self.speedx = 0
                                self.speedy = -self.speed
                                self.sparkball_muki = 0
                                self.turning_pointx = math.floor(self.rect.x/50)
                                self.turning_pointy = math.floor(self.rect.y/50)

                    elif self.bottom_squares_number_y == self.sparkball_squares_number_y + 1 and self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == 0:
                        #print("下方向に進みます")
                        self.rect.left = (self.sparkball_squares_number_x)*50
                        self.speedx = 0
                        self.speedy = self.speed
                        self.sparkball_muki = 3
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)

                elif self.adhesion == 2:
                    #print("上に接地しているんだな")
                    if self.top_squares_number_y_2 == self.sparkball_squares_number_y - 1 and self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == 0 and self.sparkball_squares_number_x*50 <= self.rect.left:
                        self.speedx = 0
                        self.speedy = -self.speed
                        self.sparkball_muki = 0
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)

                    elif self.top_squares_number_y_2 == self.sparkball_squares_number_y - 1 and self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == 1:
                        if self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1:
                                self.right_squares_number_x_3 = math.floor((self.rect.right +3)/50)
                                if self.right_squares_number_x_3 == self.sparkball_squares_number_x + 1:
                                    self.rect.left = (self.sparkball_squares_number_x + 1)*50 - 35
                                    self.speedx = 0
                                    self.speedy = self.speed
                                    self.sparkball_muki = 3
                                    self.turning_pointx = math.floor(self.rect.x/50)
                                    self.turning_pointy = math.floor(self.rect.y/50)


        # 左に進んでいる場合の処理
        elif self.sparkball_muki == 2:
            if (self.turning_pointx != self.sparkball_squares_number_x or self.turning_pointy != self.sparkball_squares_number_y) or (self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1) or (self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1):
                self.top_squares_number_y_3 = math.floor((self.rect.top -3)/50)
                self.bottom_squares_number_y_2 = math.floor((self.rect.bottom +3)/50)

                # 上に接地している場合
                if self.top_squares_number_y_3 == self.sparkball_squares_number_y - 1:
                    self.adhesion = 1
                # 下に接地している場合
                elif self.bottom_squares_number_y_2 == self.sparkball_squares_number_y + 1:
                    self.adhesion = 2

                if self.adhesion == 1:
                    # 上に接地している
                    if self.top_squares_number_y_3 == self.sparkball_squares_number_y - 1 and self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == 1:
                        #print("上に接地しています")
                        # 左にブロックが場合、下方向に移動する。
                        if self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == 1:
                            self.left_squares_number_x_2 = math.floor((self.rect.left - 3)/50)
                            if self.left_squares_number_x_2 == self.sparkball_squares_number_x - 1:
                                self.rect.left = (self.sparkball_squares_number_x)*50
                                self.speedx = 0
                                self.speedy = self.speed
                                self.sparkball_muki = 3
                                self.turning_pointx = math.floor(self.rect.x/50)
                                self.turning_pointy = math.floor(self.rect.y/50)
                    
                    # 上に接地していたが、上ブロックが途切れ、上方向に方向転換する。
                    elif self.top_squares_number_y_3 == self.sparkball_squares_number_y - 1 and self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == 0 and self.sparkball_squares_number_x*50 + 15 >= self.rect.left:
                        self.speedx = 0
                        self.speedy = -self.speed
                        self.sparkball_muki = 0
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)

                # 下に接地している
                elif self.adhesion == 2:
                    if self.bottom_squares_number_y_2 == self.sparkball_squares_number_y + 1 and self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == 1:
                        #print("下に接地しています")
                        # 左にブロックがあった場合、上方向に方向転換する。
                        if self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == 1:
                            self.left_squares_number_x_2 = math.floor((self.rect.left - 3)/50)
                            if self.left_squares_number_x_2 == self.sparkball_squares_number_x - 1:
                                self.rect.left = (self.sparkball_squares_number_x)*50
                                #print("上方向に移動します")
                                self.speedx = 0
                                self.speedy = -self.speed
                                self.sparkball_muki = 0
                                self.turning_pointx = math.floor(self.rect.x/50)
                                self.turning_pointy = math.floor(self.rect.y/50)

                    elif self.bottom_squares_number_y_2 == self.sparkball_squares_number_y + 1 and self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == 0 and self.sparkball_squares_number_x*50 + 15 >= self.rect.left:
                        self.speedx = 0
                        self.speedy = self.speed
                        self.sparkball_muki = 3
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)


        # 下に進んでいる場合の処理
        elif self.sparkball_muki == 3:
            if (self.turning_pointx != self.sparkball_squares_number_x or self.turning_pointy != self.sparkball_squares_number_y) or (self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1) or (self.back[self.sparkball_squares_number_y - 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == 1):
                self.left_squares_number_x_5 = math.floor((self.rect.left -3)/50)
                self.right_squares_number_x_5 = math.floor((self.rect.right +3)/50)
                # 左に接地している場合
                if self.left_squares_number_x_5 == self.sparkball_squares_number_x - 1:
                    self.adhesion = 1
                # 右に接地している場合
                elif self.right_squares_number_x_5 == self.sparkball_squares_number_x + 1:
                    self.adhesion = 2

                if self.adhesion == 1: 

                    if self.left_squares_number_x_5 == self.sparkball_squares_number_x - 1 and self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == 1:
                        #print("左に接地しています")

                        # 衝突して右方向に曲がる場合の処理
                        if self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == 1:
                            self.bottom_squares_number_y_3 = math.floor((self.rect.bottom +3)/50)
                            if self.bottom_squares_number_y_3 == self.sparkball_squares_number_y + 1:
                                self.rect.top = (self.sparkball_squares_number_y + 1)*50 - 35
                                self.speedx = self.speed
                                self.speedy = 0
                                self.sparkball_muki = 1
                                self.turning_pointx = math.floor(self.rect.x/50)
                                self.turning_pointy = math.floor(self.rect.y/50)

                    elif self.left_squares_number_x_5 == self.sparkball_squares_number_x - 1 and self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x - 1] == 0:
                        #print("左に曲がりたいだわさ～")
                        self.speedx = -self.speed
                        self.speedy = 0
                        self.sparkball_muki = 2
                        self.rect.top = (self.sparkball_squares_number_y)*50
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)
                
                elif self.adhesion == 2:
                    if self.right_squares_number_x_5 == self.sparkball_squares_number_x + 1 and self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 1:
                        #print("右に接地しています")
                        if self.back[self.sparkball_squares_number_y + 1][self.sparkball_squares_number_x] == 1:
                            self.bottom_squares_number_y_3 = math.floor((self.rect.bottom +3)/50)
                            if self.bottom_squares_number_y_3 == self.sparkball_squares_number_y + 1:
                                self.rect.top = (self.sparkball_squares_number_y + 1)*50 - 35
                                self.speedx = -self.speed
                                self.speedy = 0
                                self.sparkball_muki = 2
                                self.turning_pointx = math.floor(self.rect.x/50)
                                self.turning_pointy = math.floor(self.rect.y/50)

                    elif self.right_squares_number_x_5 == self.sparkball_squares_number_x + 1 and self.back[self.sparkball_squares_number_y][self.sparkball_squares_number_x + 1] == 0:
                        #print("右に曲がるってばよ")
                        self.speedx = self.speed
                        self.speedy = 0
                        self.sparkball_muki = 1
                        self.turning_pointx = math.floor(self.rect.x/50)
                        self.turning_pointy = math.floor(self.rect.y/50)

        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
