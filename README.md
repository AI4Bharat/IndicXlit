<div align="center">
	<h1><b><i>IndicXlit</i></b></h1>
	<a href="">Website</a> |
	<a href="">Paper</a> 
</div>

<!-- description about IndicXlit -->

**IndicXlit** is a transformer-based multilingual transliteration model for roman to indic script conversion that supports 21 indic languages. It is trained on [Aksharantara]() dataset which is the largest publicly available parallel corpus contains 26 million word pairs spanning 21 Indic languages. It supports following 21 Indian languages:

<!-- list the languages IndicXlit supports -->
| -------------- | -------------- | -------------- | --------------- | ------------- | -------------- | ------------ |
| Assamese (asm) | Gujarati (guj) | Kashmiri (kas) | Malayalam (mal) | Nepali (nep)  | Sanskrit (san) | Tamil (tam)  |
| Bengali (ben)  | Hindi (hin) 	  | Konkani (gom)  | Manipuri (mni)  | Oriya (ori)   | Sindhi (snd)   | Telugu (tel) |
| Bodo(brx)      | Kannada (kan)  | Maithili (mai) | Marathi (mar)   | Punjabi (pan) | Sinhala (sin)  | Urdu (urd)   |

<!-- index with hyperlinks (Table of contents) -->
<!-- [Download IndicXlit model]
[Using the model to transliterate the inputs]


[Installation]
[Training model from scratch]

[Finetuning the model] 
	via cloud storage
	via Huggingface

[Network and traning details]

Evaluation result

Corpus details



Directory structure
Citing
	License
	Contributors
	Contact -->







## Download IndicXlit model
<!-- heperlinks for downloading the models -->
<!-- mirror links set up the public drive -->	


## Using the model to transliterate the inputs

The model is trained on single word and hence, users need to split sentence into words before running the transliteratation model when using our command line interface (The python interface has `sentence_transliteration` method to transliterate the sentences ).

Here is an example snippet to split sentence into words for English and Indic languages supported by our model:

<!-- code snippet to preprocess the words to create the model inputs-->
```python
```


Follow the colab notebook to setup the environment, download the trained _IndicXlit_ model and transliterate your own text.

<!-- colab integratation on running the model on custom input cli script-->
Command line interface --> [![Open In Colab](https://colab.research.google.com/drive/1GFlqA7fpA2LLKJXtbtXSe-DqrAshuB-L?usp=sharing)]

<!-- colab integratation on running the model on custom input python script-->
Python interface       --> [![Open In Colab](https://colab.research.google.com/drive/1P78Tbr6zhe-5LeiKk525N3SGPKn2ofGg?usp=sharing)]

The python interface is useful in case you want to reuse the model for multiple translations and do not want to reinitialize the model each time








<!-- Installation -->
## Installation
<details><summary>Click to expand </summary>

```bash
cd IndicXlit
git clone https://github.com/anoopkunchukuttan/indic_nlp_library.git
git clone https://github.com/anoopkunchukuttan/indic_nlp_resources.git
# install required libraries
pip install sacremoses pandas mock sacrebleu tensorboardX pyarrow indic-nlp-library

# Install fairseq from source
git clone https://github.com/pytorch/fairseq.git
cd fairseq
pip install --editable ./

```
</details>

<!-- installation requirement to run the model -->

<!-- Training model from scratch -->
## Training the model from scratch with the Aksharantara dataset 	
[![Open In Colab](https://colab.research.google.com/drive/1KM8M2hk6fPAI039bBLtHxxojHzo6oMQ7?usp=sharing)]



<!-- Finetuning the model on cutom dataset integrate the notebook-->
## Finetuning the model 
Finetuning		--> [![Open In Colab](https://colab.research.google.com/drive/1TurBNE0Pq9_hqEOXps0FXfymsdlJotE0?usp=sharing)]
<!-- code snipet for using the model through Huggingface -->


## Network and traning details
<!-- network and training details and link to the paper  -->

- Architechture: IndicXlit uses 6 encoder and decoder layers, input embeddings of size 256 with 4 attention heads and
feedforward dimension of 1024 with total number of parameters of 11M
- Loss: Cross entropy loss
- Optimizer: Adam
- Warmup_steps: 4000

Please refer to section 6 of our [paper]() for more details on training/experimental setup.




## Evaluation result
<!-- Evaluation results on Dakshina and Benchmark -->

## Corpus details
<!-- details about number of Mining pairs or size of training corpus -->


## Directory structure
<!-- dir structure for the repo -->
```
IndicXlit
├── ablation_study
├── api
├── corpus_preprocessing
│	 └── Collating_existing_dataset
├── data_mining
│	 ├── IndicCorp
│	 │	 ├── preprocess_data
│	 │	 │	 ├── create_ngram_dict.py
│	 │	 │	 ├── filter_data_ks.py
│	 │	 │	 ├── filter_data.py
│	 │	 │	 └── filter_data_ur.py
│	 │	 └── skeleton
│	 │	     └── en_dict_workplace
│	 │	         ├── interactive_step
│	 │	         ├── ngram_dict_step
│	 │	         ├── scoring_pairs_step
│	 │	         	 ├── average_score
│	 │	         	 ├── en_indic_model_scoring
│	 │	         	 ├── indic_en_model_scoring
│	 │	         
│	 └── transliteration_mining_samanantar
│	     ├── align_data.sh
│	     ├── convert_csv.py
│	     ├── extract_translit_pairs.sh
│	     ├── final_output.zip
│	     ├── install_tools.txt
│	     ├── model_run_steps.txt
│	     ├── preprocess_data.py
│	     ├── readme.md
│	     ├── samanantar_pairs_count.xlsx
│	     └── validation_script.py
├── inference
│	 └── cli
├── model_training_scripts
│	 ├── binarizing
│	 ├── data_filtration
│	 │	 ├── combining_data_acrooss_lang.py
│	 │	 ├── refresh_data_train_all_test_valid.py
│	 │	 └── refresh_test_valid_data.py
│	 ├── evaluate
│	 ├── generation
│	 ├── training
│	 └── vocab_creation
└── README.md
```

<!-- citing information -->
## Citing

If you are using any of the resources, please cite the following article:

We would like to hear from you if:

- You are using our resources. Please let us know how you are putting these resources to use.
- You have any feedback on these resources.


<!-- License -->
### License



<!-- Contributors -->
### Contributors
 - Yash Madhani, <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>>
 - Sushane Parthan, <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>>
 - Priyanka Bedakar, <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>>
 - Ruchi Khapra, <sub> ([AI4Bharat](https://ai4bharat.org)) </sub>>
 - Vivek Seshadri, <sub> ([Microsoft](https://www.microsoft.com/en-in/), [Karya Inc.](https://projectkarya.com/)) </sub>>
 - Anoop Kunchukuttan, <sub> ([AI4Bharat](https://ai4bharat.org), [Microsoft](https://www.microsoft.com/en-in/)) </sub>>
 - Pratyush Kumar, <sub> ([AI4Bharat](https://ai4bharat.org), [Microsoft](https://www.microsoft.com/en-in/), [IITM](https://www.iitm.ac.in)) </sub>>
 - Mitesh M. Khapra, <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>>



<!-- Contact -->
### Contact
- Anoop Kunchukuttan ([anoop.kunchukuttan@gmail.com](mailto:anoop.kunchukuttan@gmail.com))
- Mitesh Khapra ([miteshk@cse.iitm.ac.in](mailto:miteshk@cse.iitm.ac.in))
- Pratyush Kumar ([pratyush@cse.iitm.ac.in](mailto:pratyush@cse.iitm.ac.in))