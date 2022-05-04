lang_abr=$1
python3 ../evaluate_result_with_rescore_option.py \
-i ../../en-$lang_abr/output_nbest_10/translit_result.xml \
-t ../../en-$lang_abr/output_nbest_10/translit_test.xml  \
--result-dict-file ../../en-$lang_abr/output_nbest_10/result_dict_$lang_abr.json  \
--rescoring  \
--rescoring-method weighted_avg  \
--alpha 0.9  \
--word-prob-dict-file "../../../../preprocessing_for_rescoring/word_prob_dicts/"$lang_abr"_word_prob_dict.json"  \
-o ../../en-$lang_abr/output_nbest_10/evaluation_details_with_rescoring.csv \
--acc-matrix-output-file ../../en-$lang_abr/output_nbest_10/matrix_score_with_rescoring.txt \
--correct-predicted-words-file ../../en-$lang_abr/output_nbest_10/correct_predicted_words_with_rescoring.txt \
--wrong-predicted-words-file ../../en-$lang_abr/output_nbest_10/wrong_predicted_words_with_rescoring.txt
