model_path=../../../../mining_models/indic-en/multi_lang
model_name=mining_model_benchmark_train_9_april_SWE_multi_indic_en

gpu=$1
source_lang=$2
target_lang=en

CUDA_VISIBLE_DEVICES=$gpu fairseq-interactive $model_path/corpus-bin \
  --path $model_path/transformer/$model_name/checkpoint_best.pt \
  --task translation_multi_simple_epoch \
  --beam 4 \
  --nbest 1 \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --encoder-langtok "src" \
  --buffer-size 8192 \
  --batch-size 8192 \
  --num-workers 128 \
  --lang-dict lang_list.txt \
  --input ../interactive_data/source.$source_lang \
  --lang-pairs as-en,bn-en,brx-en,gom-en,gu-en,hi-en,kn-en,ks-en,mai-en,ml-en,mni-en,mr-en,ne-en,or-en,pa-en,sa-en,sd-en,si-en,ta-en,te-en,ur-en  > ../output/interactive_script_output_${source_lang}_${target_lang}.txt