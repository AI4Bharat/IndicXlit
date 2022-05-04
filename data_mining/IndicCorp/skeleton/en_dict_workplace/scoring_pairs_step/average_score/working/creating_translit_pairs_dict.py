# creating dictionary for transliteration pairs where key is indicndi_word and value is list of (english word , score)

import json
import sys

lang_abr = sys.argv[1]

f_indic_en = open('../../indic_en_model_scoring/output/possible_translit_pairs_with_score_'+lang_abr+'_en.txt','r')
lines_indic_en = f_indic_en.read().split('\n')
dict_indic_en = {}

for line in lines_indic_en:
	indic_word = line.split('\t')[0]
	if indic_word in dict_indic_en.keys():
		dict_indic_en[indic_word].append( ( line.split('\t')[1] , float(line.split('\t')[2]) ) )
	else:
		dict_indic_en[indic_word] = [ ( line.split('\t')[1] , float(line.split('\t')[2]) ) ]


f_indic_en_out = open('../output/translit_pairs_dict_'+lang_abr+'_en.json','w')

json.dump(dict_indic_en, f_indic_en_out, indent = 4)

f_indic_en_out.close()
f_indic_en.close()







f_en_indic = open('../../en_indic_model_scoring/output/possible_translit_pairs_with_score_en_'+lang_abr+'.txt','r')

lines_en_indic = f_en_indic.read().split('\n')
dict_en_indic = {}

for line in lines_en_indic:
	indic_word = line.split('\t')[1]
	if indic_word in dict_en_indic.keys():
		dict_en_indic[indic_word].append( ( line.split('\t')[0] , float(line.split('\t')[2]) ) )
	else:
		dict_en_indic[indic_word] = [ ( line.split('\t')[0] , float(line.split('\t')[2]) ) ]


f_en_indic_out = open('../output/translit_pairs_dict_en_'+lang_abr+'.json','w')

json.dump(dict_en_indic, f_en_indic_out, indent = 4)

f_en_indic_out.close()
f_en_indic.close()
