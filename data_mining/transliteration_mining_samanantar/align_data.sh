/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/tools/mosesdecoder/scripts/training/train-model.perl -root-dir /home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/workplace/en-mr/align_data \
     -corpus /home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/workplace/en-mr/corpus/train \
     -f mr -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
     -mgiza -mgiza-cpus 32 \
     -lm 0:3:/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/workplace/en-mr/lm/train.arpa.en:8 \
     -external-bin-dir /home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/tools/mgiza/mgizapp/bin \
     -first-step 1 -last-step 4


