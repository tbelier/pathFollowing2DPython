import numpy as np
import os

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# Charger le tableau depuis le fichier .npy
loaded_array = np.load(f"{script_dir}/AllPointsXY.npy")
print(loaded_array)
LX = loaded_array[:,0]
LY = loaded_array[:,1]

Lx, Ly, Lc, Ls, Ltheta = [0],[0],[0],[0],[0]
for k in range(1,len(LX)-1):
    xk_1, xk = LX[k-1], LX[k] 
    yk_1, yk = LY[k-1], LY[k] 

    sk_1 = Ls[-1]
    sk = sk_1 + np.sqrt((yk_1-yk)**2+(xk_1-xk)**2)

    thetak_1 = Ltheta[-1]
    thetak = np.arctan2(yk-yk_1, xk-xk_1)

    ck = (thetak-thetak_1)/sk

    Lx.append(xk)
    Ly.append(yk)
    Lc.append(ck)
    Ls.append(sk)
    Ltheta.append(thetak)
    

array = np.column_stack((Lx,Ly,Lc,Ls,Ltheta))
print(array)
np.save(f"{script_dir}/AllPointsXYCSTheta.npy", array)

