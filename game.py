import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen, get_win_info
import time
import random
from game_util import *
from time import sleep

def press(key_list):
	for key in key_list:
		pyautogui.keyDown(key)
		pyautogui.keyUp(key)



class Rotmg(object):
	def __init__(self):
		win_location = get_win_info()
		self.win_location = (win_location[0]+8, win_location[1]+51, win_location[2]-10, win_location[3]-10)
		self.last_tp_name = ''
		self.training_state = False
		self.useless = 1
		self.get_who = False
		self.tp_num = 20
	def step(self, action, prev_hp, prev_fame):
		if self.useless % 200 == 0:
			#check_who()
			#self.get_who=True
			pass


		reward = -0.5 #reward changes based on how many red pixs in minimap
		terminal = False
		
		self.perform_action(action)
		hp, frame, fame= self.get_current()

		print('hp value is ', hp)
		if hp<25:
			self.imdead()
			reward = -1


		if self.get_who:
			name = get_player_name(frame)
			if len(name) > 15:
				self.useless = int(self.tp_num-self.tp_num*0.5)
			tp_to_player(name)
			self.last_tp_name = name
			self.get_who = False

		if fame != prev_fame: # there is a change in exp
			if fame < prev_fame:
				reward = 1
			else:
				reward = (fame - prev_fame)/100
		if hp < prev_hp:
			temp_reward = (hp - prev_hp)/100
			if (reward + temp_reward) < -1:
				reward = -1
			else:
				reward += temp_reward
		if hp < 30:
			pyautogui.hotkey('ctrl')
			reward = -1
			terminal = True
			time.sleep(4)
			self.to_realm()

		if reward == -0.5:
			self.useless+=1
		else:
			self.useless = 1

		print('useless value is ', self.useless)


		return frame, reward, terminal, hp, fame
	def imdead(self):
		print('imdead')
		time.sleep(5)
		pyautogui.click(x=self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), y=self.win_location[3]-40)
		time.sleep(1)
		pyautogui.click(x=self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), y=self.win_location[3]-40)
		time.sleep(5)
		pyautogui.click(x=self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), y=self.win_location[3]-40)
		time.sleep(5)
		pyautogui.click(x=self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), y=self.win_location[1]+100)
		time.sleep(5)
		pyautogui.click(x=self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), y=self.win_location[3]-40)
		time.sleep(1)
		watch_done(self.win_location)

		print('im in nexus')



	def reset(self):
		self.to_nexus()
		self.to_realm()

	def to_nexus(self):
		pyautogui.moveTo(self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), self.win_location[3]-35)
		for i in range(3):
			pyautogui.click()
			time.sleep(3)
		pyautogui.moveTo(self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), self.win_location[1]+150)
		pyautogui.click()
		time.sleep(3)
		pyautogui.moveTo(self.win_location[0]+((self.win_location[2] - self.win_location[0])/2), self.win_location[3]-35)
		pyautogui.click()
		time.sleep(4)

	def to_realm(self):
		print('gonig towards realm')
		toward_realm(self.win_location)
		sleep(4)
		print('im completed')
		pyautogui.moveTo(self.win_location[0]+((self.win_location[2] - self.win_location[0])/2)-100, self.win_location[1]+((self.win_location[3]-self.win_location[1])/2)-100)
		pyautogui.keyDown('i')
		pyautogui.keyUp('i')
	def is_over(self, gray):
		#if nexus or died rewards decrease, return rewards
		pass
	def check_location(self):
		pass
	def perform_action(self, action):
		if action[0] == 1: #q pressed
			press('q')
		elif action[1] == 1:
			press('w')
		elif action[2] == 1:
			press('e')
		elif action[3] == 1:
			press('a')
		elif action[4] == 1:
			press('s')
		elif action[5] == 1:
			press('d')
		elif action[6] == 1:
			key_values = 'qw'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[7] == 1:
			key_values = 'qa'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[8] == 1:
			key_values = 'qd'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[9] == 1:
			key_values = 'qs'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[10] == 1:
			key_values = 'ew'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[11] == 1:
			key_values = 'ea'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[12] == 1:
			key_values = 'ed'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[13] == 1:
			key_values = 'es'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[14] == 1:
			key_values = 'wa'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[15] == 1:
			key_values = 'wd'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[16] == 1:
			key_values = 'sa'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])
		elif action[17] == 1:
			key_values = 'sd'
			pyautogui.keyDown(key_values[0])
			pyautogui.keyDown(key_values[1])
			pyautogui.keyUp(key_values[0])
			pyautogui.keyUp(key_values[1])

		

	def get_current(self):
		is_black = False
		is_completed = False
		while True:
			screen = np.array(grab_screen(region=self.win_location), dtype='uint8')
			frame = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
			game_win, map_win, fame_level, hp_level, mana_level = process_game_frame(frame)
			try:
				prev_hp = get_hp(hp_level)
				prev_fame = get_fame(fame_level)
				if is_black:
					is_black = False
					time.sleep(3)
					is_completed = True
					continue
				if is_completed: #if entered
					print('i press controlled')
					pyautogui.hotkey('ctrl')
					time.sleep(4)
					self.to_realm()
				break
			except ValueError as e:
				print('im enter')
				is_black = True
				
				

		return prev_hp, game_win, prev_fame

		


if __name__=="__main__":
	action = [0,0,0,0,0,0,1]
	game = Rotmg()
	game.imdead()


