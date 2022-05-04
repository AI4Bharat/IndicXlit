lang_abr=$1
CUDA_VISIBLE_DEVICES=$2 fairseq-train ../en-$lang_abr/corpus-bin  \
--wandb-project transliteration_model  \
--save-dir ../en-$lang_abr/transformer/fr_mono_E_$lang_abr  \
--decoder-normalize-before --encoder-normalize-before \
--activation-fn gelu --adam-betas "(0.9, 0.98)" \
--arch transformer \
--batch-size 256 \
--decoder-attention-heads 4 --decoder-embed-dim 256 --decoder-ffn-embed-dim 1024 --decoder-layers 6 \
--dropout 0.5 \
--encoder-attention-heads 4 --encoder-embed-dim 256 --encoder-ffn-embed-dim 1024 --encoder-layers 6 \
--lr 0.001 --lr-scheduler inverse_sqrt \
--max-epoch 100 \
--optimizer adam \
--num-workers 32 \
--warmup-init-lr 0 --warmup-updates 4000
