import pandas as pd
from unipath import Path

names = ['LSS{}.txt'.format(x) for x in [101, 102, 103, 104]]

in_header = 'subjCode	seed	cuePicMapping	responseDevice	data	room	initials	trialIter	trialID	valid_cue	target_id	soa	cue_type	side	pic_version	pic_category	pic_type	pic_id	cue_category	cue_version	cue_file	pic_file	block	whichPart	curTrialIndex	expTimer	isRight	rt'.split()

out_header = 'subjCode	seed	cuePicMapping	responseDevice	data	room	initials	trialIter	trialID	valid_cue	target_id	soa	cue_type	side	pic_version	pic_category	pic_type	pic_id	cue_category	block	cue_version	pic_file	cue_file	whichPart	curTrialIndex	expTimer	isRight	rt'.split()

for name in names:
    df = pd.read_table(name, names = in_header)
    df[out_header].to_csv(name, sep='\t', index=False, header=None)
