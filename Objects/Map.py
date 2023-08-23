import pygame
from pygame.locals import *

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

from Main import PyMain

SCR_RECT = Rect(0, 0, 1200, 750)
class Map:



    def __init__(self): 

        Map.GS = 50
        # スプライトグループを生成。
        Map.all = pygame.sprite.LayeredUpdates()
        Map.blocks = pygame.sprite.Group()
        self.blocksm = pygame.sprite.Group()
        Map.blocksw = pygame.sprite.Group()
        Map.monsters = pygame.sprite.Group()
        Map.objects = pygame.sprite.Group()
        Map.suna_dokei = pygame.sprite.Group()
        Map.takarabako = pygame.sprite.Group()
        Map.fireball = pygame.sprite.Group()
        Map.light_circle = pygame.sprite.Group()
        self.monster_dead = pygame.sprite.Group()

        # オブジェクト化した場合、右辺で指定したグループに登録される。衝突すると死亡してしまうオブジェクトは全てMap.monstersに入れモンスター扱いとした。
        Hero.containers = Map.all
        Meter.containers = Map.all
        Blockm.containers = Map.all, Map.blocks
        Waku_Block.containers = Map.all, Map.blocks, Map.blocksw
        Block.containers = Map.all, Map.blocks
        Ghost.containers = Map.all, Map.monsters
        Shinigami.containers = Map.all, Map.monsters
        Sparkball.containers = Map.all, Map.monsters
        
        Rabbit.containers = Map.all, Map.monsters
        Rabbit_fireball.containers = Map.all, Map.monsters

        FireBall.containers = Map.all, Map.fireball
        Light_circle.containers = Map.all, Map.light_circle
        Monster_dead.containers = Map.all, self.monster_dead
        Key.containers = Map.all, Map.objects
        SunaDokei.containers = Map.all, Map.suna_dokei
        Drop_SunaDokei.containers = Map.all, Map.suna_dokei
        Takarabako.containers = Map.all, Map.takarabako
        Drop_Takarabako.containers = Map.all, Map.takarabako
        Door.containers = Map.all, Map.objects
        Needle.containers = Map.all, Map.monsters
        Gargoyle.containers = Map.all, Map.monsters
        Gargoyle_flame.containers = Map.all, Map.monsters
        Kishi.containers = Map.all, Map.monsters
        Lich.containers = Map.all, Map.monsters
        Lich_fireball.containers = Map.all, Map.monsters

        self.surface = pygame.Surface((19*Map.GS + 250, 15*Map.GS)).convert()
        self.sysfont = pygame.font.SysFont(None, 30)

    # ブロック及び、アイテムをオブジェクト化する関数。
    @classmethod
    def load(cls):
        Map.all.remove(Map.blocks)
        Map.blocks.empty()

        # マップからスプライトを作成
        for i in range(15):
            for j in range(19):
                if Map.men[i][j] == 1:
                    Waku_Block((j*Map.GS, i*Map.GS))
                elif Map.men[i][j] == 2:
                    Blockm((j*Map.GS, i*Map.GS))
                elif Map.men[i][j] == 3:
                    Block((j*Map.GS, i*Map.GS))
                elif Map.men[i][j] == 4:
                    Door((j*Map.GS, i*Map.GS))
                elif Map.men[i][j] == 5:
                    Needle((j*Map.GS, i*Map.GS))

        for i in range(15):
            for j in range(19):
                if Map.item[i][j] == 1:
                    Key((j*Map.GS, i*Map.GS))
                elif Map.item[i][j] == 2:
                    SunaDokei((j*Map.GS, i*Map.GS))
                elif Map.item[i][j] == 3:
                    Takarabako((j*Map.GS, i*Map.GS))

    # 各面のブロック、アイテムの並びの格納。及び、各面に登場するモンスターをオブジェクト化する関数。
    @classmethod
    def men_data(cls):
        if PyMain.men == 1:
            
            Map.men = ([
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
                [1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
                [1,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,2,0,2,0,2,0,2,0,2,0,2,0,2,0,0,0,0,1],
                [1,2,5,2,5,2,5,2,5,2,5,2,5,2,0,0,0,0,1],
                [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ])

            Map.item = ([
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,3,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ])
            Ghost((500,500),0,2)
            Ghost((500,650),0,2)
            # Gargoyle((50,150),0)
            # Gargoyle((850,150),1)
            Kishi((300,100))
            Meter((1000,320))
            # Lich((50,50))
            # Shinigami((200,200),2)
            Sparkball((50,200),2,3)
            Sparkball((500,665),2,2)
            # Rabbit((500,100),Map.fireball)
            # Drop_Takarabako((100,100))

        elif PyMain.men == 2:
            Map.men = ([
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,2,0,0,2,0,0,2,2,0,0,2,0,0,2,0,2,2,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,5,5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5,1],
                [1,2,2,2,2,2,2,2,2,2,2,2,2,2,3,2,2,2,1],
                [1,0,0,0,0,0,2,0,0,0,0,0,2,2,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,2,2,1],
                [1,4,0,0,0,0,2,0,0,2,0,0,2,0,0,0,0,0,1],
                [1,2,0,0,0,0,2,0,0,0,0,0,2,0,2,2,0,0,1],
                [1,2,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,2,5,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ])

            Map.item = ([
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ])


            Sparkball((50,450),2,0)
            Sparkball((200,200),2,0)
            Sparkball((400,200),2,0)
            #Sparkball((500,500),2,0)
            Sparkball((350,450),2,0)
            Sparkball((700,600),2,0)

            Kishi((500,200))
            Ghost((400,200),0,2)
            Ghost((100,500),0,2)

        elif PyMain.men == 3:
            Map.men = ([
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,2,2,2,0,2,2,0,2,2,0,2,2,0,2,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,5,5,5,0,5,0,0,5,0,0,5,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ])

            Map.item = ([
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
                [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ])

            Sparkball((500,465),2,2)
            Sparkball((500,350),2,2)
            # Lich((500,500))
            # Sparkball((750,500),2,1)
            # Shinigami((300,300),2)

#------------------------------------------------------------

        # 三面
        elif PyMain.men == 4:
            Map.men = ([
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ])

            Map.item = ([
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
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

            Rabbit((500,130),Map.fireball)
            Meter((1000,320))
            
#------------------------------------------------------------


    # allに登録されているオブジェクトのupdate関数を一斉に呼び出す。データ上の位置更新。
    def update(self):
        Map.all.update()

    def draw(self,screen):
        # statusにより分岐。描画処理。status 0 はタイトル画面。
        if PyMain.status == 0:
            self.surface.fill((0,0,0))
            title = self.sysfont.render("GAME_TITLE", True, (255,255,255))
            first_stage_text = self.sysfont.render("FIRST_STAGE", True, (255,255,255))
            # first_stage_text.set_alpha(100,0)
            second_stage_text = self.sysfont.render("SECOND_STAGE", True, (255,255,255))
            third_stage_text = self.sysfont.render("THIRD_STAGE", True, (255,255,255))
            fourth_stage_text = self.sysfont.render("FOURTH_STAGE", True, (255,255,255))
            maru = self.sysfont.render("*", True, (255,255,255))
            screen.blit(self.surface, (0,0), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(title, (200,200), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(first_stage_text, (200,300), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(second_stage_text, (200,340), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(third_stage_text, (200,380), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(fourth_stage_text, (200,420), (0,0,SCR_RECT.width, SCR_RECT.height))

            if PyMain.stage_select == 1:
                screen.blit(maru, (150,300), (0,0,SCR_RECT.width, SCR_RECT.height))
            elif PyMain.stage_select == 2:
                screen.blit(maru, (150,340), (0,0,SCR_RECT.width, SCR_RECT.height))
            elif PyMain.stage_select == 3:
                screen.blit(maru, (150,380), (0,0,SCR_RECT.width, SCR_RECT.height))
            elif PyMain.stage_select == 4:
                screen.blit(maru, (150,420), (0,0,SCR_RECT.width, SCR_RECT.height))

        # status 1 はゲーム画面
        elif PyMain.status == 1:            
            self.surface.fill((0,0,0))
            Map.all.draw(self.surface)
            self.life_text = self.sysfont.render("Life",True,(255,255,255))
            self.score_text= self.sysfont.render("Score",True,(255,255,255))
            self.zanki_text= self.sysfont.render("Zanki",True,(255,255,255))
            self.high_score_text= self.sysfont.render("High_Score",True,(255,255,255))
            self.magical_power_text = self.sysfont.render("Magical_power", True, (255,255,255))

            self.life_value = self.sysfont.render(str(PyMain.life),True,(255,255,255))
            self.score_value = self.sysfont.render(str(PyMain.score),True,(255,255,255))
            self.zanki_value = self.sysfont.render(str(PyMain.zanki),True,(255,255,255))
            self.high_score_value = self.sysfont.render(str(PyMain.high_score),True,(255,255,255))

            screen.blit(self.surface, (0,0), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(self.life_text,(1000,90))
            screen.blit(self.life_value,(1000,110))

            screen.blit(self.score_text,(1000,160))
            screen.blit(self.score_value,(1000,180))

            screen.blit(self.zanki_text,(1000,230))
            screen.blit(self.zanki_value,(1000,250))

            screen.blit(self.magical_power_text,(1000,300))

            screen.blit(self.high_score_text,(1000,400))
            screen.blit(self.high_score_value,(1000,420))

        # リトライ
        elif PyMain.status == 2:
            self.surface.fill((0,0,0))
            men_aida_text3 = self.sysfont.render("RETRY", True, (255,255,255))
            screen.blit(self.surface, (0,0), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(men_aida_text3, (200,200), (0,0,SCR_RECT.width, SCR_RECT.height))

        #ゲームオーバー
        elif PyMain.status == 3:
            self.surface.fill((0,0,0))
            men_aida_text4 = self.sysfont.render("GAME_OVER", True, (255,255,255))
            screen.blit(self.surface, (0,0), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(men_aida_text4, (200,200), (0,0,SCR_RECT.width, SCR_RECT.height))

        # ステージクリア        
        elif PyMain.status == 4:
            self.surface.fill((0,0,0))
            men_aida_text5 = self.sysfont.render(str(PyMain.men) + "STAGE_CLEAR", True, (255,255,255))
            screen.blit(self.surface, (0,0), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(men_aida_text5, (200,200), (0,0,SCR_RECT.width, SCR_RECT.height))

        # ゲームクリア
        elif PyMain.status == 5:
            self.surface.fill((0,0,0))
            men_aida_text6 = self.sysfont.render("GAME_CLEAR", True, (255,255,255))
            screen.blit(self.surface, (0,0), (0,0,SCR_RECT.width, SCR_RECT.height))
            screen.blit(men_aida_text6, (200,200), (0,0,SCR_RECT.width, SCR_RECT.height))
