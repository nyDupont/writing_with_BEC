import matplotlib.pyplot as plt
import numpy as np
import os
import random as rm
import re

def word2matrix(word):
    L = len(word)
    kerning_filling = np.load('str_matrices/{}.npy'.format(ord(' ')))
    matrices_list = [kerning_filling]
    for index in range(L):
        string = word[index]
        matrix = np.load('str_matrices/{}.npy'.format(ord(string)))
        matrices_list.append(matrix)
        matrices_list.append(kerning_filling)
    return np.hstack(matrices_list)

def word2od(word, randomize=True, alignement='center'):
    Lines = re.split('\n', word)
    matrices = []
    for Line in Lines:
        matrix = word2matrix(Line)
        OD = []
        for column in matrix.T:
            name = ''.join(column.astype(int).astype(str))
            files_name = sorted(os.listdir('BECttf/' + name + '/'))
            rand_index = -1
            if randomize:
                rand_index = rm.randint(0, len(files_name)-1)
            od = np.load('BECttf/{}/'.format(name) + files_name[rand_index]).T
            if name != 7*'0':
                OD.append(od/(np.max(od)))
            else:
                OD.append(od/1.5)
        matrices.append(np.hstack(OD))

    return np.vstack(justification(matrices, alignement=alignement))


def justification(arrays, alignement='center'):
    new_arrays = []
    max_w = np.max([x.shape[1] for x in arrays])
    for x in arrays:
        if x.shape[1] < max_w:
            new_x = np.zeros((arrays[0].shape[0], max_w))
            missing = max_w - x.shape[1]
            if alignement == 'center': left_fill = int(missing/2)
            elif alignement == 'left': left_fill = 0
            elif alignement == 'right': left_fill = max_w - x.shape[1]
            new_x[:,left_fill:left_fill+x.shape[1]] = x
            new_arrays.append(new_x)
        else:
            new_arrays.append(x)
    return new_arrays


def bec_write(string, randomize=False, alignement='center', width=29.7, dpi=100, save=True, cmap='Blues_r', show=True, format='png', vmax=0.6, vmin=0.08):
    od = word2od(string, randomize=randomize, alignement=alignement)
    h, w = od.shape
    ratio = h/w
    width /= 2.34
    fig, ax = plt.subplots(figsize=(width, width*ratio), dpi=dpi)
    ax.axis('off')
    ax.imshow(np.array(od), cmap=cmap, vmin=vmin, vmax=vmax)
    plt.subplots_adjust(bottom=0, top=1, right=1, left=0)
    save_name = string[:33].replace(' ', '_').replace('.', 'p').replace('\n', '&')
    if save: plt.savefig('images/{}.{}'.format(save_name, format))
    if not show: plt.close('all')
