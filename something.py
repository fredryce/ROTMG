import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen, get_win_info
import time
import random


def realm_location_get(frame, center, seed, manu=False, win_location):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	global_mask = np.zeros((frame.shape[0]+2, frame.shape[1]+2), np.uint8) 

	character_tri_mask = np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
	character_tri_mask[np.where((frame==[255,0,0]).all(axis=2))] = 255
	cv2.floodFill(character_tri_mask,global_mask,center,0)

	global_mask = global_mask[1:-1, 1:-1]

	character_tri_mask[global_mask==1] = 0
	spts = np.where((character_tri_mask==255))

	selSpty = spts[0][rand_val]
	selSptx = spts[1][rand_val]
	
	diff_y = selSpty - center[0]
	diff_x = selSptx - center[1]

	print('x:' + str(diff_x) + '  y:' + str(diff_y))

	pyautogui.keyDown('s')
	pyautogui.keyUp('s')

	print('x:'+diff_x+'  y:'+diff_y)

win_location = get_win_info()
win_location = (win_location[0]+8, win_location[1]+51, win_location[2]-10, win_location[3]-10)
toward_realm(win_location)