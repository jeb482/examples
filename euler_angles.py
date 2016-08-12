from math import atan2, pi, degrees, sqrt, cos, sin
import numpy as np
import random
from pprint import pprint
eps = 0.000000001


#########################################################
# Important code:
#########################################################
def get_euler_angles(X1, Y1, Z1):
	# Unpack vectors
	[X1x, X1y, X1z] = X1
	[Y1x, Y1y, Y1z] = Y1
	[Z1x, Z1y, Z1z] = Z1
	
	Z1xy = sqrt(Z1x**2+Z1y**2)
	# If Z is the same, just rotate there
	if (Z1xy < eps):
		alpha = 0;
		beta = 0 if (Z1z > 0) else pi
		gamma = atan2(X1y, X1x)
		return (alpha, beta, gamma)
	# Get angles if not parallel
	alpha = -atan2(Z1y*Y1x - Z1x*Y1y, Z1y*X1x - Z1x*X1y)
	beta  = -atan2(Z1xy , Z1z)
	gamma = atan2(-Z1x,Z1y)
	
	return (alpha, beta, gamma)

	
#########################################################
# Test Code:
#########################################################
def rotX(theta):
	return np.array([[1,          0,           0],
			[0, cos(theta), -sin(theta)],
			[0, sin(theta),  cos(theta)]])	
	
def rotY(theta):
	return np.array([[ cos(theta),  0,  sin(theta)],
			[          0,  1,           0],
			[ -sin(theta), 0,  cos(theta)]])
			
def rotZ(theta):
	return np.array([[cos(theta), -sin(theta),  0],
			[sin(theta),  cos(theta),  0],
			[         0,            0, 1]])
		
def eps_equals(a,b):
	return (np.linalg.norm(a-b) < eps);
	
def normalize(a):
	return (a / np.linalg.norm(a));
	
if __name__ == "__main__":
	# Tests where the z-axis is not [0,0,1] (with probability 1)
	print "Testing the case where the Z-axis is not fixed.\n"
	numTests = 10000
	failed = 0
	for i in range(numTests):
		X = normalize(np.random.rand(3))
		Y = normalize(np.random.rand(3))	
		Z = normalize(np.cross(X, Y))
		X = normalize(np.cross(Y, Z))
		
		alpha, beta, gamma = get_euler_angles(X,Y,Z)
		M = rotZ(gamma).dot(rotX(beta).dot(rotZ(alpha)))
	
		if not (eps_equals(M.dot([1,0,0]), X) or 
			    eps_equals(M.dot([0,1,0]), Y) or
			    eps_equals(M.dot([0,0,1]), Z)):
			failed += 1
	print "Passed " + str(numTests - failed) + "/" + str(numTests) + " tests.\n"
	
	
	# Tests where the z-axis is fixed.
	print "Testing the case where the Z-axis is fixed.\n"
	failed = 0
	for i in range(numTests):
		Z = np.array([0,0,(-1)**i])
		X = np.random.rand(3)
		X[2] = 0;
		X = normalize(X);
		Y = normalize(np.cross(Z,X))	
		
		alpha, beta, gamma = get_euler_angles(X,Y,Z)
		M = rotZ(gamma).dot(rotX(beta).dot(rotZ(alpha)))
	
		if not (eps_equals(M.dot([1,0,0]), X) or 
			    eps_equals(M.dot([0,1,0]), Y) or
			    eps_equals(M.dot([0,0,1]), Z)):
			failed += 1
	print "Passed " + str(numTests - failed) + "/" + str(numTests) + " tests.\n"
		

		