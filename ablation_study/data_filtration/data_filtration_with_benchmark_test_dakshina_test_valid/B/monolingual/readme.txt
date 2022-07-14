all_data contains : [existing_data, samanantar, wikidata]

en-* dir contains : [corpus, refresh_data_train_all_test_valid.py]
	-corpus : language train data filtered (train data - test and valid native,roman words)

	-refresh_data_train_all_test_valid : python script for creating corpus folder

preprocess_data : [refresh_test_valid_data.py]
	-refresh_test_valid_data.py : create test and valid data for each language in en-*/corpus dir

