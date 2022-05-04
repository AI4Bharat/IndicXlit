gpu=$1
for lang_abr in bn gom gu hi mai mr pa sd si ur
do
source_lang=en
target_lang=$lang_abr
CUDA_VISIBLE_DEVICES=$gpu fairseq-generate ../../corpus-bin \
  --path ../../transformer/fr_north_E/checkpoint_best.pt \
  --task translation_multi_simple_epoch \
  --gen-subset test \
  --beam 10 \
  --nbest 10 \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --batch-size 4096 \
  --encoder-langtok "tgt" \
  --lang-dict ../lang_list.txt \
  --num-workers 64 \
  --lang-pairs en-bn,en-gom,en-gu,en-hi,en-mai,en-mr,en-pa,en-sd,en-si,en-ur  > ../../output_nbest_10/${source_lang}_${target_lang}.txt
done
