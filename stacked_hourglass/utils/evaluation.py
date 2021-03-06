import math

import torch

from .transforms import transform_preds

__all__ = ['accuracy', 'AverageMeter']

def get_preds(scores):
    ''' get predictions from score maps in torch Tensor
        return type: torch.LongTensor
    '''
    assert scores.dim() == 4, 'Score maps should be 4-dim'
    maxval, idx = torch.max(scores.view(scores.size(0), scores.size(1), -1), 2)

    maxval = maxval.view(scores.size(0), scores.size(1), 1)
    idx = idx.view(scores.size(0), scores.size(1), 1) + 1

    preds = idx.repeat(1, 1, 2).float()

    preds[:,:,0] = (preds[:,:,0] - 1) % scores.size(3) + 1
    preds[:,:,1] = torch.floor((preds[:,:,1] - 1) / scores.size(3)) + 1

    pred_mask = maxval.gt(0).repeat(1, 1, 2).float()
    preds *= pred_mask
    return preds

def calc_dists(preds, target, normalize):
    preds = preds.float()
    target = target.float()
    dists = torch.zeros(preds.size(1), preds.size(0))
    for n in range(preds.size(0)):
        for c in range(preds.size(1)):
            if target[n,c,0] > 1 and target[n, c, 1] > 1:
                dists[c, n] = torch.dist(preds[n,c,:], target[n,c,:])/normalize[n]
            
            else:
                dists[c, n] = -1
            #print('dits',dists)
    return dists

def dist_acc(dist, thr=4):
    ''' Return percentage below threshold while ignoring values with a -1 '''
    dist = dist[dist != -1]
    #print('dist != -1', (dist != -1))
    if len(dist) > 0:
        #print('dist',dist)
        #print('bool',1.0 * (dist < thr).sum().item())
        return 1.0 * (dist < thr).sum().item() / len(dist)
    else:
        return -1

def accuracy(output, target, idxs, thr=4):
    ''' Calculate accuracy according to PCK, but uses ground truth heatmap rather than x,y locations
        First value to be returned is average accuracy across 'idxs', followed by individual accuracies
    '''
    preds   = get_preds(output)
    gts     = get_preds(target)
    norm    = torch.ones(preds.size(0))*output.size(3)/10
    dists   = calc_dists(preds, gts, norm)

    acc = torch.zeros(len(idxs)+1)
    avg_acc = 0
    cnt = 0

    for i in range(len(idxs)):
        #print('idx',idxs)
        #print('i',i)
        #print(len(idxs))
        #print('dists[idxs[i]', dists[idxs[i]])
        with open ('dists.txt','a') as f:
            f.write("dists"+str(dists[idxs[i] - 1]))
            f.write("idx[i] "+ str(idxs[i]))
            f.write('\n')
        acc[i+1] = dist_acc(dists[idxs[i]-1])
        if acc[i+1] >= 0:
            avg_acc = avg_acc + acc[i+1]
            cnt += 1


    if cnt != 0:
        acc[0] = avg_acc / cnt
    return acc

def final_preds_untransformed(output, res):
    coords = get_preds(output) # float type

    # pose-processing
    for n in range(coords.size(0)):
        for p in range(coords.size(1)):
            hm = output[n][p]
            px = int(math.floor(coords[n][p][0]))
            py = int(math.floor(coords[n][p][1]))
            if px > 1 and px < res[0] and py > 1 and py < res[1]:
                diff = torch.Tensor([hm[py - 1][px] - hm[py - 1][px - 2], hm[py][px - 1]-hm[py - 2][px - 1]])
                coords[n][p] += diff.sign() * .25
    coords += 0.5

    if coords.dim() < 3:
        coords = coords.unsqueeze(0)

    coords -= 1  # Convert from 1-based to 0-based coordinates

    return coords

def final_preds(heatmaps, center, scale, out_res, inp_res=None, rot=None):

    coords = final_preds_untransformed(heatmaps, out_res)
    preds = coords.clone()
    """Transform back."""
    for i in range(coords.size(0)):
        preds[i] = transform_preds(preds[i], center[i],
                                   scale[i],
                                   out_res, inp_res, rot)

    if preds.dim() < 3:
        preds = preds.unsqueeze(0)

    return preds, coords


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
