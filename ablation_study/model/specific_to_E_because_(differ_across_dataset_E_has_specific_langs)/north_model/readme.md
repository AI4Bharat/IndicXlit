create multi_lang/corpus dir 
create multi_lang/output dir 

preprocess_data dir
	- combining_data_acrooss_lang.py : it collates the train data across languages and put it into multi_lang/corpus dir. 
	- refresh_test_valid_data.py : filter test and valid data 

1. multi_lang/working/preprocess.sh 
it will preprocess the combined data saved in multi_lang/corpus dir and create joint dictionary and store in corpus-bin dir. 
- i/p : train files from multi_lang/corpus dir 
- o/p : it will generate the binary files in corpus-bin dir 

2. move all the files except dict* files from corpus-bin dir to some temp dir.  

3. working/preprocess_all_lang.sh
preprocess all the languages separately using joint dict and store all the bin and idx file to multi_lang/corpus-bin dir.

4. create one lang_list.txt file which contains the lang_abr for every languages and store this file in multi_lang/working dir

5. multi_lang/working/train.sh
it will train the model with given config

6. multi_lang/working/generate.sh
it will generate the results in txt file

7. multi_lang/working/generate_result_files.py
it will convert the txt file and create more structured xml result files.

8. multi_lang/working/final_result.sh 
- evaluate the final results and outputs the matrix scores, right predicted word list and wrong predicted word list using 
evaluate_result.py file.
- i/p : results xml file, test xml file
- o/p : evaluation_details.csv, matrix_score.txt, right_predicted_word.txt, wrong_predicted_word.txt


