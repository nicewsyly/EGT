import os
from scipy.io import loadmat
import numpy as np

from evaluate import compute_map

def init_revop(dataset,data_root):
    # features = loadmat('/d2/lmk_code/revisitop/data/features/roxford5k_resnet_rsfm120k_gem.mat');
    # gnd = loadmat('/d2/lmk_code/revisitop/data/datasets/roxford5k/gnd_roxford5k.mat');
    global test_dataset
    global cfg
    global features
    test_dataset = dataset
    # config file for the dataset
    cfg = configdataset(test_dataset, os.path.join(data_root, 'datasets'))
    return cfg


def eval_revop(p):
    # revisited evaluation
    gnd = cfg['gnd']

    # evaluate ranks
    ks = [1, 5, 10]

    # search for hard
    gnd_t = []
    for i in range(len(gnd)):
        g = {}
        g['ok'] = np.concatenate([gnd[i]['hard']])
        g['junk'] = np.concatenate([gnd[i]['junk'], gnd[i]['easy']])
        gnd_t.append(g)
    mapH, _, _, _ = compute_map(p, gnd_t, ks)
    return np.around(mapH*100, decimals=2)


def configdataset(dataset, dir_main):

    dataset = dataset.lower()

    if dataset == 'roxford5k' or dataset == 'rparis6k':
        cfg = {'ext' : '.jpg', 'qext' : '.jpg', 'dir_data' : os.path.join(dir_main, dataset)}
        cfg['gnd_fname'] = os.path.join(cfg['dir_data'], 'gnd_' + dataset + '.mat')
        print(cfg['gnd_fname'])
        gt = loadmat(cfg['gnd_fname'])
        cfg['imlist'] = [str(''.join(im)) for iml in np.squeeze(gt['imlist']) for im in iml]
        cfg['qimlist'] = [str(''.join(im)) for iml in np.squeeze(gt['qimlist']) for im in iml]
        cfg['gnd'] = gnd_mat2py(gt['gnd'])
        cfg['n'] = len(cfg['imlist'])
        cfg['nq'] = len(cfg['qimlist'])

    elif dataset == 'revisitop1m':
        cfg = {'ext' : '.jpg', 'dir_data' : os.path.join(dir_main, dataset)}
        cfg['imlist_fname'] = os.path.join(cfg['dir_data'], '{}.txt'.format(dataset))
        cfg['imlist'] = read_imlist(cfg['imlist_fname'])
        cfg['n'] = len(cfg['imlist'])

    else:
        raise ValueError('Unknown dataset: %s!' % dataset)

    cfg['dir_images'] = os.path.join(cfg['dir_data'], 'jpg')

    cfg['im_fname'] = config_imname
    cfg['qim_fname'] = config_qimname

    cfg['dataset'] = dataset

    return cfg


def config_imname(cfg, i):
    _, ext = os.path.splitext(cfg['imlist'][i])
    if ext:
        return os.path.join(cfg['dir_images'], cfg['imlist'][i])
    else:
        return os.path.join(cfg['dir_images'], cfg['imlist'][i] + cfg['ext'])


def config_qimname(cfg, i):
    _, ext = os.path.splitext(cfg['qimlist'][i])
    if ext:
        return os.path.join(cfg['dir_images'], cfg['qimlist'][i])
    else:
        return os.path.join(cfg['dir_images'], cfg['qimlist'][i] + cfg['qext'])


def gnd_mat2py(gnd):
    gnd = np.squeeze(gnd);
    gndpy = []
    for i in np.arange(len(gnd)):
        gndi = gnd[i]
        gndpyi = {}
        try:
            gndpyi['ok'] = gnd[i]['ok']-1
            gndpyi['ok'] = gndpyi['ok'].reshape(gndpyi['ok'].shape[1])
        except:
            pass
        try:
            gndpyi['easy'] = gnd[i]['easy']-1
            gndpyi['easy'] = gndpyi['easy'].reshape(gndpyi['easy'].shape[1])
        except:
            pass
        try:
            gndpyi['hard'] = gnd[i]['hard']-1
            gndpyi['hard'] = gndpyi['hard'].reshape(gndpyi['hard'].shape[1])
        except:
            pass
        try:
            gndpyi['junk'] = gnd[i]['junk']-1
            gndpyi['junk'] = gndpyi['junk'].reshape(gndpyi['junk'].shape[1])
        except:
            pass
        try:
            gndpyi['bbx'] = np.squeeze(gnd[i]['bbx'])
        except:
            pass
        gndpy.append(gndpyi)

    return gndpy


def read_imlist(imlist_fn):
    file = open(imlist_fn, 'r')
    imlist = file.read().splitlines();
    file.close()
    return imlist
