lang_abr=$1
python3 ../evaluate_result_with_rescore_option.py \
-i ../../output_nbest_10/translit_result_$lang_abr.xml \
-t ../../output_nbest_10/translit_test_$lang_abr.xml  \
--result-dict-file ../../output_nbest_10/result_dict_$lang_abr.json  \
--rescoring  \
--rescoring-method weighted_avg  \
--alpha 0.9  \
--word-prob-dict-file "../../../../../preprocessing_for_rescoring/word_prob_dicts/"$lang_abr"_word_prob_dict.json"  \
-o ../../output_nbest_10/evaluation_details_with_rescoring_$lang_abr.csv \
--acc-matrix-output-file ../../output_nbest_10/matrix_score_with_rescoring_$lang_abr.txt \
--correct-predicted-words-file  ../../output_nbest_10/correct_predicted_words_with_rescoring_$lang_abr.txt \
--wrong-predicted-words-file  ../../output_nbest_10/wrong_predicted_words_with_rescoring_$lang_abr.txt
