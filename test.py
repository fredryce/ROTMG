import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen, get_win_info
import time
import random


	



def count_down(count):
	for i in range(count,0,-1):
		print(i)
		time.sleep(1)




def realm_location_get(frame, center, seed, manu=False):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	global_mask = np.zeros((frame.shape[0]+2, frame.shape[1]+2), np.uint8) 

	character_tri_mask = np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
	character_tri_mask[np.where((frame==[255,0,0]).all(axis=2))] = 255
	cv2.floodFill(character_tri_mask,global_mask,center,0)

	global_mask = global_mask[1:-1, 1:-1]

	character_tri_mask[global_mask==1] = 0
	spts = np.where((character_tri_mask==255)) # this is needed to change color of the frame

	temp = global_mask.copy()
	#print(temp)
	temp[global_mask==1]=255

	random.seed(seed)
	rand_val = random.randint(0, spts[0].shape[0])

	#show_frame(temp)
	#print(spts)
	if manu:
		try:
			diff_y = spts[0][rand_val] - center[0]
			diff_x = spts[1][rand_val] - center[1]

			#print('im at center {}, my goal is {}'.format(center,(spts[0][0], spts[1][0])))
			#print(diff_y)
			pyautogui.keyDown('0')
			pyautogui.keyUp('0')

			
			if diff_y > 0:
				pyautogui.keyDown('s')
				pyautogui.keyUp('s')
			elif diff_y < 0:
				pyautogui.keyDown('w')
				pyautogui.keyUp('w')

			if diff_x < 0:
				pyautogui.keyDown('a')
				pyautogui.keyUp('a')
			elif diff_x >0:
				pyautogui.keyDown('d')
				pyautogui.keyUp('d')
			return False
		except IndexError:
			print('entered in realmw')
			print(spts)
			return True
 
def locate_realm(screen, center):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	global_mask = np.zeros((frame.shape[0]+2, frame.shape[1]+2), np.uint8) 
	character_tri_mask = np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
	character_tri_mask[np.where((frame==[255,0,0]).all(axis=2))] = 255
	cv2.floodFill(character_tri_mask,global_mask,center,0)
	global_mask = global_mask[1:-1, 1:-1] #contins all vlues for the player
	while frame.any


def toward_realm(win_location):
	pyautogui.keyDown('z')
	pyautogui.keyUp('z')
	pyautogui.keyDown('w')
	realm_location = cv2.imread('realm.png', 0)
	location_aq = False #got realm location
	w, h = realm_location.shape
	win_location = (int(win_location[0]+(win_location[2] - win_location[0])*0.75), win_location[1], win_location[2], int(win_location[1]+(win_location[3] - win_location[1])*0.33))
	counter = 0

	screen = np.array(grab_screen(region=win_location), dtype='uint8')
	frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	center = (int(frame.shape[0]/2), int(frame.shape[1]/2))

	while True:
		res = cv2.matchTemplate(frame,realm_location, cv2.TM_SQDIFF)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		min_val = min_val/10000000
		print(min_val)
		if min_val  < 0.7 and not location_aq:
			#location_aq = realm_location_get(screen, center, 0)
			pyautogui.keyUp('w')
			print('location detected..')
			locate_realm(frame, center)
			location_aq = True 

		




		#cv2.imshow('output', frame)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
		screen = np.array(grab_screen(region=win_location), dtype='uint8')
		frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	
	

	
	


win_location = get_win_info()
win_location = (win_location[0]+8, win_location[1]+100, win_location[2]-10, win_location[3]-10)
count_down(4)
toward_realm(win_location)
