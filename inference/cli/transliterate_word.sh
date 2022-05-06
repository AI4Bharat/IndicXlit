lang_abr=$1
bash interactive.sh $lang_abr
python3 generate_result_files.py $lang_abr
