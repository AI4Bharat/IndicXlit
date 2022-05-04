lang_abr=$1
gpu=$2
cd interactive_step/working/
cat temp.sh
bash temp.sh $lang_abr $gpu
cd ../../ngram_dict_step/working/
python3 generate_ngram_translit_output_files.py $lang_abr
cd ../../scoring_pairs_step/en_indic_model_scoring/working/
cat temp.sh
bash temp.sh $lang_abr $gpu
cd ../../indic_en_model_scoring/working/
cat temp.sh 
bash temp.sh $lang_abr $gpu
cd ../../average_score/working/
cat temp.sh 
bash temp.sh $lang_abr