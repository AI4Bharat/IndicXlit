<div align="center">
	<h1><b><i>IndicXlit</i></b></h1>
	<a href="https://indicnlp.ai4bharat.org/indic-xlit">Website</a> |
	<a href="#download-indicxlit-model">Downloads</a> |
	<a href="https://arxiv.org/abs/2205.03018">Paper</a> |
  <a href="https://xlit.ai4bharat.org/">Demo</a> |
  <a href="https://pypi.org/project/ai4bharat-transliteration">Python Library</a>
  <br><br>
</div>

<!-- description about IndicXlit -->

***[IndicXlit](https://indicnlp.ai4bharat.org/indic-xlit)*** is a transformer-based multilingual transliteration model (~11M) for roman to native script conversion that ***supports 21 Indic languages***. It is trained on ***[Aksharantar](https://indicnlp.ai4bharat.org/aksharantar/)*** dataset which is the ***largest publicly available parallel corpus containing 26 million word pairs spanning 20 Indic languages*** at the time of writing (5 May 2022). It supports following 21 Indic languages:

<!-- list the languages IndicXlit supports -->
| <!-- -->  	 | <!-- --> 	  | <!-- --> 	   | <!-- -->	     | <!-- -->       | <!-- -->      |
| -------------- | -------------- | -------------- | --------------- | -------------- | ------------- |
| Assamese (asm) | Bengali (ben)  |  Bodo (brx)    | Gujarati (guj)  | Hindi (hin)    | Kannada (kan) |
| Kashmiri (kas) | Konkani (gom)  | Maithili (mai) | Malayalam (mal) | Manipuri (mni) | Marathi (mar) | 
| Nepali (nep)   | Oriya (ori)    | Punjabi (pan)  |  Sanskrit (san) | Sindhi (snd)   | Sinhala (sin) |
|  Tamil (tam)   |  Telugu (tel)  |   Urdu (urd)   | 

### Evaluation Results

IndicXlit is evaluated on [Dakshina benchmark](https://github.com/google-research-datasets/dakshina) and [Aksharantar benchmark](https://indicnlp.ai4bharat.org/aksharantar/). IndicXlit achieves state-of-theart results on the Dakshina testset and also
provide baseline results on the new Aksharantar testset. The Top-1 results are summarized below. For more details, refer [paper](https://arxiv.org/abs/2205.03018)


| languages | asm | ben | brx | guj | hin | kan | kas | kok | mai | mal | mni | mar | nep | ori | pan | san | tam | tel | urd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dakshina | - | 55.49 | - | 62.02 | 60.56 | 77.18 | - | - | - | 63.56 | - | 64.85 | - | - | 47.24 | - | 68.10 | 73.38 | 42.12 | 61.45 |
| Aksharantar (native words) | 60.27 | 61.70 | 70.79 | 61.89 | 55.59 | 76.18 | 28.76 | 63.06 | 72.06 | 64.73 | 83.19 | 63.72 | 80.25 | 58.90 | 40.27 | 78.63 | 69.78 | 84.69 | 48.37 |
| Aksharantar (named entities) | 38.62 | 37.12 | 30.32 | 48.89 | 58.87 | 49.92 | 20.23 | 34.36 | 42.82 | 33.93 | 44.12 | 53.57 | 52.67 | 30.63 | 36.08 | 24.06 | 42.12 | 51.82 | 47.77 |


<!-- index with hyperlinks (Table of contents) -->
## Table of contents
- [Table of contents](#table-of-contents)
- [Resources](#resources)
  - [Download IndicXlit model](#download-indicxlit-model)
  - [Accessing on ULCA](#accessing-on-ulca)
- [Running Inference](#running-inference)
  - [Command line interface](#command-line-interface)
  - [Python Inference](#python-inference)
- [Training model](#training-model)
  - [Setting up your environment](#setting-up-your-environment)
  - [Details of models and hyperparameters](#details-of-models-and-hyperparameters)
  - [Training procedure and code](#training-procedure-and-code)
  - [WandB plots](#wandb-plots)
  - [Evaluating trained model](#evaluating-trained-model)
  - [Detailed benchmarking results](#detailed-benchmarking-results)
- [Finetuning model on your data](#finetuning-model-on-your-data)
- [Mining details](#mining-details)
- [Directory structure](#directory-structure)
- [Citing](#citing)
  - [License](#license)
  - [Contributors](#contributors)
  - [Contact](#contact)


## Resources
### Download IndicXlit model
<!-- heperlinks for downloading the models -->
Roman to Indic model [v1.0](https://storage.googleapis.com/indic-xlit-public/final_model/indicxlit-en-indic-v1.0.zip)
<!-- mirror links set up the public drive -->	

### Accessing on ULCA
You can try out our model at [ULCA](https://bhashini.gov.in/ulca/model/explore-models) and filter for IndicXlit model.


## Running Inference
### Command line interface
<!-- ## Using the model to transliterate the inputs -->
The model is trained on words as inputs. hence, users need to split sentence into words before running the transliteratation model when using our command line interface.

Follow the Colab notebook to setup the environment, download the trained _IndicXlit_ model and transliterate your own text.

<!-- colab integratation on running the model on custom input cli script-->
Command line interface --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GFlqA7fpA2LLKJXtbtXSe-DqrAshuB-L?usp=sharing)

### Python Inference
<!-- colab integratation on running the model on custom input python script-->
Python interface       --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1P78Tbr6zhe-5LeiKk525N3SGPKn2ofGg?usp=sharing)

The python interface is useful in case you want to reuse the model for multiple translations and do not want to reinitialize the model each time. Moreover, re-ranking option is available in python interface, but not in command line interface.


## Training model
###  Setting up your environment
<details><summary>Click to expand </summary>

```bash
# clone IndicXli repository
git clone https://github.com/AI4Bharat/IndicXlit.git

# install required libraries
pip install indic-nlp-library

# Install fairseq from source
git clone https://github.com/pytorch/fairseq.git
cd fairseq
pip install --editable ./

```
</details>


## Details of models and hyperparameters
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

Please refer to section 6 of our [paper](https://arxiv.org/abs/2205.03018) for more details on training setup.

### Training procedure and code

The high level steps we follow for training are as follows:

Organize the train/test/valid data in corpus dir such that it has all the files containing parallel data for en-X lang pair in the following format
train_x.en for training file of en-X lang pair which contains the space separated roman characters in each line 
train_x.x for training file of en-X lang pair which contains the space separated Indic characters in each line 

```bash
# corpus/
# ├── train_as.as
# ├── train_en.en
# ├── train_bn.bn
# ├── train_en.en
# ├── ....
# ├── valid_as.as
# ├── valid_en.en
# ├── valid_bn.bn
# ├── valid_en.en
# ├── ....
# ├── test_as.as
# ├── test_en.en
# ├── test_bn.bn
# ├── test_en.en
# └── ....

```

Joint the training files across all languages
```bash
# corpus/
# ├── train_combine.cmb
# └── train_combine.en
```

Create the joint vocabulary using all the combined training data. 
```bash
fairseq-preprocess \
   --trainpref corpus/train_combine  \
   --source-lang en --target-lang cmb \
   --workers 256 \
   --destdir corpus-bin
```

Create the binarized data required for fairseq for each langauge separately using joint vocabulary
```bash
for lang_abr in bn gu hi kn ml mr pa sd si ta te ur
do
   fairseq-preprocess \
   --trainpref corpus/train_$lang_abr --validpref corpus/valid_$lang_abr --testpref corpus/test_$lang_abr \
   --srcdict corpus-bin/dict.en.txt \
   --tgtdict corpus-bin/dict.cmb.txt \
   --source-lang en --target-lang $lang_abr \
   --workers 32 \
   --destdir corpus-bin 
done
```

Add all languages codes to `lang_list.txt` file and save it in the same dir

Start training with fairseq-train command. Please refer to [fairseq documentaion](https://fairseq.readthedocs.io/en/latest/command_line_tools.html) to know more about each of these options
```bash
# training script
!fairseq-train corpus-bin \
  --save-dir transformer \
  --arch transformer --layernorm-embedding \
  --task translation_multi_simple_epoch \
  --sampling-method "temperature" \
  --sampling-temperature 1.5 \
  --encoder-langtok "tgt" \
  --lang-dict lang_list.txt \
  --lang-pairs en-bn,en-gu,en-hi,en-kn,en-ml,en-mr,en-pa,en-sd,en-si,en-ta,en-te,en-ur  \
  --decoder-normalize-before --encoder-normalize-before \
  --activation-fn gelu --adam-betas "(0.9, 0.98)"  \
  --batch-size 1024 \
  --decoder-attention-heads 4 --decoder-embed-dim 256 --decoder-ffn-embed-dim 1024 --decoder-layers 6 \
  --dropout 0.5 \
  --encoder-attention-heads 4 --encoder-embed-dim 256 --encoder-ffn-embed-dim 1024 --encoder-layers 6 \
  --lr 0.001 --lr-scheduler inverse_sqrt \
  --max-epoch 51 \
  --optimizer adam  \
  --num-workers 32 \
  --warmup-init-lr 0 --warmup-updates 4000
```
The above steps are further documented in our colab notebook
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1KM8M2hk6fPAI039bBLtHxxojHzo6oMQ7?usp=sharing)

Please refer to section 6 of our [paper](https://arxiv.org/abs/2205.03018) for more details of our training hyperparameters.
### WandB plots
[IndicXlit en-indic model]

### Evaluating trained model
The trained model will get saved in the transformer directory. It will have the following files:
```bash
# transformer/
# └── checkpoint_best.pt
```

To generate the outputs after training, use following generation script which will generate the predictions and save it in output dir.
```bash
for lang_abr in as bn brx gom gu hi kn ks mai ml mni mr ne or pa sa sd si ta te ur
do
source_lang=en
target_lang=$lang_abr
fairseq-generate corpus-bin \
  --path transformer/checkpoint_best.pt \
  --task translation_multi_simple_epoch \
  --gen-subset test \
  --beam 4 \
  --nbest 4 \
  --source-lang $source_lang \
  --target-lang $target_lang \
  --batch-size 4096 \
  --encoder-langtok "tgt" \
  --lang-dict lang_list.txt \
  --num-workers 64 \
  --lang-pairs en-as,en-bn,en-brx,en-gom,en-gu,en-hi,en-kn,en-ks,en-mai,en-ml,en-mni,en-mr,en-ne,en-or,en-pa,en-sa,en-sd,en-si,en-ta,en-te,en-ur  > output/${source_lang}_${target_lang}.txt
done
```

To test the models after training, use `generate_result_files.py` to convert the fairseq output file into xml files and 'evaluate_result_with_rescore_option.py' to compute accuracies.

evaluate_result_with_rescore_option.py can be downloaded using following link,
```bash
wget https://storage.googleapis.com/indic-xlit-public/final_model/evaluate_result_with_rescore_option.py
```

The above evaluation steps and code for `generate_result_files.py` are further documented in the colab notebook 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1KM8M2hk6fPAI039bBLtHxxojHzo6oMQ7?usp=sharing)

### Detailed evaluation results
Refer to [Evaluation Results](#evaluation-results) for results of IndicXlit model on Dakshina and Aksharantar benchmarks.
Please refer to section 7 of our [paper](https://arxiv.org/abs/2205.03018) for detailed discussion of the results


<!-- Finetuning the model on cutom dataset integrate the notebook-->

## Finetuning the model on your input dataset

The high level steps for finetuning on your own dataset are:

Organize the train/test/valid data in corpus dir such that it has all the files containing parallel data for en-X lang pair in the following format
train_x.en for training file of en-X lang pair which contains the space separated roman characters in each line 
train_x.x for training file of en-X lang pair which contains the space separated Indic characters in each line 

```bash
# corpus/
# ├── train_as.as
# ├── train_en.en
# ├── train_bn.bn
# ├── train_en.en
# ├── ....
# ├── valid_as.as
# ├── valid_en.en
# ├── valid_bn.bn
# ├── valid_en.en
# ├── ....
# ├── test_as.as
# ├── test_en.en
# ├── test_bn.bn
# ├── test_en.en
# └── ....

```


To download and decompress the model file and joint vocabulary files use following commmand,

```bash
# download the IndicXlit models
wget https://storage.googleapis.com/indic-xlit-public/final_model/indicxlit-en-indic-v1.0.zip
unzip indicxlit-en-indic-v1.0.zip
```

binarizing the files using the joint dictionaries
```bash
for lang_abr in bn gu hi kn ml mr pa sd si ta te ur
do
   fairseq-preprocess \
   --trainpref corpus/train_$lang_abr --validpref corpus/valid_$lang_abr --testpref corpus/test_$lang_abr \
   --srcdict corpus-bin/dict.en.txt \
   --tgtdict corpus-bin/dict.mlt.txt \
   --source-lang en --target-lang $lang_abr \
   --destdir corpus-bin 
done
```

Add all languages codes to `lang_list.txt` file and save it in the same dir

Please refer to fairseq documentaion to know more about each of these options (https://fairseq.readthedocs.io/en/latest/command_line_tools.html)
```bash

# We will use fairseq-train to finetune the model:
# some notable args:
# --lr                  -> learning rate. From our limited experiments, we find that lower learning rates like 3e-5 works best for finetuning.
# --restore-file        -> reload the pretrained checkpoint and start training from here (change this path for indic-en. Currently its is set to en-indic)
# --reset-*             -> reset and not use lr scheduler, dataloader, optimizer etc of the older checkpoint

fairseq-train corpus-bin \
    --save-dir transformer \
    --arch transformer --layernorm-embedding \
    --task translation_multi_simple_epoch \
    --sampling-method "temperature" \
    --sampling-temperature 1.5 \
    --encoder-langtok "tgt" \
    --lang-dict lang_list.txt \
    --lang-pairs en-bn,en-gu,en-hi,en-kn,en-ml,en-mr,en-pa,en-sd,en-si,en-ta,en-te,en-ur \
    --decoder-normalize-before --encoder-normalize-before \
    --activation-fn gelu --adam-betas "(0.9, 0.98)"  \
    --batch-size 1024 \
    --decoder-attention-heads 4 --decoder-embed-dim 256 --decoder-ffn-embed-dim 1024 --decoder-layers 6 \
    --dropout 0.5 \
    --encoder-attention-heads 4 --encoder-embed-dim 256 --encoder-ffn-embed-dim 1024 --encoder-layers 6 \
    --lr 0.001 --lr-scheduler inverse_sqrt \
    --max-epoch 51 \
    --optimizer adam  \
    --num-workers 32 \
    --warmup-init-lr 0 --warmup-updates 4000 \
    --keep-last-epochs 5 \
    --patience 5 \
    --restore-file transformer/indicxlit.pt \
    --reset-lr-scheduler \
    --reset-meters \
    --reset-dataloader \
    --reset-optimizer
```

The above steps (setup the environment, download the trained _IndicXlit_ model and prepare your custom dataset for funetuning) are further documented in our colab notebook
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TurBNE0Pq9_hqEOXps0FXfymsdlJotE0?usp=sharing)


## Mining details
Following links provides the detail description of mining from various resources,
- Samanantar: https://github.com/AI4Bharat/IndicXlit/tree/master/data_mining/transliteration_mining_samanantar
- IndicCorp: https://github.com/AI4Bharat/IndicXlit/tree/master/data_mining/IndicCorp/skeleton/en_dict_workplace




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
