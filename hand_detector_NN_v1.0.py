import numpy as np
import matplotlib.pyplot as plt
import h5py
from aniketsNN_functions_v1 import *

#save all your data to aniketsNN_save.h5

hdf = h5py.File(r'C:\Users\anike\Desktop\Deep Learning Project 1\h5_data.h5','r')
X = hdf.get('data1')
Y=hdf.get('data2')
X=np.reshape(X,(X.shape[0],-1)).T
Y=np.reshape(Y,(1,len(Y)))
X = (X-np.mean(X, axis = 1, keepdims = True))/np.var(X,axis = 1,keepdims=True)

print(X.shape)
print(Y.shape)

m = X.shape[1]

layers_dims=[X.shape[0],15,5,1]     #set these
activation_functions=['relu','relu','sigmoid']
assert(len(layers_dims) == len(activation_functions)+1)

parameters = initialisation(layers_dims,activation_functions)

store1 = []
store2 = []

#hyperparameter lambdaa, learning rate & #iterations
lambdaa = 0.03
learning_rate = 0.7

for i in range(2500):
	A_final,caches = forward_prop(parameters,X,activation_functions)
	# print(A_final)
	cost = compute_cost(A_final,Y,lambdaa,parameters)
	if i%100 == 0:
		print("The cost of "+ str(i) +"iteration is "+str(cost))
		store1.append(i)
		store2.append(cost)
	dA_final = A_final - Y
	grads = backward_prop(dA_final,caches,activation_functions)
	for j in range(len(activation_functions)):
		parameters['W'+str(j+1)] = (1-lambdaa*learning_rate/m)*parameters['W'+str(j+1)] - learning_rate*grads['W'+str(j+1)]
		parameters['b'+str(j+1)] = (1-lambdaa*learning_rate/m)*parameters['b'+str(j+1)] - learning_rate*grads['b'+str(j+1)]

print(parameters)
print(activation_functions)
plt.plot(store1,store2)
plt.show()
np.save('my_dict.npy',  parameters) 
