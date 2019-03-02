import tkinter as tk
import math
import KeyInput
from const import *
import random
from BulletManager import BulletManager

class Player:

	PLAYER_STATUS_ALIVE = 0
	PLAYER_STATUS_DEAD = 10
	PLAYER_STATUS_RESPAWN = 30

	PLAYER_STATUS_NOMAL_COOL = 50
	PLAYER_STATUS_BOMB_COOL = 55

	PLAYER_MOVE_RUN = 100
	PLAYER_MOVE_WALK = 110
	PLAYER_MOVE_SNEAK = 120
	PLAYER_MOVE_STOP = 130

	# プレイヤーの生成に必要な情報
	# ID：プレイヤー固有のID，0から始まる．ホストやサーバーが決定する
	# x,y：プレイヤーの初期位置
	def __init__(self, client_id, bullet_manager=None):
		self.player_id = client_id
		self.team_id = -1
		self.x = random.randrange(FIELD_WIDTH)
		self.y = random.randrange(FIELD_HEIGHT)
		self.direction =  math.pi*2*10000/random.randrange(10000)
		self.damage = 0
		self.count = 0
		self.status_list = {self.PLAYER_STATUS_RESPAWN : 0, self.PLAYER_STATUS_ALIVE: 0, self.PLAYER_STATUS_NOMAL_COOL: 0, self.PLAYER_STATUS_BOMB_COOL: 0} # 状態管理用辞書リスト
		self.move_flag = self.PLAYER_MOVE_STOP
		self.stamina = PLAYER_MAX_STAMINA
		self.bm = bullet_manager

		self.sense_data = {}


	# 主にクライアントで使われる関数
	def set_received_data(self, received_data):
		if 'own' in received_data:
			player_data = received_data['own']
			self.player_id = player_data['player_id']
			self.team_id = player_data['team_id']
			self.x = player_data['x']
			self.y = player_data['y']
			self.direction = player_data['direction']
			self.damage = player_data['damage']
			self.count = player_data['count']
			self.status_list = player_data['status_list']
			self.move_flag = player_data['move_flag']
			self.stanima = player_data['stamina']
		
		self.sense_data = received_data

	# 主にサーバーで使われる関数
	def dumps_player_data(self):
		data = {'player_id':self.player_id,'team_id':self.team_id,'x':self.x,'y':self.y,'direction':self.direction,'damage':self.damage,'count':self.count,'status_list':self.status_list,'move_flag':self.move_flag, 'stamina':self.stamina}
		return data


	def update(self, received_data):
		self.direction = received_data['direction']
		self.move(received_data)
		self.shoot(received_data)

		for key in self.status_list.keys():
			self.status_list[key] += 1
		self.count += 1


	def shoot(self, received_data):
		if received_data['shoot_nomal']:
			if BULLET_COOLTIME_NOMAL <= self.status_list[self.PLAYER_STATUS_NOMAL_COOL]:
				self.bm.create_bullet(self.player_id, self.team_id, BulletManager.BULLET_KIND_NOMAL, self.x, self.y, self.direction)
				self.status_list[self.PLAYER_STATUS_NOMAL_COOL] = 0
			else:
				self.status_list[self.PLAYER_STATUS_NOMAL_COOL] += 1

		if received_data['shoot_bomb']:
			if BULLET_COOLTIME_BOMB <= self.status_list[self.PLAYER_STATUS_BOMB_COOL]:
				self.bm.create_bullet(self.player_id, self.team_id, BulletManager.BULLET_KIND_BOMB, self.x, self.y, self.direction)
				self.status_list[self.PLAYER_STATUS_BOMB_COOL] = 0
			else:
				self.status_list[self.PLAYER_STATUS_BOMB_COOL] += 1


	def move(self, received_data):
		move_flag = received_data['move_flag']
		direction = received_data['direction']
		if move_flag == self.PLAYER_MOVE_RUN and 0 < self.stamina:
			self.x += PLAYER_VELOCITY_RUN * math.cos(direction)
			self.y += PLAYER_VELOCITY_RUN * math.sin(direction)
			self.stamina -= 2
		elif move_flag == self.PLAYER_MOVE_SNEAK and 0 < self.stamina:
			self.x += PLAYER_VELOCITY_SNEAK * math.cos(direction)
			self.y += PLAYER_VELOCITY_SNEAK * math.sin(direction)
			self.stamina -= 1
		elif move_flag == self.PLAYER_MOVE_STOP:
			self.stamina +=3
		else: #move_flag == self.PLAYER_MOVE_WALK
			self.x += PLAYER_VELOCITY_WALK * math.cos(direction)
			self.y += PLAYER_VELOCITY_WALK * math.sin(direction)
			self.stamina += 1
		if PLAYER_MAX_STAMINA < self.stamina:
			self.stamina = PLAYER_MAX_STAMINA
		if self.stamina < 0:
			self.stamina = 0

		# 壁を超えて反対側に来れるように調整
#		self.x = (self.x + FIELD_WIDTH) % FIELD_WIDTH
#		self.y = (self.y + FIELD_HEIGHT) % FIELD_HEIGHT

		# 壁を超えて進めないように処理
		if self.x > FIELD_WIDTH:
			self.x = FIELD_WIDTH
		if self.x < 0:
			self.x = 0
		if self.y > FIELD_HEIGHT:
			self.y = FIELD_HEIGHT
		if self.y < 0:
			self.y = 0

'''
	def shoot(self):
		if self.keyinput.pressTime[KEY_SHOT] > 0:
			if self.cooltime > SHOOT_COOLTIME:
				# マウスが向いている方向の角度を取得
				theta = self.mouseDirection()
				theta_count = int(theta/(2*math.pi/10000))

				# <ShotBullet>のイベントを生成する，ユーザーID，発射方向を追加で載せる
				# state,x,y,timeの本来の使いみちは違うが苦肉の策として使用する（誰かイベントハンドラ自作して）
				# このイベントはBulletManagerで受理される		
				# state: プレイヤーID
				# x, y: プレイヤーの座標 
				# time: 発射方向(tan/(2pi/10000))
	 			# 仮想イベントは二重括弧でくくらないとエラーがでる
				self.window.event_generate('<<ShootBullet>>', state=self.id, x=self.x, y=self.y, time=theta_count)
				self.cooltime = 0
			else:
				self.cooltime += 1
'''



if __name__ == '__main__' :
	Player.create_init_data(0)
	print('test')