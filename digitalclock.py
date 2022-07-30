import numpy as np 
import cv2 
from time import sleep 
from datetime import datetime
import sys
from itertools import cycle

colors=cycle([[0,0,255],[0,255,0],[255,255,255]])
color=next(colors)
#original bars
left=np.array([[50,50],[60,40],[70,50],[70,130],[60,140],[50,130],[50,50]])
right=np.array([[160,50],[170,40],[180,50],[180,130],[170,140],[160,130],[160,50]])
hori=np.array([[75,45],[65,35],[75,25],[155,25],[165,35],[155,45],[75,45]])

sides=[left,right,hori]
add_one_below = lambda x: [x[0],x[1]+110]
add_one_side = lambda x:[x[0]+160,x[1]]
add_one_side2 = lambda x:[x[0]+185,x[1]]

#we create the space for the first digit
b1=np.array(list(map(add_one_below,left)))
b2=np.array(list(map(add_one_below,right)))
v1=np.array(list(map(add_one_below,hori)))
v2=np.array(list(map(add_one_below,v1)))
sides.extend([b1,b2,v1,v2])

#we create the space for the second digit 
second_left=np.array(list(map(add_one_side,left)))
second_right=np.array(list(map(add_one_side,right)))
second_hori=np.array(list(map(add_one_side,hori)))
second_b1=np.array(list(map(add_one_below,second_left)))
second_b2=np.array(list(map(add_one_below,second_right)))
second_v1=np.array(list(map(add_one_below,second_hori)))
second_v2=np.array(list(map(add_one_below,second_v1)))
sides.extend([second_left,second_right,second_hori,second_b1,second_b2,second_v1,second_v2])

#third digit
third_left=np.array(list(map(add_one_side2,second_left)))
third_right=np.array(list(map(add_one_side2,second_right)))
third_hori=np.array(list(map(add_one_side2,second_hori)))
third_b1=np.array(list(map(add_one_below,third_left)))
third_b2=np.array(list(map(add_one_below,third_right)))
third_v1=np.array(list(map(add_one_below,third_hori)))
third_v2=np.array(list(map(add_one_below,third_v1)))
sides.extend([third_left,third_right,third_hori,third_b1,third_b2,third_v1,third_v2])

#final

forth_left=np.array(list(map(add_one_side,third_left)))
forth_right=np.array(list(map(add_one_side,third_right)))
forth_hori=np.array(list(map(add_one_side,third_hori)))
forth_b1=np.array(list(map(add_one_below,forth_left)))
forth_b2=np.array(list(map(add_one_below,forth_right)))
forth_v1=np.array(list(map(add_one_below,forth_hori)))
forth_v2=np.array(list(map(add_one_below,forth_v1)))

sides.extend([forth_left,forth_right,forth_hori,forth_b1,forth_b2,forth_v1,forth_v2])

#lets create the digital board now
#(400,750)
table=np.zeros((300,750,3),dtype=np.uint8)
for i in range(table.shape[0]):
	for j in range(table.shape[1]):
		table[i,j]=[97,127,132]
for i in sides:
	cv2.fillPoly(table,pts=[i],color=[97,127,132])#color=(15,15,15)
cv2.circle(table,(368,130),9,[0,0,0],-1)
cv2.circle(table,(368,160),9,[0,0,0],-1)


enum1={"1":left,"2":hori,"3":right,"4":v1,"5":b1,"6":v2,"7":b2}
enum2={"1":second_left,"2":second_hori,"3":second_right,"4":second_v1,"5":second_b1,"6":second_v2,"7":second_b2}
enum3={"1":third_left,"2":third_hori,"3":third_right,"4":third_v1,"5":third_b1,"6":third_v2,"7":third_b2}
enum4={"1":forth_left,"2":forth_hori,"3":forth_right,"4":forth_v1,"5":forth_b1,"6":forth_v2,"7":forth_b2}
enumerations={"1":enum1,"2":enum2,"3":enum3,"4":enum4}
#which bar to light for every number
numbers={"0":[str(i)for i in [1,2,3,5,6,7]],"1":[str(i) for i in [3,7]],"2":[str(i)for i in [2,3,4,5,6]],"3":[str(i)for i in [2,3,4,7,6]]}
numbers["4"]=[str(i)for i in [1,4,3,7]]
numbers["5"]=[str(i)for i in [2,1,4,7,6]]
numbers["6"]=[str(i) for i in [2,1,4,7,6,5]]
numbers["7"]=[str(i) for i in [2,3,7]]
numbers["8"]=[str(i) for i in [1,2,3,4,5,6,7]]
numbers["9"]=[str(i) for i in [1,2,3,4,6,7]]

#function to change colors when clicked
#def clr(action,x,y,flags,*userdata):
#	global color 
#	if action==cv2.EVENT_LBUTTONDOWN:
#		color=next(colors)
#		cv2.circle(table,(368,130),9,color,-1)
#		cv2.circle(table,(368,160),9,color,-1)
#function to change the board every second
def show(n):
	img=table.copy()
	for j,k in enumerate(n):
		for i in numbers[str(k)]:
			img=cv2.fillPoly(img,pts=[enumerations[str(j+1)][i]],color=[0,0,0])
	cv2.imshow("Press Esc to ... escape (please don't move the window)",img)
	k=cv2.waitKey(1)
	sleep(0.99)
	if k==27:
		sys.exit()
while True:
	#cv2.setMouseCallback("Digital Clock press esc to ... escape",clr)
	answer=input("Press 1 for current time, 2 for countdown or 3 for timer: ")
	if answer=="1":
		while True:
			show("{0:02d}{1:02d}".format(datetime.now().hour,datetime.now().minute))
		break
	elif answer=="2":
		count_minutes=input("Minutes: ")
		count_seconds=input("Seconds: ")
		for i in range(60*int(count_minutes)+int(count_seconds),-1,-1):
			show("{0:02d}{1:02d}".format(*divmod(i,60)))
		print("Time is up!")
		break
	elif answer=="3":
		i=0
		while True:
			show("{0:02d}{1:02d}".format(*divmod(i,60)))
			i+=1
		print("Time: {0} minutes and {1}".format(*divmod(i,60)))
		break
	else:
		sys.exit()