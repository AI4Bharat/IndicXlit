1. proprocess the IndicCorp data as normailizing + tokenizing
- python3 preprocess_indiccorp_data/preprocess_indiccorp_data.py $lang_abr

2. First create word frequency dictionary
- python3 word_freq_dicts/create_word_freq_dict.py $lang_abr

3. create word probablity dictionary
- python3 word_prob_dicts/create_word_prob_dict.py $lang_abr