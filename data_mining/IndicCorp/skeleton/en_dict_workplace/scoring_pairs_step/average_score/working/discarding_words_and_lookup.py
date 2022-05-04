import json
import sys
lang_abr = sys.argv[1]

# discarding words windicch have ranked more than 5 for each indic word and mixing the scores across 2 dicts.

dict_indic_en = json.load(open('../output/translit_pairs_dict_'+lang_abr+'_en.json','r'))

dict_en_indic = json.load(open('../output/translit_pairs_dict_en_'+lang_abr+'.json','r'))


lines_translit_pairs = [] 

# lookup and taking the average of score and writing to a new file.
for indic_word_indic_en in dict_indic_en.keys():	
	if indic_word_indic_en in dict_en_indic.keys():
		for en_word_tuple_indic_en in dict_indic_en[indic_word_indic_en]:
			for en_word_tuple_en_indic in dict_en_indic[indic_word_indic_en]:
				if en_word_tuple_indic_en[0] == en_word_tuple_en_indic[0]:
					avg_score = (en_word_tuple_indic_en[1] + en_word_tuple_en_indic[1])/2
					lines_translit_pairs.append(indic_word_indic_en + '\t' + en_word_tuple_indic_en[0] + '\t' + str(avg_score))


dict_avg_score = {}

for line in lines_translit_pairs:
	indic_word = line.split('\t')[0]
	if indic_word in dict_avg_score.keys():
		dict_avg_score[indic_word].append( ( line.split('\t')[1] , float(line.split('\t')[2]) ) )
	else:
		dict_avg_score[indic_word] = [ ( line.split('\t')[1] , float(line.split('\t')[2]) ) ]



# sorting the en words as per the scores in descending order
for indic_word in dict_avg_score.keys():
	dict_avg_score[indic_word].sort(key = lambda x : float(x[1]) ,reverse = True)

# discard the words windicch are not in top 5 rank.
top = 5
for indic_word in dict_avg_score.keys():
	dict_avg_score[indic_word] = dict_avg_score[indic_word][:top]


lines_translit_pairs_avg_score = []
for indic_word in dict_avg_score.keys():	
	for en_word_tuple in dict_avg_score[indic_word]:			
		lines_translit_pairs_avg_score.append(indic_word + '\t' + en_word_tuple[0] + '\t' + str(en_word_tuple[1]))


lines_translit_pairs_avg_score.sort(key = lambda x : float( x.split('\t')[2] ) ,reverse = True)

file_translit_pairs_avg_score = open('../output/translit_pairs_with_avg_score_'+lang_abr+'.txt','w')
file_translit_pairs_avg_score.write('\n'.join(lines_translit_pairs_avg_score))
file_translit_pairs_avg_score.close()
