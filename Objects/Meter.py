import pygame
from pygame.locals import *

from Main import PyMain

# 魔力メータークラス。
class Meter(pygame.sprite.Sprite):
    # メーター
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        if PyMain.meter_count <= 520:
            PyMain.meter_count += 1

        if PyMain.meter_count >= 0 and PyMain.meter_count < 50:
            self.image = Meter.meter[0]
        elif PyMain.meter_count > 50 and PyMain.meter_count < 100:
            self.image = Meter.meter[1]
        elif PyMain.meter_count > 100 and PyMain.meter_count < 150:
            self.image = Meter.meter[2]
        elif PyMain.meter_count > 150 and PyMain.meter_count < 200:
            self.image = Meter.meter[3]
        elif PyMain.meter_count > 200 and PyMain.meter_count < 250:
            self.image = Meter.meter[4]
        elif PyMain.meter_count > 250 and PyMain.meter_count < 300:
            self.image = Meter.meter[5]
        elif PyMain.meter_count > 300 and PyMain.meter_count < 350:
            self.image = Meter.meter[6]
        elif PyMain.meter_count > 350 and PyMain.meter_count < 400:
            self.image = Meter.meter[7]
        elif PyMain.meter_count > 400 and PyMain.meter_count < 450:
            self.image = Meter.meter[8]
        elif PyMain.meter_count > 450 and PyMain.meter_count < 500:
            self.image = Meter.meter[9]
        elif PyMain.meter_count > 500 and PyMain.meter_count < 550:
            self.image = Meter.meter[10]
            PyMain.shot_switch = 1
        
        if PyMain.status == 2 or PyMain.status == 3 or PyMain.status == 4 or PyMain.status == 5:
            self.kill()
