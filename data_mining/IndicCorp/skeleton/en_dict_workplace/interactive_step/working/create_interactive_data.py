import sys
src_lang = sys.argv[1]

file_lang = open('../../../../unique_word_list_indiccorp_filtered/'+src_lang+'_unique_list_with_freq.csv','r')	
lines = file_lang.read().split('\n')

print(len(lines))
lines = [' '.join(list(line)) for line in lines]

file_lang_out = open('../interactive_data/source.'+src_lang,'w')
file_lang_out.write('\n'.join(lines))
file_lang_out.close()
