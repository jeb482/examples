# numpy_demo.py
# python 2.7.6
# @author Jimmy

import argparse
import winsound
import time
import numpy as np

def tictoc(f, functionName, playSound=True, soundFile=None):
    """
    Prints the time it takes for a function to execute,
    and plays a sound upon completion if necessary.
    """
    start = time.time()
    r = f()
    end = time.time()
    print (functionName + " took " + str(end - start) + " seconds to complete.")
    
    if playSound:
        if soundFile != None:
            try:
                winsound.PlaySound(soundFile,winsound.SND_FILENAME)
                return r
            except RuntimeError:
                pass
        print('\a')
    return r

def numpyMultiply(A,B):
    return A.dot(B)
    
def naiveMultiply(A,B):
    M = np.zeros((A.shape[0], B.shape[1]))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            for k in range(A.shape[1]):
                M[i,j] += A[i,k]*B[k,j]
    return M
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="size of matrices multiplied together", type=int)
    args = parser.parse_args()
    n = args.n
        
    A = np.random.random((n,n))
    B = np.random.random((n,n))
    print("Multiplying two " + str(n)+'x'+str(n)+ " matrices.")
    C1 = tictoc(lambda : numpyMultiply(A,B), "Numpy", True, "human_done.wav")
    C2 = tictoc(lambda : naiveMultiply(A,B), "Naive", True, "orc_complete.wav")
    
    print ("Norm(C1 - c2): " + str(np.linalg.norm(C1 - C2)))