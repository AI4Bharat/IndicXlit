model_path=../../../../../mining_models/indic-en/multi_lang
model_name=mining_model_benchmark_train_9_april_SWE_multi_indic_en

gpu=$1
src_lang=$2

source_lang=$src_lang
target_lang=en
CUDA_VISIBLE_DEVICES=$gpu fairseq-generate ../preprocessed_data_bin \
  --path $model_path/transformer/$model_name/checkpoint_best.pt \
  --task translation_multi_simple_epoch \
  --gen-subset test \
  --beam 4 \
  --nbest 1 \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --batch-size 16448 \
  --num-workers 128 \
  --encoder-langtok "src" \
  --score-reference \
  --lang-dict lang_list.txt \
  --lang-pairs as-en,bn-en,brx-en,gom-en,gu-en,hi-en,kn-en,ks-en,mai-en,ml-en,mni-en,mr-en,ne-en,or-en,pa-en,sa-en,sd-en,si-en,ta-en,te-en,ur-en  > ../output/possible_translit_pair_score_${source_lang}_${target_lang}.txt