lang_abr=$1
python3 evaluate_result_with_rescore_option.py \
-i ../en-$lang_abr/output/translit_result.xml \
-t ../en-$lang_abr/output/translit_test.xml  \
--result-dict-file ../en-$lang_abr/output/result_dict_$lang_abr.json  \
--rescoring  \
--rescoring-method weighted_avg  \
--alpha 0.9  \
--word-prob-dict-file "../../../preprocessing_for_rescoring/word_prob_dicts/"$lang_abr"_word_prob_dict.json"  \
-o ../en-$lang_abr/output/evaluation_details_with_rescoring.csv \
--acc-matrix-output-file ../en-$lang_abr/output/matrix_score_with_rescoring.txt \
--correct-predicted-words-file ../en-$lang_abr/output/correct_predicted_words_with_rescoring.txt \
--wrong-predicted-words-file ../en-$lang_abr/output/wrong_predicted_words_with_rescoring.txt
