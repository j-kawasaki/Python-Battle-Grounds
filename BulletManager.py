# coding:utf-8
import math
from Bullet import Bullet
from const import *
import random

class BulletManager():
	MAX_BULLET = 100000

	# ショットの種類
	BULLET_KIND_NOMAL = 0
	BULLET_KIND_BOMB = 10
	BULLET_KIND_GRANADE = 20
	BULLET_KIND_SMOKE = 30

	BULLET_INFO = {}
	BULLET_INFO[BULLET_KIND_NOMAL] = {'damage': BULLET_DAMAGE_NOMAL, 'velocity': BULLET_VELOCITY_NOMAL, 'size': BULLET_SIZE_NOMAL, 'life': BULLET_LIFE_NOMAL}
	BULLET_INFO[BULLET_KIND_BOMB] = {'damage': BULLET_DAMAGE_BOMB, 'velocity': BULLET_VELOCITY_BOMB, 'size': BULLET_SIZE_BOMB, 'life': BULLET_LIFE_BOMB}
	BULLET_INFO[BULLET_KIND_GRANADE] = {'damage': BULLET_DAMAGE_GRANADE, 'velocity': BULLET_VELOCITY_GRANADE, 'size': BULLET_SIZE_GRANADE, 'life': BULLET_LIFE_GRANADE}
	BULLET_INFO[BULLET_KIND_SMOKE] = {'damage': BULLET_DAMAGE_SMOKE, 'velocity': BULLET_VELOCITY_SMOKE, 'size': BULLET_SIZE_SMOKE, 'life': BULLET_LIFE_SMOKE}    

	def __init__(self):
		self.bullet_list = []
		self.setting_id = 0    

	def create_bullet(self, player_id, team_id, bullet_kind,  x, y, direction):
		self.setting_id = self.setting_id%self.MAX_BULLET
		new_bullet = Bullet(player_id, team_id, bullet_kind, self.setting_id, x, y, direction, self.BULLET_INFO[bullet_kind]['velocity'], self.BULLET_INFO[bullet_kind]['damage'], self.BULLET_INFO[bullet_kind]['size'])
		self.bullet_list.append(new_bullet)
		self.setting_id += 1

	def create_granade_bullet(self, parent_bullet):
		x = parent_bullet.x
		y = parent_bullet.y
		player_id = parent_bullet.player_id
		team_id = parent_bullet.team_id
		bullet_kind = self.BULLET_KIND_NOMAL
		# グレネードの弾を出す * 6
		for v in range(6):
			velocity = v * 0.3
			for i in range(16):
				direction = 2 * math.pi / 16 * i
				self.setting_id = self.setting_id%self.MAX_BULLET
				new_bullet = Bullet(player_id, team_id, bullet_kind, self.setting_id, x, y, direction, velocity, self.BULLET_INFO[bullet_kind]['damage'], self.BULLET_INFO[bullet_kind]['size'])
				self.bullet_list.append(new_bullet)
				self.setting_id += 1

	def create_smoke_bullet(self, parent_bullet):
		x = parent_bullet.x
		y = parent_bullet.y
		player_id = parent_bullet.player_id
		team_id = parent_bullet.team_id
		bullet_kind = self.BULLET_KIND_BOMB
		velocity = random.uniform(0.01, 0.3)
		direction = 2 * math.pi / 16 * random.randrange(0,15)
		self.setting_id = self.setting_id%self.MAX_BULLET
		new_bullet = Bullet(player_id, team_id, bullet_kind, self.setting_id, x, y, direction, velocity, 0, BULLET_SIZE_BOMB)
		self.bullet_list.append(new_bullet)
		self.setting_id += 1

	def delete_bullet(self,bullet):
		if bullet in self.bullet_list:
			self.bullet_list.remove(bullet)
		else:
			print("INVALID RWEMOVE")


	def update(self):
		for b in self.bullet_list[:]:
			b.update()
			# グレネードなら周辺に弾をばらまく
			if b.bullet_kind == self.BULLET_KIND_GRANADE:
				if BULLET_LIFE_GRANADE//5 == b.life_time:
					b.velocity = 0
					b.dx = 0
					b.dy = 0
				elif BULLET_LIFE_GRANADE == b.life_time:
					self.create_granade_bullet(b)
					self.delete_bullet(b)

			if b.bullet_kind == self.BULLET_KIND_SMOKE:
				if BULLET_LIFE_SMOKE//5 < b.life_time:
					b.velocity = 0
					b.dx = 0
					b.dy = 0
					self.create_smoke_bullet(b)

			# もしライフタイムを過ぎているならば
			if self.BULLET_INFO[b.bullet_kind]['life'] < b.life_time:
				self.delete_bullet(b)

			# 画面外にいった弾は消す
			magin = 50
			if b.x < -magin or FIELD_WIDTH+magin < b.x or b.y < -magin or FIELD_HEIGHT+magin < b.y:
				self.delete_bullet(b)
				continue


if __name__ == '__main__':
	print('test')