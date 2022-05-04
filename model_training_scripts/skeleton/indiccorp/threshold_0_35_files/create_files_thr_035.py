lang_abr_list = ['as', 'bn', 'brx', 'gom', 'gu', 'hi', 'kn', 'ks', 'mai', 'ml', 'mni', 'mr', 'ne', 'or', 'pa', 'sa', 'sd', 'ta', 'te', 'ur']
#lang_abr_list=['sa','ne','gom']
#lang_abr_list=['mai', 'ur', 'sd']

threshold = -0.35

for lang_abr in lang_abr_list:
	
	f_in = open('../org_files/translit_pairs_with_avg_score_'+lang_abr+'.txt','r')
	lines_in = f_in.read().split('\n')

	lines_in = [line for line in lines_in if float(line.split('\t')[2]) > threshold ] 

	f_out = open('translit_pairs_with_avg_score_thr_035_'+lang_abr+'.txt','w')
	f_out.write('\n'.join(lines_in))
	f_out.close()

	f_in.close()

