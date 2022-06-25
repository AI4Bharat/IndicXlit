### Languages

| <!-- -->  	 | <!-- --> 	  | <!-- --> 	   | <!-- -->	     | <!-- -->       | <!-- -->      |
| -------------- | -------------- | -------------- | --------------- | -------------- | ------------- |
| Assamese (asm) | Hindi (hin) 	  | Maithili (mai) | Marathi (mar)   | Punjabi (pan)  | Tamil (tam)   |
| Bengali (ben)  | Kannada (kan)  | Malayalam (mal)| Nepali (nep)    | Sanskrit (san) | Telugu (tel)  | 
| Bodo(brx)      | Kashmiri (kas) | Manipuri (mni) | Oriya (ori)     | Sindhi (snd)   | Urdu (urd)    |
| Gujarati (guj) | Konkani (kok)  | 


## Dataset Structure


### Data Instances

```
A random sample from Hindi (hin) Train dataset.

{
'unique_identifier': 'hin1241393', 
'native word': 'स्वाभिमानिक', 
'english word': 'swabhimanik', 
'source': 'IndicCorp', 
'score': -0.1028788579
}

```

### Data Fields

- `unique_identifier` (string): 3-letter language code followed by a unique number in each set (Train, Test, Val).
- `native word` (string): A word in Indic language.
- `english word` (string): Transliteration of native word in English (Romanised word).
- `source` (string): Source of the data.
- `score` (num): Character level log probability of indic word given roman word by IndicXlit (model). Pairs with average threshold of the 0.35 are considered.

  For created data sources, depending on the destination/sampling method of a pair in a language, it will be one of:
  - Dakshina Dataset
  - IndicCorp 
  - Samanantar
  - Wikidata
  - Existing sources (Refer ULCA format for further split)
  - Named Entities Indian (AK-NEI)
  - Named Entities Foreign (AK-NEF)
  - Data from Uniform Sampling method. (Ak-Uni)
  - Data from Most Frequent words sampling method. (Ak-Freq)
  
[All individual Datasets](https://console.cloud.google.com/storage/browser/indic-xlit-public) |
[Aksharantar](https://huggingface.co/datasets/ai4bharat/Aksharantar/tree/main)
