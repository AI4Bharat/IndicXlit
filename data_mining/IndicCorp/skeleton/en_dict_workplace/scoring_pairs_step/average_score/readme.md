- create output dir 

lang_abr = define language abbreviation

lang_abr=$1
python3 discarding_words_and_lookup.py $lang_abr

1. python3 creating_translit_pairs_dict.py $lang_abr
creating dictionary from text file which has source word as key and value as tuple of (predicted_transliteration candidate, transliteration score)
- i/p : file which has 3 columns as [source word, best candidate, tansliteration score] 
- o/p : dictionary (as described above)


2. python3 discarding_words_and_lookup.py $lang_abr
average the score of transliteration pair in the both the direction and select atmost top 5 transliteration pairs for each indic word and output a file which has 3 columns as [source word, best candidate, tansliteration score] in sorted order in descending order.
- i/p : dictionary of output step 1
- o/p : 3 columns as [source word, best candidate, tansliteration score] sorted in descending order w.r.t. transliteration score
