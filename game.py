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
	def step(self, action, prev_hp, prev_fame):

		reward = -0.1 #reward changes based on how many red pixs in minimap
		terminal = False
		
		self.perform_action(action)
		hp, frame, fame= self.get_current()
		if fame != prev_fame: # there is a change in exp
			reward = 1
		if hp < prev_hp:
			temp_reward = (hp - prev_hp)/100
			if (reward - temp_reward) < -1:
				reward = -1
			else:
				reward = temp_reward
		if hp < 30:
			reward = -1
			terminal = True
			pyautogui.hotkey('ctrl')
			self.reset()
		if reward != -0.1:
			print(reward)


		return frame, reward, terminal, hp, fame

	def reset(self):
		self.to_nexus()
		self.to_realm()

	def to_nexus(self):
		pass
	def to_realm(self):
		sleep(4)
		toward_realm(self.win_location)
		sleep(4)
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
		while True:
			screen = np.array(grab_screen(region=self.win_location), dtype='uint8')
			frame = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
			game_win, map_win, fame_level, hp_level, mana_level = process_game_frame(frame)
			try:
				prev_hp = get_hp(hp_level)
				prev_fame = get_fame(fame_level)
				if is_black:
					is_black = False
					time.sleep(2)
					continue

				break
			except ValueError as e:
				print('im leaving or entering')
				is_black = True

		return prev_hp, game_win, prev_fame

		


if __name__=="__main__":
	action = [0,0,0,0,0,0,1]
	game = Rotmg()
	prev_hp, game_win, prev_fame = game.get_current()
	while True:
		#print(prev_hp, prev_fame)
		frame, reward, terminal, prev_hp, prev_fame = game.step(action,prev_hp, prev_fame)
		print(frame.shape)
		frame =cv2.resize(frame, (80, 80))
		print(frame.shape)
		if reward != -0.1:
			print(reward)


