lang_abr=$1
python3 evaluate_result_with_rescore_option.py \
-i ../output/translit_result_$lang_abr.xml \
-t ../output/translit_test_$lang_abr.xml  \
-o ../output/evaluation_details_$lang_abr.csv \
--acc-matrix-output-file ../output/matrix_score_$lang_abr.txt \
--correct-predicted-words-file  ../output/correct_predicted_words_$lang_abr.txt \
--wrong-predicted-words-file  ../output/wrong_predicted_words_$lang_abr.txt
