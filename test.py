import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen, get_win_info
import time

def mouse_cb(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		print(params[y, x, :])


def check_special(hp_level):
	try:
		current_hp = np.where(hp_level[6,:,:] == [0,0,0])[0][-1]
		if current_hp.all():
			return True
	except IndexError:
		pass
	return False

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


def process_game_frame(frame):
	height, width, _ = frame.shape
	#print(frame.shape)
	game_win = frame[:,:int(width*0.74),:]
	map_win = frame[:int(height*0.33),int(width*0.75):,:]
	fame_level = frame[int(height*0.39):int(height*0.41),int(width*0.77):int(width*0.98),:]
	hp_level = frame[int(height*0.43):int(height*0.45),int(width*0.77):int(width*0.98),:]
	mana_level = frame[int(height*0.47):int(height*0.49),int(width*0.77):int(width*0.98),:]

	return game_win, map_win, fame_level, hp_level, mana_level



def count_down(count):
	for i in range(count,0,-1):
		print(i)
		time.sleep(1)
def show_frame(frame):
	cv2.imshow('test_out', frame)


def realm_location_get(frame):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	center = (int(frame.shape[0]/2), int(frame.shape[1]/2))

	
	#spts = np.where((frame==[255,0,0]).all(axis=2))
	character_tri_mask = np.zeros(frame.shape[:-1],np.uint8)
	cv2.floodFill(character_tri_mask,global_mask,center,255, flags=cv2.FLOODFILL_MASK_ONLY) 
	


	return []


def toward_realm(win_location):
	locations = []
	pyautogui.keyDown('z')
	pyautogui.keyUp('z')
	pyautogui.keyDown('w')
	realm_location = cv2.imread('realm.png', 0)

	w, h = realm_location.shape
	
	while True:
		screen = np.array(grab_screen(region=win_location), dtype='uint8')
		frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

		res = cv2.matchTemplate(frame,realm_location, cv2.TM_SQDIFF)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		min_val = min_val/10000000
		print(min_val)
		if min_val  < 0.3:
			locations = realm_location_get(screen)
			break
			

		top_left = min_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		cv2.rectangle(frame,top_left, bottom_right, 255, 2)


		cv2.imshow('output', frame)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
	pyautogui.keyUp('w')
	




win_location = get_win_info()
win_location = (win_location[0]+8, win_location[1]+51, win_location[2]-10, win_location[3]-10)
win_location = (int(win_location[0]+(win_location[2] - win_location[0])*0.75), win_location[1], win_location[2], int(win_location[1]+(win_location[3] - win_location[1])*0.33))
prev_hp = 99
count_down(1)
print(win_location)

cv2.namedWindow('output')
cv2.setMouseCallback('output',mouse_cb)
nexus = True

while True:
	screen = np.array(grab_screen(region=win_location), dtype='uint8')
	frame = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
	global_mask = np.zeros((frame.shape[0]+2, frame.shape[1]+2), np.uint8) 
	center = (int(frame.shape[0]/2)+2, int(frame.shape[1]/2))


	character_tri_mask = np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
	character_tri_mask[np.where((frame==[255,0,0]).all(axis=2))] = 255
	cv2.floodFill(character_tri_mask,global_mask,center,200) 

	global_mask[global_mask==1] = 255
	print(global_mask)
	cv2.imshow('output', global_mask)
	cv2.setMouseCallback('output',mouse_cb, frame)
	

	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
