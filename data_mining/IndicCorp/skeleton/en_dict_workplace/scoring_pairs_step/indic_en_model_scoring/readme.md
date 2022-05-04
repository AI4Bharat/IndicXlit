- create output dir 

lang_abr = define language abbreviation
gpu = gpu number

1. bash preprocess.sh $lang_abr
preprocess the data 
- i/p : test.en ( space separated character in one line as one roman words )
		test.$lang_abr ( space separated character in one line as one native words )
- o/p : binary files (.bin and .idx file) => dir preprocessed_data_bin

2. bash generate.sh $gpu $lang_abr with --score-reference argument
predict the tansliteration score for pairs
- i/p : binary files 
- o/p : model output file [source word, predicted candidates, tansliteration score] => dir output

3. python3 generate_result_score_flie.py $lang_abr
create a file which has 3 columns as [source word, best candidate, tansliteration score]
- i/p : model output file
- o/p : file which has 3 columns as [source word, best candidate, tansliteration score] => dir output
