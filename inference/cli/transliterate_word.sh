lang_abr=$1
input_file=$2
beam=$3
nbest=$4
rerank=$5
bash interactive.sh $lang_abr $input_file $beam $nbest 
python3 generate_result_files.py $lang_abr $rerank
