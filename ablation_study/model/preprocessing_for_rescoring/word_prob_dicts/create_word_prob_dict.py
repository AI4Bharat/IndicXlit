import json
import sys
lang_abr = sys.argv[1] 

word_freq_dict = json.load(open('../word_freq_dicts/'+lang_abr+'_word_freq_dict.json','r'))

total_count = 0
for word in word_freq_dict.keys():
    total_count += word_freq_dict[word]

word_prob_dict={}
for word in word_freq_dict.keys():
    word_prob_dict[word] = (word_freq_dict[word]/total_count)

f_out = open(lang_abr+'_word_prob_dict.json','w')

json.dump(word_prob_dict, f_out, indent = 4)

f_out.close()

