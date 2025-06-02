import cv2,time
import numpy as np
import os
import h5py
from hand_detector_NN_functions_v1 import forward_prop
hdf = h5py.File(r'C:\Users\anike\Desktop\Deep Learning Project 1\h5_data.h5','r')
X2 = hdf.get('data1')
X2=np.reshape(X2,(X2.shape[0],-1)).T




activation_function = ['relu', 'relu', 'sigmoid']

my_dict_back = np.load('my_dict.npy')
print(my_dict_back.item().keys())    
# print(my_dict_back.item().get('W1'))
parameters = {}
for i in my_dict_back.item().keys():
	parameters[i] = my_dict_back.item().get(i)

filepath = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'



video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
a=0
flag = 0
t1=time.time()
while True :
	# os.system()
	time.sleep(0.1)
	a+=1
	check, frame = video.read()
	frame=cv2.resize(frame, (64,64))
	X = np.resize(frame,(12288,1))
	X = (X-np.mean(X2, axis = 1, keepdims = True))/np.var(X2,axis = 1,keepdims=True)

	A_final,caches = forward_prop(parameters,X,activation_function)

	if np.sum(A_final)>0.5:
		if flag == 0:
			os.startfile(filepath)
			time.sleep(2.2) 
			flag = 1
			A_final=0
		elif flag==1:
			os.system('taskkill /IM chrome.exe')
			time.sleep(2.2) 
			flag = 0			
			A_final=0
		X=np.zeros(X.shape)	

	print(A_final)
	#gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	cv2.imshow("capturing you",frame)
	
	#key = cv2.wait(1)

	if cv2.waitKey(1)  & 0xFF == ord('q'):
		break;
	if a==100:
		t2=time.time()
		print('fps : ' + str(100/(t2-t1)))

video.release()

cv2.destroyAllWindows
