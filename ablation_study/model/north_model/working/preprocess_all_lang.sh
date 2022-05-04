for lang_abr in as bn gom gu hi ks mai mr ne or pa sa sd si ur
do
   fairseq-preprocess \
   --wandb-project transliteration_model \
   --trainpref ../en-$lang_abr/corpus/train --validpref ../en-$lang_abr/corpus/valid --testpref ../en-$lang_abr/corpus/test \
   --srcdict ../multi_lang/corpus-bin/dict.en.txt \
   --tgtdict ../multi_lang/corpus-bin/dict.mlt.txt \
   --source-lang en --target-lang $lang_abr \
   --workers 32 \
   --destdir ../multi_lang/corpus-bin 
done
