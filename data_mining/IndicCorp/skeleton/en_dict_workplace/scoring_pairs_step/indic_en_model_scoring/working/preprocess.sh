model_path=../../../../../mining_models/indic-en/multi_lang

src_lang=$1

fairseq-preprocess \
   --wandb-project transliteration_model \
   --testpref ../../../ngram_dict_step/output/test  \
   --source-lang $src_lang --target-lang en \
   --srcdict $model_path/corpus-bin/dict.$src_lang.txt \
   --tgtdict $model_path/corpus-bin/dict.en.txt \
   --destdir ../preprocessed_data_bin \
   --workers 128
