import json

#lang_abr_list = ['as', 'bn', 'en',  'gu', 'hi', 'kn', 'ml', 'mr', 'or', 'pa', 'ta', 'te']
#lang_list = ['Assamese', 'Bangla', 'English' ,'Gujarati', 'Hindi', 'Kannada' ,'Malayalam', 'Marathi' ,'Oriya', 'Punjabi', 'Tamil', 'Telugu']

#lang_abr_list = ['sa','ne','gom']
#lang_list = ['Sanskrit','Nepali','Konkani']

lang_abr_list=['brx', 'mai', 'sat', 'sd', 'ur']
lang_list=['Bodo', 'Maithili', 'Santali', 'Sindhi', 'Urdu']


#define n gram
n = 4

for lang, lang_abr in zip(lang_list,lang_abr_list):

	file_lang = open('/home/yashkm/indic-xlit/monolingual_corpora_mining/ngram_dict_approach/unique_word_list_indiccorp_filtered/'+lang_abr+'_unique_list_with_freq.csv','r')
	word_list = file_lang.read().split('\n')

	ngram_dict = {}
	for word in word_list:
		for i in range(len(word) - n + 1 ):
			
			ngram_word = word[i:i+n]

			if ngram_word in ngram_dict.keys():
				ngram_dict[ngram_word].append(word)
			else:
				ngram_dict[ngram_word]= [word,]

	print(len(ngram_dict.keys()))
	f_ngram_dict_out = open('/home/yashkm/indic-xlit/monolingual_corpora_mining/ngram_dict_approach/ngram_dicts_indiccorp/'+lang_abr+'_ngram_dict.json','w')

	json.dump(ngram_dict, f_ngram_dict_out, indent = 4)

	f_ngram_dict_out.close()
	file_lang.close()
