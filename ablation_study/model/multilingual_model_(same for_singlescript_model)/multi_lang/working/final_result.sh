lang_abr=$1
python3 evaluate_result_with_rescore_option.py \
-i ../output/translit_result_$lang_abr.xml \
-t ../output/translit_test_$lang_abr.xml  \
--result-dict-file ../output/result_dict_$lang_abr.json  \
--rescoring  \
--rescoring-method weighted_avg  \
--alpha 0.9  \
--word-prob-dict-file "../../../../preprocessing_for_rescoring/word_prob_dicts/"$lang_abr"_word_prob_dict.json"  \
-o ../output/evaluation_details_with_rescoring_$lang_abr.csv \
--acc-matrix-output-file ../output/matrix_score_with_rescoring_$lang_abr.txt \
--correct-predicted-words-file  ../output/correct_predicted_words_with_rescoring_$lang_abr.txt \
--wrong-predicted-words-file  ../output/wrong_predicted_words_with_rescoring_$lang_abr.txt
