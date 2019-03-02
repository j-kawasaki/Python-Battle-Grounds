# coding:utf-8
import math
from Bullet import Bullet
from const import *

class BulletManager():
    MAX_BULLET = 100000

    # ショットの種類
    BULLET_KIND_NOMAL = 0
    BULLET_KIND_BOMB = 10
    BULLET_KIND_GRENADE = 20
    BULLET_KIND_SMOKE = 30

    def __init__(self):
        self.bullet_list = []
        self.setting_id = 0

        self.bullet_configurarion = {}
        self.bullet_configurarion[self.BULLET_KIND_NOMAL] = {'damage': BULLET_DAMAGE_NOMAL, 'velocity': BULLET_VELOCITY_NOMAL, 'size': BULLET_SIZE_NOMAL}
        self.bullet_configurarion[self.BULLET_KIND_BOMB] = {'damage': BULLET_DAMAGE_BOMB, 'velocity': BULLET_VELOCITY_BOMB, 'size': BULLET_SIZE_BOMB}


    def create_bullet(self, player_id, team_id, bullet_kind,  x, y, direction):
        self.setting_id = self.setting_id%self.MAX_BULLET
        new_bullet = Bullet(player_id, team_id, bullet_kind, self.setting_id, x, y, direction, self.bullet_configurarion[bullet_kind]['velocity'], self.bullet_configurarion[bullet_kind]['damage'], self.bullet_configurarion[bullet_kind]['size'])
        self.bullet_list.append(new_bullet)
        self.setting_id += 1


    def delete_bullet(self,bullet):
        self.bullet_list.remove(bullet)


    def update(self):
        for b in self.bullet_list:
            b.update()
            magin = 50
            if b.x < -magin or FIELD_WIDTH+magin < b.x or b.y < -magin or FIELD_HEIGHT+magin < b.y:
                self.delete_bullet(b)
                continue


if __name__ == '__main__':
    print('test')