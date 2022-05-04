- create output dir 

lang_abr = define language abbreviation

1. python3 generate_ngram_translit_output_files.py $lang_abr
 
- i/p : 
		1. file which has 3 columns as [source word, best candidate, tansliteration score]  (output of 1st step)
		2. ngram dictionary (english)

- o/p : file with all possible pairs => output dir 
		test.en ( space separated character in one line as one roman words ) => output dir
		test.$lang_abr ( space separated character in one line as one native words ) => output dir

