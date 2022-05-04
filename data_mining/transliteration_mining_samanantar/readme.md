# Mining transliteration pairs from parallel translation corpus using Moses toolkit
- To install the toolkit follow the guidelines from install_tools.txt
- To preprocess the dataset (Normalization + tokenisation) run preprocess_data.py file with setting appropriate path in the script
- To align the parallel translation corpus run align.sh script with setting up appropriate path in the script
- To extract the transliteration pairs from parallel translation corpus using alignments run extract_translit_pair.sh script with setting up appropriate path in the script
- Follow steps in model_run_steps.txt for running model on local machine or server

## Samanantar alignments and mined transliteration pairs
- https://console.cloud.google.com/storage/browser/samanantar-alignments-transliteration-pairs;tab=objects?forceOnBucketsSortingFiltering=false&project=ai4b-word-embeddings

## VM Image for en-bn language with installed moses toolkit
- https://console.cloud.google.com/compute/imagesDetail/projects/ai4b-word-embeddings/global/images/moses-alignment-and-transliteration-pairs?project=ai4b-word-embeddings
