source_lang=en
target_lang=$1

fairseq-interactive corpus-bin \
  --path transformer/indicxlit.pt \
  --task translation_multi_simple_epoch \
  --beam 4 \
  --nbest 1 \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --encoder-langtok "tgt" \
  --lang-dict lang_list.txt \
  --input "source/source.txt" \
  --lang-pairs en-as,en-bn,en-brx,en-gom,en-gu,en-hi,en-kn,en-ks,en-mai,en-ml,en-mni,en-mr,en-ne,en-or,en-pa,en-sa,en-sd,en-si,en-ta,en-te,en-ur  > output/${source_lang}_${target_lang}.txt