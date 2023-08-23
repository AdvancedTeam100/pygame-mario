import pygame
from pygame.locals import *
import time
import threading

import Map
from Main import PyMain

class Hero(pygame.sprite.Sprite):
    # 主人公
    
    # 重力加速度、移動スピード、及び、ジャンプ力。
    GRAVITY = 0.2
    MOVE_SPEED = 3.0
    JUMP_SPEED = 5.0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.muki = 0

        self.hero_pos_x = float(self.rect.x)
        self.hero_pos_y = float(self.rect.y)
        self.hero_vel_x = 0.0
        self.hero_vel_y = 0.0
        Hero.posx = 0
        Hero.posy = 0
        self.on_floor = False
        self.first_touch_switch = 0
        self.walking_anime_count = 10
        self.stand_sit_switch = 0
        self.dead_switch = 0
        self.monster_first_collision = 0

    # 主人公が死亡した場合の処理。
    def dead_process(self):

        if self.dead_switch == 0:
            self.dead_switch = 1
            self.hero_vel_x = 0
            self.image = Hero.dead
            for x in range(15):
                time.sleep(0.01)
                self.hero_pos_y -= 3
            for x in range(10):
                time.sleep(0.01)
                self.hero_pos_y += 3

            time.sleep(0.5)

            if PyMain.zanki > 0:
                PyMain.zanki -= 1
                PyMain.status = 2
            elif PyMain.zanki == 0:
                PyMain.status = 3

    # 衝突関数。二つのオブジェクトが重なっていた場合、Trueを返し、重なりが無い場合はFalseを返す。
    def collision(self, top1, bottom1, left1, right1, top2, bottom2, left2, right2):
        
        if left1 < right2 and top1 < bottom2 and right1 > left2 and bottom1 > top2:
            return True
        else:
            return False

    # block 移動先のrect値を求める　→　移動先のrect値とブロックとの衝突を調べる。　→　移動先のrect値とブロックとの衝突がみとめられない場合は実際に位置を更新する。
    def collision_x(self):
        # x方向の衝突判定処理
        # 主人公のサイズを取得
        width = self.rect.width
        height = self.rect.height

        # X方向の移動先の座標を求める。
        newx = self.hero_pos_x + self.hero_vel_x
        # 移動先のrect値を求める。
        newrect = Rect(newx, self.hero_pos_y, width, height)

        # ブロックとの衝突判定。画面上にある全てのブロックとの衝突を調べる。
        for block in Map.blocks:
            # 移動先のrect値と取り出した一つのブロックrect値との衝突を調べる。
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突するブロックがあった場合
                if self.hero_vel_x > 0:    # 右に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.hero_pos_x = block.rect.left - width
                    self.hero_vel_x = 0
                elif self.hero_vel_x < 0:  # 左に移動中に衝突
                    self.hero_pos_x = block.rect.right
                    self.hero_vel_x = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.hero_pos_x = newx


    # block Y軸方向の衝突判定処理
    def collision_y(self):
        # 主人公のサイズ
        width = self.rect.width
        height = self.rect.height

        # Y方向の移動先の座標と矩形を求める
        newy = self.hero_pos_y + self.hero_vel_y
        # newrect = Rect(self.hero_pos_x, newy, width, height + 1)

        # ブロックとの衝突判定。処理が円滑に進むように、値を補正している。
        for self.block in Map.blocks:
            #collide = newrect.colliderect(self.block.rect)
            collide = self.collision(newy, newy + height + 1, self.hero_pos_x, self.hero_pos_x + width - 10, self.block.rect.top, self.block.rect.bottom ,self.block.rect.left, self.block.rect.right)
            if collide:  # 衝突するブロックあり
                if self.hero_vel_y > 0:    # 下に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.hero_pos_y = self.block.rect.top - height
                    self.hero_vel_y = 0
                    # 下に移動中に衝突したなら床の上にいる
                    self.on_floor = True

                elif self.hero_vel_y < 0:  # 上に移動中に衝突
                    self.hero_pos_y = self.block.rect.bottom
                    self.hero_vel_y = 0

                elif self.hero_vel_y == 0:
                    # めり込まないように調整
                    self.hero_pos_y  = self.block.rect.top - height
                    # 下に移動中に衝突したなら床の上にいる
                    self.on_floor = True

                break  # 衝突ブロックは1個調べれば十分

            else:
                # 衝突ブロックがない場合、位置を更新
                self.hero_pos_y = newy
                # 衝突ブロックがないなら床の上にいない
                self.on_floor = False


    # item アイテム別に分岐する。アイテムとの衝突処理をまとめる。
    def collision_objects(self):
        for self.object in Map.objects:
            collide = self.rect.colliderect(self.object.rect)
            if collide:
                # アイテム別処理
                # key アイテム「鍵」を手に入れた場合
                if Map.item[int(self.object.rect.centery/50)][int(self.object.rect.centerx/50)] == 1:
                    Map.item[int(self.object.rect.centery/50)][int(self.object.rect.centerx/50)] = 0
                    PyMain.key_flag = 1
                    pygame.sprite.spritecollide(self,Map.objects,True)

                # elif Map.item[int(self.object.rect.centery/50)][int(self.object.rect.centerx/50)] == 2:
                #     Map.item[int(self.object.rect.centery/50)][int(self.object.rect.centerx/50)] = 0
                #     pygame.sprite.spritecollide(self,Map.objects,True)

                # door ドアに衝突した時点で鍵を取得していた場合、面clearとなる。鍵を持っていなかった場合は何も起こらない。
                elif Map.men[int(self.object.rect.centery/50)][int(self.object.rect.centerx/50)] == 4:
                    # Map.men[int(self.object.rect.centery/50)][int(self.object.rect.centerx/50)] = 0
                    if PyMain.key_flag == 0:                        
                        print("鍵を取らないとクリア出来ません")
                    elif PyMain.key_flag == 1:
                        PyMain.men_clear = 1
                        if PyMain.men <= 3:
                            PyMain.status = 4
                        elif PyMain.men ==4:
                            PyMain.status = 5
                
                # 自身とself.bellグループ内のオブジェクトの内いずれかが衝突した場合、そのオブジェクトを削除する。
                # pygame.sprite.spritecollide(self,Map.objects,True)
                break

    # monster モンスターとの衝突判定処理。接触して死亡してしまうオブジェクトは全てmonster扱いになっている。
    def collision_monsters(self):
        for self.monster in Map.monsters:
            collide = self.collision(self.hero_pos_y + 20, self.hero_pos_y + 40 -20, self.hero_pos_x + 20, self.hero_pos_x + 40 - 20, self.monster.rect.top, self.monster.rect.bottom ,self.monster.rect.left, self.monster.rect.right)
            # collide = self.rect.colliderect(self.monster.rect)
            if collide:
                #衝突以下の処理が1度のみ実行されるように設けた分岐。
                if self.monster_first_collision == 0:
                    self.monster_first_collision = 1
                    th2 = threading.Thread(target=self.dead_process)
                    th2.start()

    # hourglass アイテム「砂時計」との衝突判定処理。初期マップに配置されている配置アイテム　と　monsterからdropするドロップアイテム共通の処理。
    def collision_sunadokei(self):
        for self.suna in Map.suna_dokei:
            collide = self.rect.colliderect(self.suna.rect)
            if collide:
                # アイテムマップからアイテムを削除。配置アイテム用の処理。
                if Map.item[int(self.suna.rect.centery/50)][int(self.suna.rect.centerx/50)] == 2:
                    Map.item[int(self.suna.rect.centery/50)][int(self.suna.rect.centerx/50)] = 0
                #自身とself.sunasグループ内のオブジェクトの内いずれかが衝突した場合、そのオブジェクトを削除する。
                pygame.sprite.spritecollide(self,Map.suna_dokei,True)
                PyMain.life += 5000
                break

    # strongbox アイテム「ベル」との衝突判定処理。
    def collision_takarabako(self):
        for self.takara in Map.takarabako:
            collide = self.rect.colliderect(self.takara.rect)
            if collide:
                if Map.item[int(self.takara.rect.centery/50)][int(self.takara.rect.centerx/50)] == 3:
                    Map.item[int(self.takara.rect.centery/50)][int(self.takara.rect.centerx/50)] = 0
                #自身とMap.takarabakoグループ内のオブジェクトの内いずれかが衝突した場合、そのオブジェクトを削除する。
                pygame.sprite.spritecollide(self,Map.takarabako,True)
                PyMain.score += 5000
                break


    def update(self):

        # 主人公の現在位置をクラス変数に収めている。
        Hero.posx = self.rect.left
        Hero.posy = self.rect.top
        Hero.center_pos_x = self.rect.centerx
        Hero.center_pos_y = self.rect.centery

        pressed_keys = pygame.key.get_pressed()
        if self.dead_switch == 0:
            # 左右移動
            # 矢印キーを押し続けた場合。(長押し)
            if pressed_keys[K_RIGHT]:
                self.muki = 0
                # 左右いずれかのキーを長押しする時、押した最初の1フレーム目に一度だけ実行される。画像配列の添え字の初期化。
                if self.first_touch_switch == 0:
                    self.walking_anime_switch = 0
                    self.first_touch_switch = 1

                # self.walking_anime_count：アニメーション用カウント変数
                # self.walking_anime_switch：画像配列の添字
                # moto 中割りを表示する前にABどちらの画像が表示されていたかを保存する変数。A → N → B　　 B → N → A　　　Nの次の画像はmotoが0の場合はA motoが1の場合はBが来る。
                self.walking_anime_count -= 1
                if self.walking_anime_switch == 0 and self.walking_anime_count <= 0:
                    self.walking_anime_count = 10
                    self.moto = 0
                    self.walking_anime_switch = 4
                elif self.walking_anime_switch == 1 and self.walking_anime_count <= 0:
                    self.walking_anime_count = 10
                    self.moto = 1
                    self.walking_anime_switch = 4
                elif self.walking_anime_switch == 4 and self.walking_anime_count <= 0:
                    self.walking_anime_count = 10
                    if self.moto == 0:
                        self.walking_anime_switch = 1
                    elif self.moto == 1:
                        self.walking_anime_switch = 0
                if self.on_floor == True and PyMain.wand_switch == 0:
                    self.image = self.walking_anime[self.walking_anime_switch]
                self.hero_vel_x = self.MOVE_SPEED    

            # 左を長押した場合
            elif pressed_keys[K_LEFT]:
                self.muki = 1
                if self.first_touch_switch == 0:
                    self.walking_anime_switch = 2
                    self.first_touch_switch = 1

                # self.walking_anime_count：アニメーション用カウント変数
                # self.walking_anime_switch：画像配列の添字
                self.walking_anime_count -= 1
                if self.walking_anime_switch == 2 and self.walking_anime_count <= 0:
                    self.walking_anime_count = 10
                    self.walking_anime_switch = 3
                elif self.walking_anime_switch == 3 and self.walking_anime_count <= 0:
                    self.walking_anime_count = 10
                    self.walking_anime_switch = 2
                if self.on_floor == True and PyMain.wand_switch == 0:
                    self.image = self.walking_anime[self.walking_anime_switch]
                self.hero_vel_x = -self.MOVE_SPEED

            # しゃがむ
            elif pressed_keys[K_DOWN]:
                if PyMain.wand_switch == 0:
                    if self.muki == 0:
                        self.image = self.sit_wand_up_right
                        
                    elif self.muki == 1:
                        self.image = self.sit_wand_up_left
                    self.stand_sit_switch = 1
                    if self.on_floor == True:
                        self.hero_vel_x = 0
                        self.hero_vel_y = 0

            # キーが何も押されていない場合の処理。
            else:
                if self.on_floor == True and PyMain.wand_switch != 1 and self.dead_switch == 0:
                    self.hero_vel_x = 0.0
                    self.first_touch_switch = 0
                    self.walking_anime_count = 10
                    self.stand_sit_switch = 0
                    
                    if self.muki == 0:
                        self.image = Hero.right_image
                    elif self.muki == 1:
                        self.image = Hero.left_image

            # ジャンプ
            if pressed_keys[K_SPACE]:
                if self.on_floor:
                    self.hero_vel_y = -self.JUMP_SPEED  # 上向きに速度を与える
                    self.on_floor = False
                    #ジャンプ中の画像を代入。
                    if self.muki == 0:
                        self.image = Hero.walking_anime[0]
                    elif self.muki == 1:
                        self.image = Hero.walking_anime[2]


        # もし床に居なかったら(もし空中にいたら)重力加速度をy軸方向の速度に加算する。
        if self.on_floor == False:
            self.hero_vel_y += self.GRAVITY

        # もし死亡状態でなかったら、以下を実行する。
        if self.dead_switch == 0:

            # ブロックとx方向の衝突が無かった場合、自座標のxを更新する。
            self.collision_x()
            # ブロックとy方向の衝突が無かった場合、自座標のyを更新する。
            self.collision_y()
            # マップ上のオブジェクトと衝突した場合に行う処理。
            self.collision_objects()
            # マップ上のモンスターと衝突した場合に行う処理。衝突すると死亡してしまうオブジェクトは全て、モンスター扱いとする。
            self.collision_monsters()
            # アイテム「砂時計」との衝突処理。
            self.collision_sunadokei()
            # アイテム「宝箱」との衝突処理。
            self.collision_takarabako()

        self.rect.x = self.hero_pos_x
        self.rect.y = self.hero_pos_y

        # 面間に入ったら、自身(自オブジェクト)を削除する。
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
