lang_abr=$1
python3 ../evaluate_result_with_rescore_option.py \
-i ../../en-$lang_abr/output_nbest_10/translit_result.xml \
-t ../../en-$lang_abr/output_nbest_10/translit_test.xml  \
-o ../../en-$lang_abr/output_nbest_10/evaluation_details.csv \
--acc-matrix-output-file ../../en-$lang_abr/output_nbest_10/matrix_score.txt \
--correct-predicted-words-file ../../en-$lang_abr/output_nbest_10/correct_predicted_words.txt \
--wrong-predicted-words-file ../../en-$lang_abr/output_nbest_10/wrong_predicted_words.txt
