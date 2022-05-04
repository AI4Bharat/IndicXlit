import json
import sys
lang_abr = sys.argv[1] 

f_in = open('/preprocess_indiccorp_data/'+lang_abr+'.tok.txt','r')
lines_in = f_in.read().split('\n')
lines_in = [line for line in lines_in if line]

word_dict = {}

for line in lines_in:
	word_list = line.split(' ')
	for word in word_list:
		if word in word_dict.keys():
			word_dict[word] += 1
		else:
			word_dict[word] = 1

f_out = open(lang_abr+'_word_freq_dict.json','w')

json.dump(word_dict, f_out, indent = 4)

f_out.close()
f_in.close()

