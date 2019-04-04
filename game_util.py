
import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen, get_win_info
import random
import time

def process_game_frame(frame):
	height, width, _ = frame.shape
	#print(frame.shape)
	game_win = frame[:,:int(width*0.74),:]
	map_win = frame[:int(height*0.33),int(width*0.75):,:]
	fame_level = frame[int(height*0.39):int(height*0.41),int(width*0.77):int(width*0.98),:]
	hp_level = frame[int(height*0.43):int(height*0.45),int(width*0.77):int(width*0.98),:]
	mana_level = frame[int(height*0.47):int(height*0.49),int(width*0.77):int(width*0.98),:]

	return game_win, map_win, fame_level, hp_level, mana_level

def get_hp(hp_level):
	try:
		current_hp = np.where(hp_level[6,:,:] == [52, 52, 224])[0][-1]
	except IndexError as e:
		current_hp = 10
	return (current_hp/hp_level.shape[1])*100


def get_mana(mana_level):
	try:
		current_mana = np.where(mana_level[6,:,:] == [244,132,96])[0][-1]
	except IndexError as e:
		current_mana = 10

	return (current_mana/mana_level.shape[1])*100

def get_fame(fame_level):
	try:
		fame_level = cv2.cvtColor(fame_level, cv2.COLOR_RGB2GRAY)
		_, current_fame = cv2.threshold(fame_level,85,255,cv2.THRESH_BINARY)

		fame = np.where(current_fame[6,:]==[255])[0][-1]
		return (fame/fame_level.shape[1])*100

	except IndexError as e:
		print('im not able to get fame result')
		raise ValueError

	





def toward_realm(win_location):
	pyautogui.keyDown('z')
	pyautogui.keyUp('z')
	pyautogui.keyDown('w')
	realm_location = cv2.imread('realm.png', 0)
	location_aq = False #got realm location
	empty=None
	w, h = realm_location.shape
	win_location = (int(win_location[0]+(win_location[2] - win_location[0])*0.75), win_location[1], win_location[2], int(win_location[1]+(win_location[3] - win_location[1])*0.33))
	counter = 0
	screen = np.array(grab_screen(region=win_location), dtype='uint8')
	frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	center = (int(frame.shape[0]/2), int(frame.shape[1]/2))
	while frame.any():
		res = cv2.matchTemplate(frame,realm_location, cv2.TM_SQDIFF)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		min_val = min_val/10000000
		#print(min_val)
		if min_val  < 0.4 and not location_aq:
			#location_aq = realm_location_get(screen, center, 0)
			pyautogui.keyUp('w')
			print('location detected..')
			location_aq = True 
		elif location_aq:

			if counter%15==0:

				seed = random.randrange(0,100)

			empty = realm_location_get(screen, center, seed, empty, True)
			counter+=1
			

		top_left = min_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		cv2.rectangle(frame,top_left, bottom_right, 255, 2)


		#cv2.imshow('output', frame)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
		screen = np.array(grab_screen(region=win_location), dtype='uint8')
		frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	
	



def realm_location_get(frame, center, seed, empty=None,manu=False):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	global_mask = np.zeros((frame.shape[0]+2, frame.shape[1]+2), np.uint8) 

	character_tri_mask = np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
	character_tri_mask[np.where((frame==[255,0,0]).all(axis=2))] = 255
	cv2.floodFill(character_tri_mask,global_mask,center,0)

	global_mask = global_mask[1:-1, 1:-1]

	character_tri_mask[global_mask==1] = 0
	spts = np.where((character_tri_mask==255)) # this is neede ot change color of the frame

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
			

			
			if diff_y > 0:
				pyautogui.keyDown('s')
				pyautogui.keyUp('s')
				empty = 's'
			elif diff_y < 0:
				pyautogui.keyDown('w')
				pyautogui.keyUp('w')
				empty='w'

			if diff_x < 0:
				pyautogui.keyDown('a')
				pyautogui.keyUp('a')
				empty='a'
			elif diff_x >0:
				pyautogui.keyDown('d')
				pyautogui.keyUp('d')
				empty='d'

		except IndexError as e:
			print(e)
			print('entered in realm')
			print(spts)
			if empty:
				pyautogui.keyDown(empty)
				time.sleep(1)
				pyautogui.keyUp(empty)

		pyautogui.keyDown('0')
		pyautogui.keyUp('0')

		return empty