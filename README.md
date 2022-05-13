<div align="center">
	<h1><b><i>IndicXlit</i></b></h1>
	<a href="https://indicnlp.ai4bharat.org/indic-xlit">Website</a> |
	<a href="#download-indicxlit-model">Downloads</a> |
	<a href="https://arxiv.org/abs/2205.03018">Paper</a><br><br>
</div>

<!-- description about IndicXlit -->

***[IndicXlit](https://indicnlp.ai4bharat.org/indic-xlit)*** is a transformer-based multilingual transliteration model (~11M) for roman to Indic script conversion that ***supports 20 Indic languages***. It is trained on ***[Aksharantar](https://indicnlp.ai4bharat.org/aksharantar/)*** dataset which is the ***largest publicly available parallel corpus containing 26 million word pairs spanning 20 Indic languages*** at the time of writing ( 5 May 2022 ). It supports following 20 Indic languages:

<!-- list the languages IndicXlit supports -->
| <!-- -->  	 | <!-- --> 	  | <!-- --> 	   | <!-- -->	     | <!-- -->       | <!-- -->      |
| -------------- | -------------- | -------------- | --------------- | -------------- | ------------- |
| Assamese (asm) | Hindi (hin) 	  | Maithili (mai) | Marathi (mar)   | Punjabi (pan)  | Tamil (tam)   |
| Bengali (ben)  | Kannada (kan)  | Malayalam (mal)| Nepali (nep)    | Sanskrit (san) | Telugu (tel)  | 
| Bodo(brx)      | Kashmiri (kas) | Manipuri (mni) | Oriya (ori)     | Sindhi (snd)   | Urdu (urd)    |
| Gujarati (guj) | Konkani (gom)  | 




<!-- index with hyperlinks (Table of contents) -->
- [Installation](#installation)
- [Download IndicXlit model](#download-indicxlit-model)
- [Using the model to transliterate the inputs](#using-the-model-to-transliterate-the-inputs)
- [Training the model from scratch with your own dataset](#training-the-model-from-scratch-with-your-own-dataset)
- [Finetuning the model on your input dataset](#finetuning-the-model-on-your-input-dataset)
- [Network and training details](#network-and-training-details)
- [Directory structure](#directory-structure)
- [Citing](#citing)
  - [License](#license)
  - [Contributors](#contributors)
  - [Contact](#contact)



<!-- Installation -->
<!-- installation requirement to run the model -->
## Installation
<details><summary>Click to expand </summary>

```bash
# clone IndicXli repository
git clone https://github.com/AI4Bharat/IndicXlit.git

# install Indicnlp library
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



## Download IndicXlit model
<!-- heperlinks for downloading the models -->
Roman to Indic model [v1.0](https://storage.googleapis.com/indic-xlit-public/final_model/indicxlit-en-indic-v1.0.zip)
<!-- mirror links set up the public drive -->	


## Using the model to transliterate the inputs
The model is trained on words as inputs. hence, users need to split sentence into words before running the transliteratation model when using our command line interface.


Follow the Colab notebook to setup the environment, download the trained _IndicXlit_ model and transliterate your own text.

<!-- colab integratation on running the model on custom input cli script-->
Command line interface --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GFlqA7fpA2LLKJXtbtXSe-DqrAshuB-L?usp=sharing)

<!-- colab integratation on running the model on custom input python script-->
Python interface       --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1P78Tbr6zhe-5LeiKk525N3SGPKn2ofGg?usp=sharing)

The python interface is useful in case you want to reuse the model for multiple translations and do not want to reinitialize the model each time.



<!-- Training model from scratch -->
## Training the model from scratch with your own dataset 	
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1KM8M2hk6fPAI039bBLtHxxojHzo6oMQ7?usp=sharing)
Follow the colab notebook to setup the environment, download the dataset and train the IndicXlit model.


<!-- Finetuning the model on cutom dataset integrate the notebook-->
## Finetuning the model on your input dataset
Finetuning		--> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TurBNE0Pq9_hqEOXps0FXfymsdlJotE0?usp=sharing)

The colab notebook can be used to setup the environment, download the trained IndicXlit model and prepare your custom dataset for funetuning the IndicXlit model.
<!-- code snipet for using the model through Huggingface -->



## Network and training details
<!-- network and training details and link to the paper  -->

- Architecture: IndicXlit uses 6 encoder and decoder layers, input embeddings of size 256 with 4 attention heads and
feedforward dimension of 1024 with total number of parameters of 11M
- Loss: Cross entropy loss
- Optimizer: Adam
- Adam-betas: (0.9, 0.98)
- Peak-learning-rate: 0.001
- Learning-rate-scheduler: inverse-sqrt
- Temperature-sampling (T): 1.5
- Warmup-steps: 4000

Please refer to section 6 of our [paper]() for more details on training setup.


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
```
@article{Madhani2022AksharantarTB,
  title={Aksharantar: Towards building open transliteration tools for the next billion users},
  author={Yash Madhani and Sushane Parthan and Priyanka A. Bedekar and Ruchi Khapra and Vivek Seshadri and Anoop Kunchukuttan and Pratyush Kumar and Mitesh M. Khapra},
  journal={ArXiv},
  year={2022},
  volume={abs/2205.03018}
}
```
We would like to hear from you if:

- You are using our resources. Please let us know how you are putting these resources to use.
- You have any feedback on these resources.


<!-- License -->
### License

The IndicXlit code (and models) are released under the MIT License.



<!-- Contributors -->
### Contributors
 - Yash Madhani <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>
 - Sushane Parthan <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>
 - Priyanka Bedakar <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>
 - Ruchi Khapra <sub> ([AI4Bharat](https://ai4bharat.org)) </sub>
 - Anoop Kunchukuttan <sub> ([AI4Bharat](https://ai4bharat.org), [Microsoft](https://www.microsoft.com/en-in/)) </sub>
 - Pratyush Kumar <sub> ([AI4Bharat](https://ai4bharat.org), [Microsoft](https://www.microsoft.com/en-in/), [IITM](https://www.iitm.ac.in)) </sub>
 - Mitesh M. Khapra <sub> ([AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in)) </sub>



<!-- Contact -->
### Contact
- Anoop Kunchukuttan ([anoop.kunchukuttan@gmail.com](mailto:anoop.kunchukuttan@gmail.com))
- Mitesh Khapra ([miteshk@cse.iitm.ac.in](mailto:miteshk@cse.iitm.ac.in))
- Pratyush Kumar ([pratyush@cse.iitm.ac.in](mailto:pratyush@cse.iitm.ac.in))
