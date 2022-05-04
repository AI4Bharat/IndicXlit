lang_abr=$1
gpu=$2
mkdir ../output
bash preprocess.sh $lang_abr
bash generate.sh $gpu $lang_abr
python3 generate_result_score_flie.py $lang_abr
