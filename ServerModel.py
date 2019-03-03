# coding:utf-8

import math
from Player import Player
from const import *
from BulletManager import BulletManager
import random
import numpy as np
from numpy import linalg as LA



class ServerModel:

	def __init__(self):
		self.bm = BulletManager()
		self.entire_data = {'players':{}, 'bullets': self.bm.bullet_list}

	def calc_dist(self, a, b):
		return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))

	def set_init_data(self, new_player_data):
		self.entire_data['players'][new_player_data.player_id] = new_player_data

	def delete_player(self, player_id):
		if player_id in self.entire_data['players'].keys():
			self.entire_data['players'].pop(player_id)

	def update_player_data(self, received_data):
		player_id = received_data['player_id']
		if player_id in self.entire_data['players'].keys():
			player = self.entire_data['players'][player_id]
			player.update(received_data)
		else:
			print("[LOG] Invalid Player ID")
#			exit()


	def update_bullet_data(self):
		self.bm.update()


	def dumps_all_data(self, received_data):
		sense_data = {'sight':{}, 'hearing':{}, 'own': None}
		player_id = received_data['player_id']
		# プレイヤーIDが登録がのものだったら，空のデータを返して終了
		if player_id not in self.entire_data['players'].keys():
			return sense_data
		# 注目するプライヤーを決定
		player = self.entire_data['players'][player_id]

		sense_data['sight'] = self.dumps_sight_data(player)
		sense_data['own'] = player.dumps_player_data()
		return sense_data


	def dumps_sight_data(self, player):
		sight_data = {'enemies':[], 'bullets':[]}
		# 自分以外の全プレイヤーについて
		for other in self.entire_data['players'].values():
			if other.player_id != player.player_id:
				relative_distance = self.calc_dist(other, player)
				relative_direction = math.atan2(other.y - player.y, other.x - player.x) - player.direction # 自分の向きと他のプレイヤーのいる向きの差
				# もし他のプレイヤーが中心視野内に入っているならば
				if relative_distance < PLAYER_SIGHT_RANGE and abs(relative_direction) < PLAYER_SIGHT_CENTRAL_ANGLE:
					enemy = {}
					enemy['player_id'] = other.player_id
					enemy['direction'] = relative_direction
					enemy['distance'] = relative_distance
					enemy['relative_x'] = relative_distance * math.cos(relative_direction)
					enemy['relative_y'] = relative_distance * math.sin(relative_direction)
					sight_data['enemies'].append(enemy)
				# もし他のプレイヤーが周辺視野内に入っているならば
				elif relative_distance < PLAYER_SIGHT_RANGE and abs(relative_direction) < PLAYER_SIGHT_PERIPHERAL_ANGLE:
					enemy = {}
					enemy['player_id'] = other.player_id
					enemy['direction'] = relative_direction + random.uniform(-math.pi/10, math.pi/10) 
					enemy['distance'] = relative_distance + random.uniform(-PLAYER_SIZE, PLAYER_SIZE)
					enemy['relative_x'] = relative_distance * math.cos(relative_direction)
					enemy['relative_y'] = relative_distance * math.sin(relative_direction)
					sight_data['enemies'].append(enemy)

		# 弾について
		for bullet in self.entire_data['bullets']:
			relative_distance = self.calc_dist(bullet, player)
			relative_direction = math.atan2(bullet.y - player.y, bullet.x - player.x) - player.direction # 自分の向きと他のプレイヤーのいる向きの差
			# もし他のプレイヤーが中心視野内に入っているならば
			if relative_distance < PLAYER_SIGHT_RANGE and abs(relative_direction) < PLAYER_SIGHT_CENTRAL_ANGLE:
				b = {}
				b['player_id'] = bullet.player_id
				b['bullet_kind'] = bullet.bullet_kind
				b['direction'] = relative_direction
				b['distance'] = relative_distance
				b['relative_x'] = relative_distance * math.cos(relative_direction)
				b['relative_y'] = relative_distance * math.sin(relative_direction)
				sight_data['bullets'].append(b)
			# もし他のプレイヤーが周辺視野内に入っているならば
			elif relative_distance < PLAYER_SIGHT_RANGE and abs(relative_direction) < PLAYER_SIGHT_PERIPHERAL_ANGLE:
				b = {}
				b['player_id'] = bullet.player_id
				b['bullet_kind'] = bullet.bullet_kind
				b['direction'] = relative_direction + random.uniform(-math.pi/10, math.pi/10) 
				b['distance'] = relative_distance + random.uniform(-PLAYER_SIZE, PLAYER_SIZE)
				b['relative_x'] = relative_distance * math.cos(relative_direction)
				b['relative_y'] = relative_distance * math.sin(relative_direction)
				sight_data['bullets'].append(b)

		return sight_data

#	def update(self, gamedata):
#		self.load_data(gamedata)
#		self.checkCollision()
#		return self.dump_data(gamedata)




	# 全てのプレイヤー，弾の組み合わせについて衝突判定
	def checkCollision(self):
		for player in self.entire_data['players'].values():
			for bullet in self.entire_data['bullets'][:]: #[:]することでforループの中でremoveできる
				# 自分で撃った弾にはあたらない
#				print(bullet)
				if player.player_id != bullet.player_id:
					if self.checkBalletPlayerCollision(player, bullet):
						# 衝突処理
						player.damage += bullet.damage
						self.bm.delete_bullet(bullet)
						continue


	# ある弾とあるプレイヤーが次１ステップのうちに衝突するかどうか
	# 弾のワープに対応するため，1ピクセルづつ動かして検証する（もっと頭いい方法あるはず）
	def checkBalletPlayerCollision(self, player, bullet):
		for i in range(int(bullet.velocity)):
			#print(bullet['direction'])
			tmpx = bullet.x + math.cos(bullet.direction) * i
			tmpy = bullet.y + math.sin(bullet.direction) * i
			dist = self.calc_dist(player, bullet)
			if dist < (PLAYER_SIZE + bullet.size):
				return True
		return False


if __name__ == '__main__' :
	model = ServerModel()
	print("test")