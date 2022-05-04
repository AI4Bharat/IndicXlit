all_data contains : [existing_data, samanantar, wikidata]

en-* dir contains : [corpus, corpus_lang_token, refresh_data_train_all_test_valid.py]
	-corpus : language train data filtered (train data - test and valid native,roman words with all data all languages)
	-corpus_lang_token : lang_token added to source file for each language
	-refresh_data_train_all_test_valid : python script for creating corpus folder

multi_lang : [corpus]
	-corpus : combine data for across all the languages. 

preprocess_data : [adding_lang_tokens.py, combining_data_acrooss_lang.py, refresh_test_valid_data.py]
	-refresh_test_valid_data.py : create test and valid data for each language in en-*/corpus dir

