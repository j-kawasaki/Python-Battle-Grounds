# coding:utf-8

import tkinter as tk
from const import *
from BulletManager import BulletManager

class ClientView:
	def __init__(self, window, config):
		# ウィンドウの設定
		self.window = window
		self.config = config
		
		self.window.resizable(width=False, height=False)
		self.window.title(f'Shooting Simulator')
#		self.window.geometry(f'{FIELD_WIDTH + LISTBOX_WIDTH}x{FIELD_HEIGHT}')
#		self.window.geometry(f'200x200')
		# 描画領域を作成
		self.canvas = tk.Canvas(self.window, width=CLIENT_FIELD_WIDTH, height=CLIENT_FIELD_HEIGHT)
#		self.canvas.create_rectangle(0, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=BACKGROUND_COLOR)
		self.canvas.pack(side=tk.LEFT)


	# player を画面の中心とした場合の a の画面内座標(左上が 0,0)を計算して返す
	def calc_relative_point(self, relative_x, relative_y):
		x = relative_x + CLIENT_FIELD_WIDTH / 2 
		y = relative_y + CLIENT_FIELD_HEIGHT / 2
		return x, y

	def update(self, player=''):
		# 一旦全て消す
		if player != '':
			self.canvas.delete("all")
			self.canvas.create_rectangle(0, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=BACKGROUND_COLOR)
	#		self.canvas.delete(f'player{self.data["id"]}')
			if 'sight' in player.sense_data:
				self.sight_update(player)
	#		self.bullet_update()
	#		self.message_update()

	def sight_update(self, player=''):
		# 自分を中心に描く			
		self.canvas.create_oval(int(CLIENT_FIELD_WIDTH/2 - PLAYER_SIZE/2), int(CLIENT_FIELD_HEIGHT/2 - PLAYER_SIZE/2), int(CLIENT_FIELD_WIDTH/2 + PLAYER_SIZE/2), int(CLIENT_FIELD_HEIGHT/2 + PLAYER_SIZE/2), fill=PLAYER_COLORS[player.player_id])	
		# 他のプレイやーがいるならば描写する
		if 'enemies' in player.sense_data['sight']:
			for enemy in player.sense_data['sight']['enemies']:
				x, y = self.calc_relative_point(enemy['relative_x'], enemy['relative_y'])
				self.canvas.create_oval(int(x-PLAYER_SIZE//2), int(y-PLAYER_SIZE//2), int(x+PLAYER_SIZE//2), int(y+PLAYER_SIZE//2), fill=PLAYER_COLORS[enemy['player_id']])

		if 'bullets' in player.sense_data['sight']:
			for b in player.sense_data['sight']['bullets']:
				x, y = self.calc_relative_point(b['relative_x'], b['relative_y'])
				if b['bullet_kind'] == BulletManager.BULLET_KIND_NOMAL:
					size = BULLET_SIZE_NOMAL
					color = BULLET_COLORS[b['player_id']]
				elif b['bullet_kind'] == BulletManager.BULLET_KIND_BOMB:
					size = BULLET_SIZE_BOMB
					color = BULLET_COLORS[b['player_id']]
				elif b['bullet_kind'] == BulletManager.BULLET_KIND_GRANADE:
					size = BULLET_SIZE_GRANADE
					color = BULLET_COLORS[b['player_id']]
				elif b['bullet_kind'] == BulletManager.BULLET_KIND_SMOKE:
					size = BULLET_SIZE_SMOKE
					color = BULLET_COLOR_SMOKE
				self.canvas.create_oval(int(x-size//2), int(y-size//2), int(x+size//2), int(y+size//2), fill=color)


	def message_update(self):
		textlist = []
		textlist.append(f'You are Player {self.player_id}({PLAYER_COLORS[self.player_id]})')
		textlist.append("------------------------")
		textlist.append(f'Uplink Delay:\t{self.config["uplinkdelay"]} (ms)')
		textlist.append(f'Downlink Delay:\t{self.config["downlinkdelay"]} (ms)')
		textlist.append(f'Manual Mode:\t{self.config["manual"]}')
		textlist.append("------------------------")		
		textlist.append("Name\t\tDamage")
		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in self.data:
				player = self.data[f'player{i}']
				textlist.append(f'Player {player["id"]}({PLAYER_COLORS[i]})\t{player["point"]}')

		self.player_log.set('\n'.join(textlist))

if __name__ == '__main__' :
    print('test')
