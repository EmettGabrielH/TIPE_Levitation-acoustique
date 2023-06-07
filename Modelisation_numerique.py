
# Importation des bibliothèques utiles
from math import cos, sin, pi 
import matplotlib.pyplot as plt
import numpy as np

def graphique (X,Y, xtitre,ytitre,titre): # Fonction pour afficher un graphe
    plt.title(titre)
    plt.plot(X,Y)
    plt.xlabel(xtitre)
    plt.ylabel(ytitre)
    plt.show()
    
def Calculs_theoriques(h,f):
    #Variables:
    φ = 2            # déphasage entre les deux transducteurs (en rad)
    ω = 2 * pi * f   # pulsation (en rad.s-1)
    
    # Données
    H = 5 * 10**-2   # distance max entre les émetteurs (en m)
    
    c0 = 344         #vitesse du son dans l'air (en m.s-1)
    ρ0 = 1.292                # kg.m-3, masse volumique air
    κ0 = 1/((c0**2) *  ρ0)    # coefficient compressibilité air
    
    f0 = 40 *10**3
    Am0 = 50*10**-2           # vitesse des hauts parleurs de référence à f = 40 kHz (en m.s-1)
    d0 = Am0/f0               # distance caractéristique de déplacement transducteurs (en m)
    Am = d0 * f               # vitesse déplacement transducteurs (en m.s-1)
    Bm = Am                   

    
    a = 3*10**-3              # rayon bille de polystyrène (en m)
    Vp = (4/3) * pi * (a ** 3)# volume bille
    cp = 425                  # vitesse du son dans le polystyrène (en m.s-1)
    ρp = 14                   # masse volumique du polystyrène expansé (en kg.m-3)
    κp = 1/((cp**2) *  ρp)
    
    def Urad(P_m, V_m):       # Fonction donnant l'énergie potentiel de radiation
        f1 = 1 - (κp/κ0)
        f2 = 2*(ρp/ρ0 -1 )/ (2*(ρp/ρ0) - 1 )
        return Vp * (f1 * (κ0/2) * P_m - f2 * (3/4)*ρ0*V_m)

    def Ep(z):
        M = Vp*ρp             # Fonction donnant l'énergie potentiel de pesanteur
        g = 9.81              # accélération gravitationnel (en m.s-1)
        return M*g*z
    def Transducteur_ultrason(t,U,phi):
        return U*cos(ω*t + phi)
    


    # Calcul champs pression + vitesse
    Nz = 144                  # Nombre de subdivisions de H
    δz = H/Nz                 # Pas de la subdivision (en m)
    Nh = int(h/δz )

    T = 0.0003                # Temps de l'expérience (en s)
    δt= 10**-6                # Pas de la subdivision (en s)
    Nt = int(T/δt)
    
    V = [[0 for m in range(Nz)] for n in range(Nt)]
    P = [[0 for m in range(Nz)] for n in range(Nt)]
    #Initialisation
    
    V[0][0] = Transducteur_ultrason(0,Am,0)
    V[0][Nh] = Transducteur_ultrason(0,Bm,φ)
    V[1][0] = Transducteur_ultrason(δt,Am,0)
    V[1][Nh] = Transducteur_ultrason(δt,Bm,φ)

    #Calcul de V (champs vitesse) et de P (champs pression)
    for n in range(2, Nt):
        t = n*δt
        V[n][0] = Transducteur_ultrason(t,Am,0)
        V[n][Nh] = Transducteur_ultrason(t,Bm,φ)
        for m in range(1,Nh):
            V[n][m] = (((c0*δt)/(δz)) ** 2) * ( V[n-1][m+1] - 2*V[n-1][m] + V[n-1][m-1]) + 2*V[n-1][m] - V[n-2][m]
            P[n][m] = P[n][m-1] +  δz*(-ρ0)* ((V[n][m]-V[n-1][m])/δt)

    #Initialisation
    V_m,P_m = [0 for m in range(Nz)], [0 for m in range(Nz)]
    U_rad_z = [0 for m in range(Nz)]
    U = [0 for m in range(Nz)]
    N = Nt - int(Nt/2)
    
    #Calcul moyenne temporel champs vitesse/ pression au carré
    for m in range(Nz):
        for n in range(int(Nt/2), Nt):
            V_m[m] += (V[n][m]**2)/N
            P_m[m] += (P[n][m]**2)/N
        U_rad_z[m] = Urad(P_m[m],V_m[m])
        U[m] = U_rad_z[m] + Ep(m*δz)
        
    x=[i*δz*100 for i in range(Nz)]
    graphique(x,U,"Position (en cm)","Potentiel (en kg.m²/s²)", "Energie Potentiel \n pour f="+str(f/1000)+" kHz, h = "+str(h*100) +" cm")
    #graphique(x,P_m,"Position (en cm)","Pression (en Pa)", "Graphe pression moyenne à f="+str(f/1000)+" kHz, h = "+str(h*100) +" cm")
    #graphique(x,V_m,"Position (en cm)","Vitesse (en m.s-1)", "Graphe vitesse moyenne à f="+str(f/1000)+" kHz, h = "+str(h*100) +" cm")
    
    #"""
    y=np.linspace(0,T*1000,Nt)
    X,Y=np.meshgrid(x,y)
    plt.figure(figsize=(25,15))
    
    cf=plt.contourf(X,Y,V,100,cmap='jet')
    graph=plt.contour(X,Y,V,10,colors='black')
    plt.clabel(graph,inline=1,fontsize=10,fmt='%3.2f') 
    plt.colorbar(cf)
    plt.xlabel("Position selon l'axe z (en cm)")
    plt.ylabel("Temps (en ms)")
    plt.title("Carte Vitesse par rapport au temps et à la position\n à f="+str(f/1000)+"kHz, h = "+str(h*100) +"cm")      
    plt.show()
    #"""
    
def main():
    h = 2.73 * 10**-2  # distance entre les émetteurs en cm
    f  = 39 *10**3
    Calculs_theoriques(h,f)
    return None

main()
