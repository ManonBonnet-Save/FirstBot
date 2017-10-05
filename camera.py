import sys, time
import numpy as np
import cv2

        
color = 'black'
if len(sys.argv) > 1:
        color = sys.argv[1]
range_dict = {'red':([17,15,100],[50,56,200]), 'white':([170,170,170], [255,255,255]), 'black':([0,0,0],[90,90,90])}
cap = cv2.VideoCapture(0)
cap.set(4, 480)
cap.set(3, 640)
lines = None

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
ly = len(frame)
lx = len(frame[0])
l_buff = int(0.15*lx)
l2_buff = int(l_buff/2)
enough_color = 200
count = 0
nby_buffs = 4

while True:
	ret, frame = cap.read()
	if not ret:
		count += 1
		print('['+str(count)+'] error')
		continue

	frame = cv2.GaussianBlur(frame,(5,5),0)
	lower = np.array(range_dict[color][0], dtype = 'uint8')
	upper = np.array(range_dict[color][1], dtype = 'uint8')
	mask = cv2.inRange(frame, lower, upper)
	#mask = cv2.erode(mask, np.ones((8,8), np.uint8), iterations = 1)
       	#mask = cv2.Canny(mask, 100, 200)
	#cv2.HoughLinesP(mask, 10, np.pi/60, 10, lines, 500)
	
	x0, y0 =(int(lx/2)-l2_buff, ly-l_buff)
        buff_list = []
        for i in range(nby_buffs):
                buff_failed = True
                buff_exit = False
                x_buff = x0
                y_buff = y0 - i*l_buff
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
                                print('Line not found')
                                buff_failed = True
                                buff_exit = True
                
        cv2.imshow('waouh3', mask)
        for checked_buff in buff_list:
                x_buff = checked_buff[0]
                y_buff = checked_buff[1]
	        cv2.line(frame, (x_buff, y_buff), (x_buff, y_buff+l_buff), (0,255,0),2)
                cv2.line(frame, (x_buff+l_buff, y_buff), (x_buff+l_buff, y_buff+l_buff), (0,255,0),2)


        if buff_list:
                # computes with (0, 0) before the robot, x axis forward, y axis to the left
                regression_y = [int(lx/2) - (e[0]+l2_buff)  for e in buff_list]
                regression_x = [ly - (e[1]+l2_buff)  for e in buff_list]
                print(regression_x)
                print(regression_y)
                poly_var = np.polyfit(regression_x, regression_y, 1)
                if poly_var is not None:
                        poly_a, poly_b = poly_var
                        followed_line = [ (int(poly_b), int(0)), np.arctan(poly_a)]

                        tmp_1 = (int(lx/2) - followed_line[0][0], ly)
                        tmp_2 = (int(lx/2 - followed_line[0][0] - np.sin(followed_line[1])*300), ly -  int(np.cos(followed_line[1])*300))
                        print(followed_line)
                        
                        print(tmp_1, tmp_2)
                        cv2.line(frame, tmp_1, tmp_2, (255,255,0),2)
                else:
                        followed_line = None
                
        else :
                followed_line = None
                
        if followed_line is None:
                print('[\_(:/)_/]] lost... should do some recovering')
        elif followed_line[0][0] > 20:
                if followed_line[1] > 0:
                        print('[ORDER] turn left++')
                else:
                        print('[ORDER] turn left')
        elif followed_line[0][0] < -20:
                if followed_line[1] < 0:
                        print('[ORDER] turn right++')
                else:
                        print('[ORDER] turn right')
        elif abs(followed_line[0][0]) < 20:
                print('[ORDER] continue forward')
        else :
                print('[?????]] wut?')

        '''
	if lines is not None:
		lines = lines[0]
		print(len(lines))
		for e in lines:
			x1 = e[0]
			y1 = e[1]
			x2 = e[2]
			y2 = e[3]
			cv2.line(frame, (x1, y1), (x2, y2), (0,255,0),2)
	'''
	cv2.imshow('waouh', frame)
	key = cv2.waitKey(100)
	if key == ord('q') or key == 1048689:
		break
cap.release()
cv2.destroyAllWindows()
