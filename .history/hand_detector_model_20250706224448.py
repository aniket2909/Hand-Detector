# import numpy as np

# ######################################################################################

# def initialisation(layers_dims,activation_functions):
# 	he = True
# 	parameters = {}
# 	for i in range(len(layers_dims) -1):
# 		parameters['W'+str(i+1)] = np.random.randn(layers_dims[i+1],layers_dims[i])
# 		if(he == True):
# 			if activation_functions[i] == 'sigmoid': 
# 				parameters['W'+str(i+1)] = parameters['W'+str(i+1)]*np.sqrt(1/layers_dims[i])
# 			else:
# 				parameters['W'+str(i+1)] = parameters['W'+str(i+1)]*np.sqrt(2/layers_dims[i])
# #hyperparameter 0.01
# 		else:
# 			parameters['W'+str(i+1)]=parameters['W'+str(i+1)]*0.01
# 		parameters['b'+str(i+1)] = np.zeros((layers_dims[i+1],1))	
# 	return parameters		


# #######################################################################################

# def forward_prop(parameters,X,activation_functions):
# 	caches = []
# 	A_prev = X
# 	Z = None
# 	for i in range(len(activation_functions)):
# 		Z = np.dot(parameters['W'+str(i+1)],A_prev) + parameters['b'+str(i+1)]
# 		if activation_functions[i] == 'relu':
# 			A = Z*(Z>0)
# 		else:
# 			A = 1/(1+np.exp(-Z))
# 			if np.sum(A)==0 : print("        "+str(i))		
# 		# A = np.resize(A,(A.shape[0],-1))	
# 		caches.append([A_prev, parameters['W'+str(i+1)], parameters['b'+str(i+1)],A])
# 		A_prev = A	
# 	return A,caches

# #######################################################################################

# def compute_cost(A_final,Y,lambdaa,parameters):
# 	m=A_final.shape[1]
# 	cost = None
# 	cost = 1/m*np.sum(-Y*np.log(A_final)-(1-Y)*np.log(1-A_final))
# 	for i in range(int(len(parameters)/2)):
# 		cost+= 1/m*lambdaa*np.sum(parameters['W'+str(i+1)]*parameters['W'+str(i+1)])
# 	return cost

# #######################################################################################

# def backward_prop(dA_final,caches,activation_functions):
# 	dA = dA_final
# 	m = dA.shape[1]
# 	grads = {}
# 	for i in reversed(range(len(caches))):
# 		A_prev,W,b,A = caches[i]
# 		if activation_functions[i] == "relu":
# 			dg = (A>0)
# 		elif activation_functions[i] == "sigmoid":
# 			dg = A*(1-A)
# 		dZ = dg*dA
# 		dW = 1/m * np.dot(dZ,A_prev.T)
# 		db = 1/m * np.sum(dZ,axis = 1,keepdims = 1)
# 		dA = np.dot(W.T,dZ)
# 		grads['W'+str(i+1)] = dW
# 		grads['b'+str(i+1)] = db
# 	return grads	
