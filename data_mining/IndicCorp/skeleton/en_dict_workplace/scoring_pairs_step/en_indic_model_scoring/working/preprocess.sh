model_path=../../../../../mining_models/en-indic/multi_lang

tgt_lang=$1

fairseq-preprocess \
   --wandb-project transliteration_model \
   --testpref ../../../ngram_dict_step/output/test  \
   --source-lang en --target-lang $tgt_lang \
   --srcdict $model_path/corpus-bin/dict.en.txt \
   --tgtdict $model_path/corpus-bin/dict.$tgt_lang.txt \
   --destdir ../preprocessed_data_bin \
   --workers 64 
