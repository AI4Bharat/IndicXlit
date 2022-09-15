source_lang=$1
target_lang=en
input_file='../'$source_lang'/'$source_lang'_unique_word_list.txt'
beam=$2
nbest=$3

fairseq-interactive ../indic-en-indicxlit-model/corpus-bin \
  --path ../indic-en-indicxlit-model/transformer/indicxlit.pt \
  --task translation_multi_simple_epoch \
  --beam $beam \
  --nbest $nbest \
  --buffer-size 512 \
  --batch-size 512 \
  --skip-invalid-size-inputs-valid-test \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --encoder-langtok "src" \
  --lang-dict lang_list.txt \
  --input $input_file \
  --lang-pairs as-en,bn-en,brx-en,gom-en,gu-en,hi-en,kn-en,ks-en,mai-en,ml-en,mni-en,mr-en,ne-en,or-en,pa-en,sa-en,sd-en,si-en,ta-en,te-en,ur-en  > '../'$source_lang'/fairseq_op_'${source_lang}'_'${target_lang}'.txt'