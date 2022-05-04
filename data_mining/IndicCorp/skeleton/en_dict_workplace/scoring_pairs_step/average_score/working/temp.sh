lang_abr=$1
python3 creating_translit_pairs_dict.py $lang_abr
python3 discarding_words_and_lookup.py $lang_abr
