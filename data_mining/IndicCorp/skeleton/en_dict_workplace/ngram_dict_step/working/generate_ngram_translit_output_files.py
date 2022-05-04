import json
import sys
import itertools

src_lang = sys.argv[1]

f_in = open('../../interactive_step/output/interactive_translit_pairs_'+src_lang+'_en.txt', 'r')
lines_in = f_in.read().split('\n')

ngram_dict = json.load(open('../../../../ngram_dicts_indiccorp/en_ngram_dict.json','r'))

n = 4

lines_out = []
for line in lines_in:
	
	word = line.split('\t')[1]
	lines_out.append(line.split('\t')[0] + '\t' + word)

	word_ngrams_list = [] 
	
	for i in range(len(word) - n + 1 ):	
		word_ngrams_list.append(word[i:i+n])


	word_ngrams_list_subset_3 = list( itertools.combinations(set(word_ngrams_list), 3) )

	for word_ngram_subset in word_ngrams_list_subset_3:
		
		first_ngram_word_list = []
		second_ngram_word_list = []
		third_ngram_word_list = []

		if word_ngram_subset[0] in ngram_dict.keys():
			first_ngram_word_list = ngram_dict[word_ngram_subset[0]]
		if word_ngram_subset[1] in ngram_dict.keys():
			second_ngram_word_list = ngram_dict[word_ngram_subset[1]]
		if word_ngram_subset[2] in ngram_dict.keys():
			third_ngram_word_list = ngram_dict[word_ngram_subset[2]]

		intersection_of_2_list =  set(first_ngram_word_list).intersection(set(second_ngram_word_list)) 
		
		intersection_of_3_list =  list(set(intersection_of_2_list).intersection(set(third_ngram_word_list)) )



		for possible_translit_word in intersection_of_3_list:
				lines_out.append(line.split('\t')[0] + '\t' + possible_translit_word)


lines_out = list(set(lines_out))
f_out = open('../output/ngram_translit_pairs_'+src_lang+'_en.txt', 'w')
f_out.write('\n'.join(lines_out))
f_out.close()
f_in.close()


f_out_rom = open('../output/test.'+'en', 'w')
f_out_nat = open('../output/test.'+src_lang, 'w')

lines_out_nat = [' '.join(line.split('\t')[0]) for line in lines_out]
lines_out_rom = [' '.join(line.split('\t')[1]) for line in lines_out]

f_out_nat.write('\n'.join(lines_out_nat))
f_out_rom.write('\n'.join(lines_out_rom))

f_out_nat.close()
f_out_rom.close()




