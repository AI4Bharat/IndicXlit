fairseq-preprocess \
   --wandb-project transliteration_model \
   --trainpref ../corpus/train  \
   --source-lang en --target-lang mlt \
   --workers 256 \
   --destdir ../corpus-bin
