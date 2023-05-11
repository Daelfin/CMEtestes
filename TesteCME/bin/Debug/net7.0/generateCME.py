import os
print("----------------diretório atual", os.getcwd())

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import subprocess

Nx = 856
maps = "gist_heat"
color = '.9'

for j in range(10):
    subprocess.call([r"./TesteCME.exe", "300", "400", "400", "150", "60", "4857", str(j)])
    print(str(j))
    f = open("teste.txt", "r")
    vetor = f.read().split(",")
    for i in range(len(vetor)):
        vetor[i] = float(vetor[i])
    ndvetor = np.asarray(vetor)
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
 