#!/usr/bin/env python
# encoding: utf-8
"""
generateTrials.py
"""
import pandas as pd
import numpy as np

from experimentResources import (counterbalance, expand, extend,
                                 add_block, smart_shuffle)
from experimentResources import StimGenerator

def main(seed=None, cuePicMapping='random', ratio=0.50, block_size=100,
         id_col='cue_category'):
    if seed:
    	seed = int(seed)
    conditions = {'cue_type':['label'],
    			  'soa': ['.8', '1.0', '1.2'],
    			  'side': ['left','right'],
                  'pic_version':['A','B']}
    trialTypes = counterbalance(conditions)
    picInfo = pd.read_csv('stimuli_info.csv')
    trials = pd.merge(trialTypes, picInfo)

    trials = expand(trials, ids=['valid_cue', 'target_id'],
                    ratio=ratio, seed=seed)

    cueGen = StimGenerator(picInfo, 'valid_cue', 'pic_category', seed=seed)
    trials['cue_category'] = trials.apply(cueGen.next, axis=1)

    trials = extend(trials, max_length=400)
    trials = add_block(trials, block_size, id_col, seed)
    trials = smart_shuffle(trials, 'cue_category', 'block', seed)

    if cuePicMapping == 'fixed':
        trials['cue_version'] = trials.pic_version
    elif cuePicMapping == 'reversed':
        reverser = dict(A='B', B='A')
        trials['cue_version'] = trials.pic_version.map(reverser)
    elif cuePicMapping == 'random':
        # To determine cue_version, simply shuffle all the pic_versions
        shuffled_pic_versions = trials.pic_version.sample(len(trials)).tolist()
        trials['cue_version'] = shuffled_pic_versions
    else:
        raise NotImplementedError('picCueMaping = {}'.format(picCueMapping))

    trials['pic_id'] = trials['pic_id'].astype(str)
    trials['pic_file'] = trials['pic_category'] + '_' + trials['pic_type'] + \
                        '_' + trials['pic_id']
    trials['cue_file'] = trials['cue_category'] + '_' + trials['cue_type'] + \
                        '_' + trials['cue_version']

    return trials

def write(path, **kwargs):
    trials = main(**kwargs)
    trials.to_csv(path, index=False)

if __name__ == '__main__':
    trials = main(cuePicMapping='reversed')
    trials.to_csv('sample_trials.csv', index=False)
