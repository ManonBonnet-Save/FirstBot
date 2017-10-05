import sys, time
import numpy as np
import cv2
from comm_serie import serial_init,serial_close,left,right,forward,backward,stop
        
color = 'black'
if len(sys.argv) > 1:
        color = sys.argv[1]
range_dict = {'red':([0,0,133],[255,132,255]), 'white':([170,170,170], [255,255,255]), 'black':([0,0,0],[100,100,100])}
cap = cv2.VideoCapture(0)
cap.set(4, 240)
cap.set(3, 320)

serial_init()

ret = False
for i in range(5):
        ret, frame = cap.read()
        print(ret)
        cv2.waitKey(100)
        
if i == 4 and not ret:
        print('[ERROR] failed to read cap : re-openning')
        cap.release()
        time.sleep(1)
        cap = cv2.VideoCapture(0)
while not ret:
        print('[ERROR] failed to read cap')
        ret, frame = cap.read()
        cv2.waitKey(100)
#cv2.imshow('frame', frame)
cv2.waitKey(10)

ly = len(frame)
lx = len(frame[0])
l_buff = int(0.15*lx)
l2_buff = int(l_buff/2)
l4_buff = int(l_buff/4)
enough_color = 140
count = 0
nby_buffs = 5

while True:
        ti = time.time()
        print(' > > > loop < < <')
	ret, frame = cap.read()
	if not ret:
		count += 1
		print('['+str(count)+'] error')
		continue
        t1 = time.time()
	#frame = cv2.GaussianBlur(frame,(5,5),0)
	lower = np.array(range_dict[color][0], dtype = 'uint8')
	upper = np.array(range_dict[color][1], dtype = 'uint8')
	mask = cv2.inRange(frame, lower, upper)
	#mask = cv2.erode(mask, np.ones((8,8), np.uint8), iterations = 1)
       	#mask = cv2.Canny(mask, 100, 200)
	print(time.time() -t1)
	x0, y0 =(int(lx/2)-l2_buff, ly-l_buff)
        buff_list = []
        t1 = time.time()
        for i in range(nby_buffs):
                buff_failed = True
                buff_exit = False
                x_buff = x0
                y_buff = y0 - i*l2_buff
                buff_offset = 0
	        buff_side = -1
                while not buff_exit:
                        buff = mask[y_buff:y_buff+l_buff, x_buff:x_buff+l_buff]
                        if np.average(buff) > enough_color:
                                buff_exit = True
                                buff_failed = False
                                buff_list += [(x_buff, y_buff)]
                        else:
                                buff_offset += l2_buff
                                buff_side *= -1
                                x_buff += buff_offset * buff_side
                        if  x_buff < 0 or (x_buff + l_buff) > lx:
                                buff_failed = True
                                buff_exit = True
	                

        print(time.time() -t1)
        t1 = time.time()
        for checked_buff in buff_list:
                x_buff = checked_buff[0]
                y_buff = checked_buff[1]
	        cv2.line(mask, (x_buff, y_buff), (x_buff, y_buff+l_buff), (0,255,0),2)
                cv2.line(mask, (x_buff+l_buff, y_buff), (x_buff+l_buff, y_buff+l_buff), (0,255,0),2)

	print(time.time() -t1)
        
        t1 = time.time()
        if buff_list:
                # computes with (0, 0) before the robot, x axis forward, y axis to the left
                regression_y = [int(lx/2) - (e[0]+l2_buff)  for e in buff_list]
                regression_x = [ly - (e[1]+l2_buff)  for e in buff_list]
                poly_var = np.polyfit(regression_x, regression_y, 1)
                if poly_var is not None:
                        poly_a, poly_b = poly_var
                        followed_line = [ (int(poly_b), int(0)), np.arctan(poly_a)]

                        tmp_1 = (int(lx/2) - followed_line[0][0], ly)
                        tmp_2 = (int(lx/2 - followed_line[0][0] - np.sin(followed_line[1])*300), ly -  int(np.cos(followed_line[1])*300))
                        cv2.line(mask, tmp_1, tmp_2, (255,255,0),2)
                else:
                        followed_line = None
                
        else :
                followed_line = None
        print(time.time() -t1)
        t1 = time.time()
        if followed_line is None:
                print('[\_(:/)_/]] lost... should do some recovering')
		backward()
        else:
                dist_from_line = int(followed_line[0][1] / np.sqrt(1+followed_line[0][0]**2))
                dist_from_line = followed_line[0][0]
                angle_with_line = followed_line[1]
                cv2.line(frame, (int(lx/2), ly), (lx/2 - int(np.cos(angle_with_line)*dist_from_line),ly - int(np.cos(angle_with_line)*dist_from_line)), (90,123,250),2)
        	
		ratio=min(abs(angle_with_line*2/np.pi),1)
                
		if angle_with_line < -np.pi/12:
                        print('turn right')
                        right(ratio)
                elif angle_with_line > np.pi/12:
                        print('turn left')
                        left(ratio)
                else:
                        print('forward ')
                        forward()
                
        print(time.time() - t1)
        '''
        t1 = time.time()
	cv2.imshow('mask', mask)
	key = cv2.waitKey(10)
	if key == ord('q') or key == 1048689:
		break
        print(time.time()- t1)
        '''
        print(' freq : '+str(1/(time.time()-ti)))
cap.release()
cv2.destroyAllWindows()
serial_close()
