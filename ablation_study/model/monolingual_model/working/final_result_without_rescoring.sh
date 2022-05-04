lang_abr=$1
python3 evaluate_result_with_rescore_option.py \
-i ../en-$lang_abr/output/translit_result.xml \
-t ../en-$lang_abr/output/translit_test.xml  \
-o ../en-$lang_abr/output/evaluation_details.csv \
--acc-matrix-output-file ../en-$lang_abr/output/matrix_score.txt \
--correct-predicted-words-file ../en-$lang_abr/output/correct_predicted_words.txt \
--wrong-predicted-words-file ../en-$lang_abr/output/wrong_predicted_words.txt
