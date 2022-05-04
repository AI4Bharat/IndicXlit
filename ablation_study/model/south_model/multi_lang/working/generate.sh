gpu=$1
for lang_abr in kn ml ta te
do
source_lang=en
target_lang=$lang_abr
CUDA_VISIBLE_DEVICES=$gpu fairseq-generate ../corpus-bin \
  --path ../transformer/fr_multi_SWE/checkpoint_best.pt \
  --task translation_multi_simple_epoch \
  --gen-subset test \
  --beam 4 \
  --nbest 4 \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --batch-size 4096 \
  --encoder-langtok "tgt" \
  --lang-dict lang_list.txt \
  --num-workers 64 \
  --lang-pairs en-kn,en-ml,en-ta,en-te  > ../output/${source_lang}_${target_lang}.txt
done
