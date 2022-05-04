lang_abr=$1
fairseq-preprocess \
  --wandb-project transliteration_model \
  --trainpref ../en-$lang_abr/corpus/train --validpref ../en-$lang_abr/corpus/valid --testpref ../en-$lang_abr/corpus/test \
  --source-lang en --target-lang $lang_abr \
  --workers 32 \
  --destdir ../en-$lang_abr/corpus-bin
