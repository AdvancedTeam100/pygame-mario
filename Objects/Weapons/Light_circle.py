import pygame

import Map


# 魔法の効果：モンスター「死神」を一時的に遠ざける事が出来る。
# 変数light_circle_time は魔法「Light_circle」の効果時間(フレーム数)である。
class Light_circle(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.light_circle_time = 300
        Light_circle.switch == False

    # 1フレーム毎にlight_circle_timeを減少させる、その値が0以下になった場合、自身を消去 / 初期化する。
    def update(self):
        Map.all.move_to_back(self)
        if Light_circle.switch == True:
            self.light_circle_time -= 1

        # Light_circleを敷き、一定時間経過したら。
        if self.light_circle_time <= 0:
            self.kill()
            self.light_circle_time = 300
            Light_circle.switch = False
