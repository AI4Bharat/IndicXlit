lang_abr=$1
gpu=$2
mkdir ../interactive_data
mkdir ../output
python3 create_interactive_data.py $lang_abr
bash interactive_script.sh $gpu $lang_abr
python3 generate_interactive_translit_pairs.py $lang_abr
