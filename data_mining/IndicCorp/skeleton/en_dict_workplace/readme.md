### Preprocess data
- Follow the link below to preprocess the required data to mine the pairs from IndicCorp, 
https://github.com/AI4Bharat/IndicXlit/tree/master/data_mining/IndicCorp/preprocess_data

### 1. Intractive step

- In this step we take all the unique native(e.g. hindi) words from IndicCorp monolingual corpora and pass it through the Indic-En model and predict the transliteration candidate.

- output would be hi-en pairs { number of pairs will be same as number of unique words in unique native(e.g. Hindi) list from IndicCorp }


### 2. Ngram_dict_step

- In this step we create ngram (e.g 4-gram) dictionary from the IndicCorp unique word list where key is ngram word and value as the list of words which contains that ngram in it. script: https://github.com/AI4Bharat/IndicXlit/blob/master/data_mining/IndicCorp/preprocess_data/create_ngram_dict.py

- Now, take all the words from ngram english dictionary for each english word (corresponding to hi-en pair <- output of interactive step) which have atleast 3 ngram (e.g 4-gram) in common. (common ngram => between english predicted word and ngram english dictionary words) 

- e.g.	
	1. let's take one hi-en pair (output of interactive step)
	2. now separate en word from hi-en pair.
	3. find new en words from ngram english dictionary which are simillar to this en word from 2nd step. (we say words are simillar if atleast 3 ngrams are overlapping b/w two words. )

- create new hi-en pairs from this simillar new english words collected from ngram english dictionary for each hi word.

### 3. Scoring_pairs_step

- Now in this step we score the hi-en pair with both model in both direction [ Indic-En and En-Indic ]  

- pass all hi-en pairs to Indic-En model (src_word = hi , tgt_word = en) and score all the pairs.

- pass all this hi-en pairs in reverse direction to En-Indic model (src_word = en , tgt_word = hi) and score all the pairs.

- take the average of both the score of all the pairs 

- here for each hi word we will have more than one english word and their corresponding tranlsiteration score

- now create the dictionary where the key is Indic word and value as a list of tuple of ( transliteration candidate , corresponding transliteration score ).

- sort the list of each key (Indic word) in the dictionary in descending order with the respect to transliteration score.

- then take atmost top (eg. top=5) transliterated words for each Indic word and discard all the reamining en words in the list.

- take all the words from the dictionary and create the list of hi-en pairs.

- sort the list in in descending order.

- Analyse the data and decide one threshold above which all the pairs are of good quality.
