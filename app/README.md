# AI4Bharat Transliteration Application

A deep transliteration engine for major languages of the Indian subcontinent.

This package provides support for:
1. Python Library for transliteration from Roman to Native text (using Transformer-based models)
2. HTTP API exposing for interation with web applications

## Languages Supported

|ISO 639 code|Language|
|---|---------------------|
|as |Assamese - অসমীয়া	|
|bn |Bengali - বাংলা        |
|brx|Boro - बड़ो	|
|gu |Gujarati - ગુજરાતી      |
|hi |Hindi - हिंदी           |
|kn |Kannada - ಕನ್ನಡ        |
|ks |Kashmiri - كٲشُر 	|
|gom|Konkani Goan - कोंकणी  |
|mai|Maithili - मैथिली       |
|ml |Malayalam - മലയാളം    |
|mni|Manipuri - ꯃꯤꯇꯩꯂꯣꯟ	|
|mr |Marathi - मराठी        |
|ne |Nepali - नेपाली 	|
|or |Oriya - ଓଡ଼ିଆ 	|
|pa |Panjabi - ਪੰਜਾਬੀ       |
|sa |Sanskrit - संस्कृतम् 	|
|sd |Sindhi - سنڌي        |
|si |Sinhala - සිංහල       |
|ta |Tamil - தமிழ்         |
|te |Telugu - తెలుగు        |
|ur |Urdu - اُردُو          |

## Usage

### Python Library

Import the transliteration engine by:
```
from ai4bharat.transliteration import XlitEngine
```

**Example 1** : Using word Transliteration

```py

e = XlitEngine("hi", beam_width=10, rescore=True)
out = e.translit_word("computer", topk=5)
print(out)
# output:{'hi': ['कंप्यूटर', 'कम्प्यूटर', 'कॉम्प्यूटर', 'कम्प्युटर', 'कंप्युटर']}
```

Note:
- `beam_width` increases beam search size, resulting in improved accuracy but increases time/compute.
- `topk` returns only specified number of top results.
- `rescore` return the rescored candidates.   


**Example 2** : word Transliteration without rescoring
```py

e = XlitEngine("hi", beam_width=10, rescore=False)
out = e.translit_word("computer", topk=5)
print(out)
# output:{'hi': ['कम्प्यूटर', 'कंप्यूटर', 'कॉम्प्यूटर', 'कम्प्युटर', 'कंप्युटर']}
```

**Example 3** : Using Sentence Transliteration

```py

e = XlitEngine("ta", beam_width=10)
out = e.translit_sentence("vanakkam ulagam")
print(out)
# output:{'ta': 'வணக்கம் உலகம்'}
```

Note:
- Only single top most prediction is returned for each word in sentence.

**Example 4** : Using Multiple language Transliteration

```py

e = XlitEngine(["ta", "ml"], beam_width=10)
# leave empty or use "all" to load all available languages
# e = XlitEngine("all)

out = e.translit_word("amma", topk=3)
print(out)
# output:

out = e.translit_sentence("hello world")
print(out)
# output: 

## Specify language name to get only specific language result
out = e.translit_word("amma", target_lang = "ml", topk=3)
print(out)
# output: 

```

**Example 5** : Transliteration for all available languages
```py

e = XlitEngine(beam_width=10)
out = e.translit_sentence("Hello World")
print(out)
# output: 

```


### Web API Server

Running a flask server in a 3-line script:
```py
from ai4bharat.transliteration import xlit_server
app, engine = xlit_server.get_app()
app.run(host='0.0.0.0', port=8000)
```

You can also check the extended [sample script](https://github.com/AI4Bharat/IndianNLP-Transliteration/blob/master/apps/api_expose.py) as shown below:

1. Make required modification in SSL paths in `api_expose.py`. By default set to local host and both http & https are enabled.

2. Run the API expose code:
`$ sudo env PATH=$PATH python3 api_expose.py`
(Export `GOOGLE_APPLICATION_CREDENTIALS` if needed, by default functions realted to Google cloud is disabled.)

3. In browser (or) curl, use link as http://{IP-address}:{port}/tl/{lang-id}/{word in eng script}
If debug mode enabled port will be 8000, else port will be 80.

Example:
http://localhost:80/tl/ta/amma
http://localhost:80/languages

---

## Debugging errors

If you face any of the following errors:
> ValueError: numpy.ndarray size changed, may indicate binary incompatibility. Expected 88 from C header, got 80 from PyObject
> ValueError: Please build (or rebuild) Cython components with `python setup.py build_ext --inplace`.

Run: `pip install --upgrade numpy`

---

## Release Notes

This package contains applications built around the Transliteration engine. The contents of this package can also be downloaded from [latest GitHub release](https://github.com/AI4Bharat/IndianNLP-Transliteration/releases/latest) is sufficient for inference usage.

All the NN models (along with metadata) of Xlit - Transliteration are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].



[cc-by-sa]: http://creativecommons.org/licenses/by/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
