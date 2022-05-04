
1. preprocess_data.sh
- It preprocess the data using fairseq-preprcess and stores the output in corpus-bin dir which contains bin and idx files.
- i/p : trian, test, valid files in corpus dir where each file contains word as space separated characters in one line. 
- o/p : bin and idx files in corpus-bin dir

2. train.sh
- train the model with given configuration
- i/p : corpus-bin dir
- o/p : model checkpoints

3. generate.sh
- generate the results on test set which contains the source word, transliteration candidates and transliteration score
- i/p : corpus-bin dir and best model checkpoint 
- o/p : results in txt file

4. generate_result_files.py
- extract the results from text file and create structured xml file
- i/p : results in txt file
- o/p : results in xml file 

5. final_result.sh 
- evaluate the final results and outputs the matrix scores, right predicted word list and wrong predicted word list using 
evaluate_result.py file.
- i/p : results xml file, test xml file
- o/p : evaluation_details.csv, matrix_score.txt, right_predicted_word.txt, wrong_predicted_word.txt
