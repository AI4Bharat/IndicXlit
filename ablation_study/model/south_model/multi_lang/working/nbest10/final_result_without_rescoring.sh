lang_abr=$1
python3 ../evaluate_result_with_rescore_option.py \
-i ../../output_nbest_10/translit_result_$lang_abr.xml \
-t ../../output_nbest_10/translit_test_$lang_abr.xml  \
-o ../../output_nbest_10/evaluation_details_$lang_abr.csv \
--acc-matrix-output-file ../../output_nbest_10/matrix_score_$lang_abr.txt \
--correct-predicted-words-file  ../../output_nbest_10/correct_predicted_words_$lang_abr.txt \
--wrong-predicted-words-file  ../../output_nbest_10/wrong_predicted_words_$lang_abr.txt
