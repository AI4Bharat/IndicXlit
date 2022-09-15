#### Following scripts are to transliterate the corpus step by step,
1. indic_tok.py : tokenize the text as per the unicode range given for Indian languages
2. create_ip_word_list.py : Create the unique word list given the corpus
3. interactive.sh : fairseq interactive script 
- lang_list.txt : list of languages supported by IndicXlit (meta file to support interactive script)
4. fairseq_postprocess.py : Postprocess fairseq output and save the output in nice dictionary {source : target}
5. romanize_corpus.py : romanize the corpus in O(n) using the output dictionary.
 
