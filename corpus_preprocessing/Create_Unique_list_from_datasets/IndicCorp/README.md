1. `Create_Smaller_Text_Files` splits the huge IndicCorp native text file in to smaller text files and also runs `GCLD3` on it to remove non-language characters.
2. We then convert text files to CSV performing various pre-processing steps.
3. We need dataset which doesn't include SWE (Samanantar, Wikidata, Existing) data. We use `Consolidate_SWE` and `Join_My_Dict`.
