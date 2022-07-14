all_data contains : [existing_data, samanantar, wikidata, IndicCorp_0.35]

en-* dir contains : [corpus, corpus_lang_token, refresh_data_train_all_test_valid.py]
	-corpus : language train data filtered (train data - test and valid native,roman words with all data all languages)
	-corpus_lang_token : lang_token added to source file for each language
	-refresh_data_train_all_test_valid : python script for creating corpus folder (path in files are different but origin data is same as in this folder named "all_data" )

multi_lang : [corpus]
	-corpus : combine data for across all the languages. 

preprocess_data : [adding_lang_tokens.py, combining_data_acrooss_lang.py, refresh_test_valid_data.py]
	-adding_lang_tokens.py :  add lang tokens in train,test,valid files for every language and create corpus_lang_token dir in en-*
	-combining_data_acrooss_lang.py : combine data and create files in corpus dir in multi_lang
	-refresh_test_valid_data.py : create test and valid data for each language in en-*/corpus dir

