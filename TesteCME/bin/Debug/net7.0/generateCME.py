import os
print("----------------diretório atual", os.getcwd())

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import subprocess
from numpy.linalg import norm
import random

Nx = 856
maps = "gist_heat"
color = '.9'

pontoX = 300
pontoY = 400
raioMaior = 400
raioMenor = 150
angulo = 60
radianos = angulo * np.pi / 180
seed = random.randint(0,10000)

frames = 10

for j in range(frames):
    rMai = (raioMaior / frames) + (raioMaior / frames) * j
    rMen = (raioMenor / frames) + (raioMenor / frames) * j

    subprocess.call([r"./TesteCME.exe", str(j), str(seed)])
    print(str(j))
    f = open(f"CMEFrame{j}.txt", "r")
    vetor = f.read().split(",")
    for i in range(len(vetor)):
        vetor[i] = float(vetor[i])
    ndvetor = np.asarray(vetor)
    
    #Criar mascara
    mascara = np.zeros(856*856)
    index = 0

    cosa = np.cos(radianos)
    sina = np.sin(radianos)
    dd = rMai * rMai
    DD = rMen * rMen

    arrayX = np.arange(0,Nx)
    arrayY = np.arange(0,Nx)
    
    distanciaVetor = []

    mascara = np.empty((Nx,Nx))
    for y in arrayY:
        a = np.power(cosa*(arrayX-pontoX)+sina*(y-pontoY),2)
        b = np.power(sina*(arrayX-pontoX)-cosa*(y-pontoY),2)
        distancia = (a/dd)+(b/DD)        
        mascara[y] = (np.where(distancia <= 1, 1-(distancia*distancia*distancia*distancia),0))
    
    mascara = mascara.reshape(Nx*Nx)    
    ###
    #Multiplicar ndvetor pela mascara
    ndvetor = ndvetor*mascara
    ###
    ndvetor = ndvetor.reshape(Nx, Nx)

    fig = plt.figure(figsize=(8, 6), dpi=128)#, facecolor='k', edgecolor='k')
    gs = gridspec.GridSpec(4, 1)#, width_ratios=[1, 1])
    #ax = fig.add_subplot(111)
    ax = plt.subplot(gs[:3, :])
    ax.imshow(ndvetor, cmap=maps, interpolation='gaussian', origin='lower')
    ax = plt.subplot(gs[3:, :])
    ax.set_xlabel('time (h)', fontweight='bold')
    ax.set_ylabel(r'flux (L$\star$)', fontweight='bold')
    ax.grid(which='major', c=color, alpha=.6, lw=.6)
    ax.grid(which='minor', c=color, alpha=.3, lw=.3)
    ax.set_facecolor('k')
    for sp in ('left','bottom', 'right', 'top'):
        ax.spines[sp].set_color(color)
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis='both', which='both', colors=color)
    fig.tight_layout()			
    fig.savefig(f'noise{str(j)}.png', dpi=128, facecolor='k')
    plt.close('all')
 