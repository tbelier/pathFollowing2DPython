import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os
from roblib import *

def displayFinal(t_stock, s1_stock, y1_stock, theta_stock):
    ax.figure()
    ax.plot(t_stock, s1_stock, 'r', label='s1 (rouge)')
    ax.plot(t_stock, y1_stock, 'g', label='y1 (vert)')
    ax.plot(t_stock, theta_stock, 'b', label='Theta (bleu)')
    ax.legend()
    ax.title('Évolution des variables')
    ax.show()

def find_index_in_interval_np(s, pathCSY): #on donne une valeur s et une liste 1D, le code renvoie le premier indice entre lesquels se trouve notre valeur s
    pathCSY = np.array(pathCSY)  # Convertir la liste en tableau NumPy
    X,Y,C,S,Psi = pathCSY.T
    Smax = max(S)
    indices = np.where((pathCSY[:-1] <= s) & (s < pathCSY[1:]))[0]
    return indices[0] if len(indices) > 0 else None

def interrogation_chemin(L, s):
    index = find_index_in_interval_np(s, L)
    lievreX, lievreY, lievreC, lievreS, lievrePsi = L[index]
    return np.array([[lievreX],
                     [lievreY],
                     [lievrePsi]]), lievreC

def modele(X, U):
    x,y,psi = X.flatten()
    u1,u2 = U.flatten() # vitesse linéaire et de rotation de commande

    B = array([[np.cos(psi), 0], 
               [np.sin(psi), 0], 
               [0,           1]])
    Xp = B @ array([[u1],
                    [u2]])
    return Xp

def getPath(str):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    loaded_array = np.load(f"{script_dir}/{str}")
    X,Y,C,S,Psi = loaded_array.T
    Smax = max(S)
    return np.column_stack((X,Y,C,S,Psi))

def display(L):
    LX,LY,LC,LS,LPsi = L.T
    lievreX, lievreY, lievrePsi = lievre.flatten()

    ax.cla()
    ax.plot(LX,LY, "lightgrey", label='Chemin')

    draw_rov2D(ax,X,col='blue',scale=3, facing="right",w=3)
    draw_arrow(lievreX, lievreY,lievrePsi,1,col='green',w=1)
    draw_arrow(lievreX, lievreY,lievrePsi+np.pi/2,1,col='red',w=1)
    ax.axis("equal")
    ax.legend()

def sawtoothvector(V, modulo = "2pi"):
    if modulo == "2pi":
        x,y,psi = V.flatten()
        psi = psi%(2*pi)
        return array([[x],[y],[psi]])
    
    if modulo == "pi":
        x,y,psi = V.flatten()
        psi = (psi + np.pi) % (2 * np.pi) - np.pi
        return array([[x],[y],[psi]])
    
def sawtooth1D(psi, modulo = "2pi"):
    if modulo == "2pi":
        return psi%(2*pi)
    
    if modulo == "pi":
        return (psi + np.pi) % (2 * np.pi) - np.pi
    
j=0
if __name__ == "__main__":
    Wxmin,Wxmax, Wymin, Wymax = 50,50,50,50
    ax=init_figure(Wxmin-5,Wxmax+5,Wymin-5,Wymax+5)


    # Initialisation du système
    X = np.array([[20], 
                  [10],
                  [np.pi/4]])
    s = 0
    U = array([[0.1],
               [0]])
    dt = 0.1
    K, K1, Kdy1, K10 = 10, 10, 10, 10

    Lpath = getPath("AllPointsXYCSTheta.npy")
       
    for k in arange(0,1500,dt):
        # récupération des variables d'état et des commandes
        _,_,psi = X.flatten()
        u1,u2 = U.flatten()

        B = np.array([[cos(psi), 0], 
                      [sin(psi), 0], 
                      [0, 1]])
        
        X0 = B @ np.array([[u1], 
                          [u2]])
        x0,y0,psi0 = X0.flatten()
        V_0 = np.array([[x0],
                        [y0]])
        W_0 = np.array([[psi0]])

        lievre, lievreCc = interrogation_chemin(Lpath, s)
        lievreX,lievreY,lievrePsi = lievre.flatten()
        
        E = lievre-X
        errX, errY, theta = E.flatten()
        theta = sawtooth1D(theta, "pi")
        errXY = np.array([[errX],
                          [errY]])
        R = np.array([[np.cos(lievrePsi), -np.sin(lievrePsi)],
                      [np.sin(lievrePsi),  np.cos(lievrePsi)]])
        
        errX_Fresnet = inv(R) @ errXY
        
        s1, y1 = errX_Fresnet.flatten() 
        sp = u1 * cos(theta) - K1 * s1
        lievreXp_Fresnet = np.array([[sp], 
                                     [0]])
        dot_X_e_F = lievreXp_Fresnet - inv(R) @ V_0

        s1p,y1p = dot_X_e_F.flatten()
        psip_lievre = lievreCc * sp

        delta = -np.arctan(Kdy1 * y1)
        deltaPrime = -Kdy1 / (1 + (Kdy1 * y1) ** 2)
        deltaP = deltaPrime * y1p

        Err_Ang = sawtooth1D(delta - theta, "pi")
        if Err_Ang > np.pi: Err_Ang -= 2 * np.pi
        elif Err_Ang < -np.pi: Err_Ang += 2 * np.pi
            
        dot_Theta_Control = deltaP + K * Err_Ang
        dot_psi = psip_lievre - dot_Theta_Control
        u2 = dot_psi

        U = array([[u1],
                   [u2]])
        if sp < 0: sp = 0
        s = s + sp*dt
        
        Xp = modele(X,U)
        X = sawtoothvector(X + dt*Xp, modulo = "2pi")
        pause(0.01)
        display(Lpath)
        
    show()