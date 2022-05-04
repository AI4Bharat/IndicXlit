lang_abr_list=['ur']
lang_list=['Urdu']

for lang, lang_abr in zip(lang_list,lang_abr_list):

	file_lang = open('../unique_word_list_indiccorp/'+lang_abr+'_unique_list_with_freq.csv','r')	
	lines = file_lang.read().split('\n')

	print(len(lines))

	# removing freq
	lines = [ line for line in lines if len(line.split(',')) == 2 ]
	print(len(lines))
	
	lines = [ line.split(',')[0] for line in lines ]

	# removing blank lines
	lines = [ line for line in lines if line ]
	print(len(lines))

	# lower case
	# lines = [line.lower() for line in lines]

	#removing duplicates
	lines = list(set(lines))
	print(len(lines))

	file_lang_out = open('../unique_word_list_indiccorp_filtered/'+lang_abr+'_unique_list_with_freq.csv','w')
	file_lang_out.write('\n'.join(lines))
	file_lang_out.close()
	file_lang.close()
