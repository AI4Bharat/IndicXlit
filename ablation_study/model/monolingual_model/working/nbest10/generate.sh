lang_abr=$1
CUDA_VISIBLE_DEVICES=$2 fairseq-generate ../../en-$lang_abr/corpus-bin \
	--path ../../en-$lang_abr/transformer/fr_mono_SWE_$lang_abr/checkpoint_best.pt \
	--beam 10 \
	--remove-bpe \
	--nbest 10 \
	--batch-size 2048 \
	--num-workers 32 \
	--results-path ../../en-$lang_abr/output_nbest_10
