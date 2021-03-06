import numpy as np
import cv2
import pyautogui
from grabscreen import grab_screen, get_win_info
import time
import random
import pytesseract
import re
from game_util import watch_done
def mouse_cb(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		try:
			print(params[y, x, :])
		except Exception as e:
			print(params[y, x])


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
			

			
			if diff_y > 0:
				pyautogui.keyDown('s')
				time.sleep(0.01*abs(diff_y))
				pyautogui.keyUp('s')
			elif diff_y < 0:
				pyautogui.keyDown('w')
				time.sleep(0.01*abs(diff_y))
				pyautogui.keyUp('w')

			if diff_x < 0:
				pyautogui.keyDown('a')
				time.sleep(0.01*abs(diff_x))
				pyautogui.keyUp('a')
			elif diff_x >0:
				pyautogui.keyDown('d')
				time.sleep(0.01*abs(diff_x))
				pyautogui.keyUp('d')
		except IndexError:
			pass
 
		pyautogui.keyDown('0')
		pyautogui.keyUp('0')

def toward_realm(win_location):
	pyautogui.keyDown('z')
	pyautogui.keyUp('z')
	pyautogui.keyDown('w')
	realm_location = cv2.imread('realm.png', 0)
	location_aq = False #got realm location
	w, h = realm_location.shape
	is_stuck = 0
	win_location = (int(win_location[0]+(win_location[2] - win_location[0])*0.75), win_location[1], win_location[2], int(win_location[1]+(win_location[3] - win_location[1])*0.33))
	#win_location = (win_location[0]+20, win_location[1]+20, win_location[2]-20, win_location[3]-20) #add temp
	counter = 0
	screen = np.array(grab_screen(region=win_location), dtype='uint8')
	frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	center = (int(frame.shape[0]/2), int(frame.shape[1]/2))
	while frame.any():
		#print(frame.any())
		
		res = cv2.matchTemplate(frame,realm_location, cv2.TM_SQDIFF)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		min_val = min_val/10000000
		#print(min_val)
		if min_val  < 0.7 and not location_aq:
			#location_aq = realm_location_get(screen, center, 0)
			pyautogui.keyUp('w')
			print('location detected..')
			location_aq = True 
		elif location_aq:

			if counter%15==0:

				seed = random.randrange(0,100)

			realm_location_get(screen, center, seed, True)
			counter+=1
		else:
			if is_stuck%100 == 0:
				print('im stuck')
				stuck_direction = int((is_stuck/100))
				if stuck_direction > 0:
					if (stuck_direction)%2==0:
						for i in range(stuck_direction):
							pyautogui.keyDown('a')
							pyautogui.keyUp('a')
					else:
						for i in range(stuck_direction):
							pyautogui.keyDown('d')
							pyautogui.keyUp('d')


			is_stuck+=1
	
			

		top_left = min_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		cv2.rectangle(frame,top_left, bottom_right, 255, 2)


		#cv2.imshow('output', frame)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
		screen = np.array(grab_screen(region=win_location), dtype='uint8')
		frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	
	
def check_who():
	pyautogui.keyDown('/')
	pyautogui.keyUp('/')
	pyautogui.typewrite('who')
	pyautogui.keyDown('return')
	pyautogui.keyUp('return')
	time.sleep(1)
def get_player_name(frame):
	player_frame = frame[int(frame.shape[0]*0.94):,:,:]
	
	mask = np.zeros((player_frame.shape[0], player_frame.shape[1]), np.uint8)
	mask[np.where((player_frame==[0,255,255]).all(axis=2))] = 255
	gray = cv2.medianBlur(mask, 3)
	show_frame(mask)
	string_names = pytesseract.image_to_string(mask)
	string_names = ''.join(x for x in string_names if x.isalpha() or x==',')
	name_list = string_names.split(',')
	assert len(name_list) > 0
	index = random.randrange(len(name_list))
	print('teleporting to ', name_list[index])
	print(string_names)
	return name_list[index]

def tp_to_player(name):
	pyautogui.keyDown('/')
	pyautogui.keyUp('/')
	value = 'teleport '+name
	pyautogui.typewrite(value)
	pyautogui.keyDown('return')
	pyautogui.keyUp('return')

def check_dong(game_win, kargs):
	result = []
	game_win = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	#print(kargs)
	for key, value in kargs.items():
		conf = cv2.matchTemplate(game_win,value, cv2.TM_SQDIFF)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(conf)
		min_val = min_val/10000000
		result.append(min_val)

	np_result = np.argmin(np.array(result))
	print(result)
	if result[np_result] > 0.3:
		np_result = 3

	return np_result
	
	


win_location = get_win_info()
win_location = (win_location[0]+8, win_location[1]+50, win_location[2]-10, win_location[3]-10)
prev_hp = 99
count_down(0)
print(win_location)

next_image = cv2.imread('next.png', 0)
pet_yard = cv2.imread('petyard.png', 0)


#toward_realm(win_location)
#cv2.namedWindow('output')
#cv2.setMouseCallback('output',mouse_cb)
nexus = False
nexusing = False
tp=False
check=False
while True:
	screen = np.array(grab_screen(region=win_location), dtype='uint8')
	frame = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
	game_win, map_win, fame_level, hp_level, mana_level = process_game_frame(frame)
	if not nexus:
		
		hp = get_hp(hp_level)
		mana = get_mana(mana_level)
		print('HP:{} mana:{}'.format(hp, mana))
		if hp < 30:
			if check_special(hp_level):

				print("Entering Dongen")
				watch_done(win_location)
				time.sleep(2)

			else:
				print('dying')
				pyautogui.hotkey('ctrl')
				nexusing = True
	else:
		#toward_realm(win_location)
		nexus = False
		nexusing=False
	#frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	#cv2.imshow('output', frame)
	cv2.setMouseCallback('output',mouse_cb, frame)
	

	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
