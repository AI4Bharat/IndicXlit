- create interactive_data dir
- create output dir 

lang_abr = define language abbreviation
gpu = gpu number


1. python3 working/create_interactive_data.py $lang_abr
creates source file 
- i/p : list of words
- o/p : space separated character in one line as one word => dir interactive_data


2. bash working/interactive_script.sh $gpu $lang_abr
pass the source list to model to predict the tansliterations for words
- i/p : space separated character in one line as one word
- o/p : model output file [source word, predicted candidates, tansliteration score] => dir output

3. python3 working/generate_interactive_translit_pairs.py $lang_abr
create a file which has 3 columns as [source word, best candidate, tansliteration score]
- i/p : model output file
- o/p : file which has 3 columns as [source word, best candidate, tansliteration score] => dir output
