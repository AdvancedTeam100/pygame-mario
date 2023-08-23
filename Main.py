
import pygame
from pygame.locals import *
import time
import sys
import threading
import math
import numpy as np

import Hero
import Meter
import Blockm
import Waku_Block
import Block
import Ghost
import Shinigami
import Sparkball
import Rabbit
import Rabbit_fireball
import FireBall
import Light_circle
import Monster_dead
import Key
import SunaDokei
import Drop_SunaDokei
import Takarabako
import Drop_Takarabako
import Door
import Needle
import Gargoyle
import Gargoyle_flame
import Kishi
import Lich
import Lich_fireball
import Map

from Main import PyMain

SCR_RECT = Rect(0, 0, 1200, 750)

class PyMain:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("Python_oop")

        Hero.walking_anime = [0]*6
        Monster_dead.honou_anime = [0]*2
        Kishi.hokou = [0]*4
        Meter.meter = [0]*11
        
        PyMain.status = 0
        PyMain.wand_switch = 0
        PyMain.key_flag = 0
        PyMain.life = 10000
        PyMain.score = 0
        PyMain.zanki = 3
        PyMain.gameover = 0
        PyMain.shot_switch = 0
        PyMain.meter_count = 0
        PyMain.men_aida_timer = 300
        PyMain.men = 1
        PyMain.men_clear = 0
        Light_circle.switch = False
        PyMain.stage_select = 1

        # high_scoreをファイルより読み出す。
        self.all_high_score = np.loadtxt("assets/score.dat")

#--------------------------------------------------画像読込--------------------------------
        # ブロック画像読み込み
        Block.image = pygame.image.load("renga.png")
        Blockm.image = pygame.image.load("mono_renga.png")
        Waku_Block.image = pygame.image.load("mono_renga.png")

#--------------------------------------------------
        # モンスター「Ghost」の画像読み込み
        Ghost.right_image = pygame.image.load("ghost.png")
        Ghost.left_image = pygame.transform.flip(Ghost.right_image, 1, 0)
        Ghost.image = Ghost.right_image

#--------------------------------------------------

        #主人公
        Hero.right_image = pygame.image.load("chara1.png")
        Hero.left_image = pygame.transform.flip(Hero.right_image, 1, 0)

        # 歩行_画像
        # 右向き
        Hero.walking_anime[0] = pygame.image.load("chara4.png")
        Hero.walking_anime[1] = pygame.image.load("chara5.png")
        # 左向き
        Hero.walking_anime[2] = pygame.transform.flip(Hero.walking_anime[0], 1, 0)
        Hero.walking_anime[3] = pygame.transform.flip(Hero.walking_anime[1], 1, 0)

        # 中割
        Hero.walking_anime[4] = pygame.image.load("n.png")
        Hero.walking_anime[5] = pygame.transform.flip(Hero.walking_anime[4], 1, 0)

        # 死亡時
        Hero.dead = pygame.image.load("dead.png")

        # 主人公_初期化
        Hero.image = Hero.right_image

#--------------------------------------------------

        # 立ち状態_杖_振り上げ_右向き
        Hero.stand_wand_up_right = pygame.image.load("chara2.png")
        # 立ち状態_杖_振り下ろし_右向き
        Hero.stand_wand_down_right = pygame.image.load("chara3.png")
        # 立ち状態_杖_振り上げ_左向き
        Hero.stand_wand_up_left = pygame.transform.flip(Hero.stand_wand_up_right, 1, 0)
        # 立ち状態_杖_振り下ろし_左向き
        Hero.stand_wand_down_left = pygame.transform.flip(Hero.stand_wand_down_right, 1, 0)

        # 座り状態_杖_振り上げ_右向き
        Hero.sit_wand_up_right = pygame.image.load("chara6.png")
        # 座り状態_杖_振り下ろし_右向き
        Hero.sit_wand_down_right = pygame.image.load("chara7.png")

        # 座り状態_杖_振り上げ_左向き
        Hero.sit_wand_up_left = pygame.transform.flip(Hero.sit_wand_up_right, 1, 0)
        # 座り状態_杖_振り下ろし_左向き
        Hero.sit_wand_down_left = pygame.transform.flip(Hero.sit_wand_down_right, 1, 0)

        # ブロック_上_下した状態
        Hero.block_ue_down = pygame.image.load("chara10.png")
        # ブロック上_杖_振り上げ
        Hero.block_ue_up = pygame.image.load("chara11.png")

#--------------------------------------------------

        # 主人公の魔法「FireBall」
        FireBall.right_image = pygame.image.load("honou5.png")
        FireBall.right_image2 = pygame.image.load("honou5_2.png")
        FireBall.left_image = pygame.transform.flip(FireBall.right_image, 1, 0)
        FireBall.left_image2 = pygame.transform.flip(FireBall.right_image2, 1, 0)
        FireBall.image = FireBall.right_image

#--------------------------------------------------

        # 主人公の魔法「Light_circle」
        Light_circle.image = pygame.image.load("light_circle3.png")

#--------------------------------------------------

        # 鍵
        Key.image = pygame.image.load("key.png")

#--------------------------------------------------
        
        # 砂時計
        SunaDokei.image = pygame.image.load("suna.png")
        # ドロップ砂時計
        Drop_SunaDokei.image = pygame.image.load("suna.png")
        # 宝箱
        Takarabako.image = pygame.image.load("takarabako.png")
        # ドロップ宝箱
        Drop_Takarabako.image = pygame.image.load("takarabako.png")

#--------------------------------------------------
        # ドア
        Door.close_image = pygame.image.load("door.png")
        Door.open_image = pygame.image.load("door2.png")
        Door.image = Door.close_image

#--------------------------------------------------

        # モンスター死亡アニメーション
        Monster_dead.honou_anime[0] = pygame.image.load("monster_dead.png")
        Monster_dead.honou_anime[1] = pygame.transform.flip(Monster_dead.honou_anime[0], 1, 0)
        Monster_dead.image = Monster_dead.honou_anime[0]

#--------------------------------------------------

        # 針
        Needle.image = pygame.image.load("needle.png")

#--------------------------------------------------     

        # ガーゴイル
        Gargoyle.right_image = pygame.image.load("gargoyle.png")
        Gargoyle.left_image = pygame.transform.flip(Gargoyle.right_image, 1, 0)
        Gargoyle.image = Gargoyle.right_image

        # ガーゴイルの吐く炎
        Gargoyle_flame.right_image = pygame.image.load("honou.png")
        Gargoyle_flame.left_image = pygame.transform.flip(Gargoyle_flame.right_image, 1, 0)
        Gargoyle_flame.image = Gargoyle_flame.right_image

#--------------------------------------------------  

        # 騎士
        Kishi.hokou[0] = pygame.image.load("kishi.png")
        Kishi.hokou[1] = pygame.image.load("kishi2.png")
        Kishi.hokou[2] = pygame.transform.flip(Kishi.hokou[0], 1, 0)
        Kishi.hokou[3] = pygame.transform.flip(Kishi.hokou[1], 1, 0)
        Kishi.image = Kishi.hokou[0]

#--------------------------------------------------

        # リッチ
        Lich.image = pygame.image.load("mahou_tsukai.png")
        # リッチファイヤーボール
        Lich_fireball.image = pygame.image.load("fireball2.png")

#--------------------------------------------------
        # 死神
        Shinigami.right_image = pygame.image.load("shinigami.png")
        Shinigami.left_image = pygame.transform.flip(Shinigami.right_image, 1, 0)
        Shinigami.image = Shinigami.right_image

#--------------------------------------------------

        # スパークボール
        Sparkball.image = pygame.image.load("sparkball.png")

#--------------------------------------------------

        # ラビット_ボス
        Rabbit.left_image = pygame.image.load("rabbit.png")
        Rabbit.right_image = pygame.transform.flip(Rabbit.left_image, 1, 0)
        Rabbit.image = Rabbit.left_image
        
        # ラビット_ダメージ
        Rabbit.damage_left_image = pygame.image.load("rabbit_d.png")
        Rabbit.damage_right_image = pygame.transform.flip(Rabbit.damage_left_image, 1, 0)

        # ラビット_ファイヤーボール
        Rabbit_fireball.image = pygame.image.load("fireball.png")

#--------------------------------------------------


        #Meter
        Meter.meter[0] = pygame.image.load("meter1.png")
        Meter.meter[1] = pygame.image.load("meter2.png")
        Meter.meter[2] = pygame.image.load("meter3.png")
        Meter.meter[3] = pygame.image.load("meter4.png")
        Meter.meter[4] = pygame.image.load("meter5.png")
        Meter.meter[5] = pygame.image.load("meter6.png")
        Meter.meter[6] = pygame.image.load("meter7.png")
        Meter.meter[7] = pygame.image.load("meter8.png")
        Meter.meter[8] = pygame.image.load("meter9.png")
        Meter.meter[9] = pygame.image.load("meter10.png")
        Meter.meter[10] = pygame.image.load("meter11.png")
        Meter.image = Meter.meter[0]

#--------------------------------------------------画像読込end-------------------------------

        self.map = Map()

        # メインループ
        """
        update                 データ上オブジェクトを移動させる。各オブジェクトの「振る舞い」を記述する関数。
        draw                   surface(レイヤーの様なもの)にオブジェクトを描画する。(updateでデータ上オブジェクトは移動している)
        timer                  各status毎の時間経過に伴う処理をまとめたもの。
        pygame.display.update  実画面に反映
        key_handler            キー操作受付
        
        メインループ全体のイメージ
        ① update関数で主人公の位置をx+2,y+1の位置をデータ上移動させる。
        ② draw関数でupdate関数でx+2,y+1の位置にデータ上移動したオブジェクトをsurfaceに描画する。
        ③ pygame.display.updateによりsurface描画した「絵」を実画面に反映させる。
        """
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            self.timer()
            pygame.display.update()
            self.key_handler()

#--------------------------------------------------

    # 杖を振るアニメーション描画関数。
    # 内部でtime.sleep関数を用いている為、並列処理として呼び出される。
    # wand_switchに1が格納されている間は、Heroクラスのself.imageに通常立ち画像 (ボタンが何も押されていない場合に表示されているdefaultの主人公画像) は代入されない。
    def wand_anime(self): #stick

        if self.hero.stand_sit_switch == 0:
            if self.hero.muki == 0:
                PyMain.wand_switch = 1
                self.hero.image = Hero.stand_wand_up_right
                time.sleep(0.05)
                self.hero.image = Hero.stand_wand_down_right
                time.sleep(0.2)
                PyMain.wand_switch = 0
            elif self.hero.muki == 1:
                PyMain.wand_switch = 1
                self.hero.image = Hero.stand_wand_up_left
                time.sleep(0.05)
                self.hero.image = Hero.stand_wand_down_left
                time.sleep(0.2)
                PyMain.wand_switch = 0
        elif self.hero.stand_sit_switch == 1:
            if self.hero.muki == 0:
                PyMain.wand_switch = 1
                self.hero.image = Hero.sit_wand_up_right
                time.sleep(0.05)
                self.hero.image = Hero.sit_wand_down_right
                time.sleep(0.2)
                PyMain.wand_switch = 0
            elif self.hero.muki == 1:
                PyMain.wand_switch = 1
                self.hero.image = Hero.sit_wand_up_left
                time.sleep(0.05)
                self.hero.image = Hero.sit_wand_down_left
                time.sleep(0.2)
                PyMain.wand_switch = 0

    # wand_anime上 主人公が頭上にブロックを作る場合のアニメーション。
    def wand_anime_ue(self): #block
        if self.hero.stand_sit_switch == 0:
            PyMain.wand_switch = 1
            self.hero.image = Hero.block_ue_down
            time.sleep(0.05)
            self.hero.image = Hero.block_ue_up
            time.sleep(0.2)
            PyMain.wand_switch = 0

    # 主人公生成関数。
    def hero_seisei(self): 
        if PyMain.men == 1:
            self.hero = Hero((50,600))
        elif PyMain.men == 2:
            self.hero = Hero((50,100))
        elif PyMain.men == 3:
            self.hero = Hero((50,500))
        elif PyMain.men == 4:
            self.hero = Hero((50,50))

    # 初期化関数
    def init(self):
        # key_flagについて：鍵を取ると1が代入される。値が1の状態で扉に到達するとclearになる。
        PyMain.key_flag = 0
        # men_clearについて：プレイする面をclearすると1が代入される。
        PyMain.men_clear = 0
        # lifeについて：life = 制限時間
        PyMain.life = 10000
        # meter_countについて：メーターを制御する変数。
        PyMain.meter_count = 0
        # scoreについて：スコア
        PyMain.score = 0
        # shot_switchについて：メーターがフルになると1が代入され、魔法「ファイヤーボール」を放つことが出来る。
        PyMain.shot_switch = 0
        # switchについて：値がFalseの時、魔法陣「Light_circle」を使う事が出来る。画面上に魔法陣「Light_circle」が表示されている間はTrueが入る
        # つまり画面上に二つ同時に描く事は出来ない。
        Light_circle.switch = False

    # タイマー関数。制限時間(ライフ)を1フレーム毎に1減少させる関数。タイムオーバーの際の処理も担う。
    # 各status状態に留まる時間をカウントし、一定の時間経過したらstatusを変更する処理を担う。
    """
    各status説明
    0 タイトル画面
    1 ゲーム画面
    2 RETRY
    3 GAME_OVER
    4 X Stage Clear
    5 GAME_CLEAR
    """
    def timer(self):
        if PyMain.status == 1:
            PyMain.life -= 1
            
            # タイムオーバー時の処理
            if PyMain.life <= 0:
                th6 = threading.Thread(target=self.hero.dead_process)
                th6.start()

        # 残機あり、死亡時
        elif PyMain.status == 2:
            PyMain.men_aida_timer -= 1

            if PyMain.men_aida_timer <= 0 and self.hero.dead_switch == 1:
                PyMain.status = 1
                PyMain.men_aida_timer = 300
                self.init()
                self.hero_seisei()
                Map.men_data()
                Map.load()

        # 残機なし、死亡時
        elif PyMain.status == 3:
            PyMain.men_aida_timer -= 1

            if PyMain.men_aida_timer <= 0 and self.hero.dead_switch == 1:
                PyMain.status = 0
                PyMain.zanki = 3
                PyMain.men_aida_timer = 300
        
        # 面クリア時
        elif PyMain.status == 4:
            PyMain.men_aida_timer -= 1

            if PyMain.men_aida_timer <= 0 and PyMain.men_clear == 1:
                
                # 残Lifeをscoreに加算する。
                PyMain.score = PyMain.score + PyMain.life
                # scoreが保存されていたhigh_scoreより大きな値であった場合、high_scoreとして保存する。
                if PyMain.score > PyMain.high_score:
                    self.all_high_score[PyMain.men - 1] = PyMain.score
                    np.savetxt('score.dat', self.all_high_score,fmt="%.0f")
                
                # 次面へ
                PyMain.status = 1
                PyMain.men_aida_timer = 300
                PyMain.men += 1
                PyMain.high_score = self.all_high_score[PyMain.men - 1]
                self.init()
                self.hero_seisei()
                Map.men_data()
                Map.load()                    

#--------------------------------------------------

    # mapクラスのupdate関数を呼び出しているだけ。
    def update(self):
        self.map.update()

    # mapクラスのdraw関数を呼び出しているだけ。
    def draw(self, screen):
        self.map.draw(screen)

    # キー入力を捉え、紐づく処理を行っている。例：sボタンを押下したら前方にブロックを作る。
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # タイトル画面におけるステージセレクト
            # status == 0の場合(タイトル画面の場合)
            if PyMain.status == 0:
                # 下キーを押した場合。ステージセレクト。
                if event.type == KEYDOWN and event.key == K_DOWN:
                    if PyMain.stage_select == 1:
                        PyMain.stage_select = 2
                    elif PyMain.stage_select == 2:
                        PyMain.stage_select = 3
                    elif PyMain.stage_select == 3:
                        PyMain.stage_select = 4

                    elif PyMain.stage_select == 4:
                        PyMain.stage_select = 1

                # 上キーを押した場合。ステージセレクト。
                elif event.type == KEYDOWN and event.key == K_UP:
                    if PyMain.stage_select == 1:
                        PyMain.stage_select = 4

                    elif PyMain.stage_select == 2:
                        PyMain.stage_select = 1
                    elif PyMain.stage_select == 3:
                        PyMain.stage_select = 2
                    elif PyMain.stage_select == 4:
                        PyMain.stage_select = 3

                # リターンを押した場合。遊ぶ面を決定。 rounding selection
                elif event.type == KEYDOWN and event.key == K_RETURN:
            
                    if PyMain.stage_select == 1:
                        PyMain.status = 1
                        PyMain.men = 1
                        PyMain.high_score = self.all_high_score[PyMain.men - 1]
                        self.hero_seisei()
                        Map.men_data()
                        Map.load()

                    elif PyMain.stage_select == 2:
                        PyMain.status = 1
                        PyMain.men = 2
                        PyMain.high_score = self.all_high_score[PyMain.men - 1]
                        self.hero_seisei()
                        Map.men_data()
                        Map.load()

                    elif PyMain.stage_select == 3:
                        PyMain.status = 1
                        PyMain.men = 3
                        PyMain.high_score = self.all_high_score[PyMain.men - 1]
                        self.hero_seisei()
                        Map.men_data()
                        Map.load()

                    elif PyMain.stage_select == 4:
                        PyMain.status = 1
                        PyMain.men = 4
                        PyMain.high_score = self.all_high_score[PyMain.men - 1]
                        self.hero_seisei()
                        Map.men_data()
                        Map.load()

            # ゲーム画面における操作
            elif PyMain.status == 1:
                # 目の前にブロックを作る or 目の前のブロックを消す。
                if event.type == KEYDOWN and event.key == K_s and self.hero.stand_sit_switch == 0 and self.hero.dead_switch == 0:
                    th1 = threading.Thread(target=self.wand_anime)
                    th1.start()

                    # 主人公の中心座標より主人公の居るマスを割り出している。 // set position
                    self.squares_number_x = math.floor(self.hero.rect.centerx / 50)
                    self.squares_number_y = math.floor(self.hero.rect.centery / 50)

                    # 主人公が右を向いている場合、主人公が居るマスの一つ右のマス目にブロックを作る。 // right position
                    if self.hero.muki == 0:
                        if self.map.men[self.squares_number_y][self.squares_number_x + 1] == 0:
                            self.map.men[self.squares_number_y][self.squares_number_x + 1] = 3
                        elif self.map.men[self.squares_number_y][self.squares_number_x + 1] == 3:
                            self.map.men[self.squares_number_y][self.squares_number_x + 1] = 0

                        # もし出現させたブロックと主人公が重なっていた場合、主人公の位置を修正する。
                        if (self.squares_number_x + 1) * 50 < self.hero.hero_pos_x + 40:
                            self.hero.hero_pos_x = (self.squares_number_x + 1) * 50 - 40

                    # 主人公が左を向いている場合、主人公が居るマスの一つ左のマス目にブロックを作る。// left position
                    if self.hero.muki == 1:
                        if self.map.men[self.squares_number_y][self.squares_number_x - 1] == 0:
                            self.map.men[self.squares_number_y][self.squares_number_x - 1] = 3
                        elif self.map.men[self.squares_number_y][self.squares_number_x - 1] == 3:
                            self.map.men[self.squares_number_y][self.squares_number_x - 1] = 0
                        
                        # もし出現させたブロックと主人公が重なっていた場合、主人公の位置を修正する。
                        if self.squares_number_x * 50 > self.hero.hero_pos_x:
                            self.hero.hero_pos_x = self.squares_number_x * 50

                    self.map.load()


                # しゃがんだ状態_x + 1,y + 1 の位置にブロックを出現させる。 
                elif event.type == KEYDOWN and event.key == K_s and self.hero.stand_sit_switch == 1 and self.hero.dead_switch == 0:
                    th1 = threading.Thread(target=self.wand_anime)
                    th1.start()

                    # 自マス座標を算出
                    self.squares_number_x = math.floor(self.hero.rect.centerx / 50)
                    self.squares_number_y = math.floor(self.hero.rect.centery / 50)

                    if self.hero.muki == 0:
                        if self.map.men[self.squares_number_y +1][self.squares_number_x + 1] == 0:
                            self.map.men[self.squares_number_y +1][self.squares_number_x + 1] = 3
                        elif self.map.men[self.squares_number_y +1][self.squares_number_x + 1] == 3:
                            self.map.men[self.squares_number_y +1][self.squares_number_x + 1] = 0
                    elif self.hero.muki == 1:
                        if self.map.men[self.squares_number_y + 1][self.squares_number_x - 1] == 0:
                            self.map.men[self.squares_number_y + 1][self.squares_number_x - 1] = 3
                        elif self.map.men[self.squares_number_y + 1][self.squares_number_x - 1] == 3:
                            self.map.men[self.squares_number_y + 1][self.squares_number_x - 1] = 0
                    
                    self.map.load()

                # 頭上にブロックを作る。
                elif event.type == KEYDOWN and event.key == K_e:
                    th10 = threading.Thread(target=self.wand_anime_ue)
                    th10.start()

                    self.squares_number_x = math.floor(self.hero.rect.centerx / 50)
                    self.squares_number_y = math.floor(self.hero.rect.centery / 50)

                    if self.map.men[self.squares_number_y - 1][self.squares_number_x] == 0:
                        self.map.men[self.squares_number_y - 1][self.squares_number_x] = 3
                    elif self.map.men[self.squares_number_y - 1][self.squares_number_x] == 3:
                        self.map.men[self.squares_number_y - 1][self.squares_number_x] = 0

                    self.map.load()


                # 魔法「FireBall」を放つ。条件は次の通り。主人公が立った状態にある。主人公が死亡した状態にない。魔力メーターがFULLの状態でshot_switchが1の場合。
                elif event.type == KEYDOWN and event.key == K_d and self.hero.stand_sit_switch == 0 and self.hero.dead_switch == 0 and PyMain.shot_switch == 1:
                    th1 = threading.Thread(target=self.wand_anime)
                    th1.start()
                    FireBall(self.hero.rect.center, self.hero.muki)
                    PyMain.shot_switch = 0
                    PyMain.meter_count = 0

                # 魔法「Light_circle」を描く。二つ同時には描くことは出来ない。
                # Light_circleが画面上に表示されている間switch は Trueとなっている。
                elif event.type == KEYDOWN and event.key == K_f and Light_circle.switch == False:
                    th9 = threading.Thread(target=self.wand_anime_ue)
                    th9.start()
                    Light_circle((Hero.center_pos_x,Hero.center_pos_y))
                    Light_circle.switch = True
                    
if __name__ == "__main__":
    PyMain()