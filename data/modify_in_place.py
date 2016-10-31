import pandas as pd
from unipath import Path

names = ['LSS_v2_{}.txt'.format(x) for x in [122, 123]]

in_header = 'subjCode	seed	cuePicMapping	responseDevice	data	room	initials	trialIter	trialID	valid_cue	target_id	soa	cue_type	side	pic_version	pic_category	pic_type	pic_id	cue_category	block	cue_version	pic_file	cue_file	whichPart	curTrialIndex	expTimer	isRight	rt'.split()

out_header = 'subjCode	seed	cuePicMapping	responseDevice	data	room	initials	trialIter	trialID	valid_cue	target_id	soa	cue_type	side	pic_version	pic_category	pic_type	pic_id	cue_category	block	cue_version	pic_file	cue_file	exp_name	whichPart	curTrialIndex	expTimer	isRight	rt'.split()

for name in names:
    df = pd.read_table(name, names = in_header)
    df['exp_name'] = 'LSS_v2'
    df[out_header].to_csv(name, sep='\t', index=False, header=None)
