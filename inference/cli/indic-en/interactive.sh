source_lang=$1
target_lang=en
input_file=$2
beam=$3
nbest=$4

fairseq-interactive corpus-bin \
  --path transformer/indicxlit.pt \
  --task translation_multi_simple_epoch \
  --beam $beam \
  --nbest $nbest \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --encoder-langtok "src" \
  --lang-dict lang_list.txt \
  --input $input_file \
  --lang-pairs as-en,bn-en,brx-en,gom-en,gu-en,hi-en,kn-en,ks-en,mai-en,ml-en,mni-en,mr-en,ne-en,or-en,pa-en,sa-en,sd-en,si-en,ta-en,te-en,ur-en  > output/${source_lang}_${target_lang}.txt