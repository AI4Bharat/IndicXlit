fairseq-preprocess \
   --wandb-project transliteration_model \
   --trainpref ../corpus/train  \
   --source-lang en --target-lang mlt \
   --workers 32 \
   --destdir ../corpus-bin
