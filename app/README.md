# AI4Bharat Transliteration Application

An AI-based transliteration engine for 21 major languages of the Indian subcontinent.

This package provides support for:  
1. Python Library for transliteration from Roman to Native script
2. HTTP API server that can be hosted for interaction with web applications

## About

This library is based on our [research work](https://indicnlp.ai4bharat.org/indic-xlit/) called **Indic-Xlit** to build tools that can translit text to Indic languages from colloquially-typed content (in English alphabet), precisely called as Roman-to-Native back-transliteration. Note that currently we **do not support** Indic to English conversion (Native-to-Roman transliteration).

- Example  Input: `namaste bhai`
- Example Output: `नमस्ते भाई`

An online demo is available here: https://xlit.ai4bharat.org

## Languages Supported

|ISO 639 code | Language |
|---|--------------------|
|as |Assamese - অসমীয়া   |
|bn |Bengali - বাংলা      |
|brx|Boro - बड़ो	      |
|gu |Gujarati - ગુજરાતી   |
|hi |Hindi - हिंदी         |
|kn |Kannada - ಕನ್ನಡ     |
|ks |Kashmiri - كٲشُر 	  |
|gom|Konkani Goan - कोंकणी|
|mai|Maithili - मैथिली     |
|ml |Malayalam - മലയാളം|
|mni|Manipuri - ꯃꯤꯇꯩꯂꯣꯟ	 |
|mr |Marathi - मराठी       |
|ne |Nepali - नेपाली 	    |
|or |Oriya - ଓଡ଼ିଆ         |
|pa |Panjabi - ਪੰਜਾਬੀ      |
|sa |Sanskrit - संस्कृतम् 	 |
|sd |Sindhi - سنڌي       |
|si |Sinhala - සිංහල     |
|ta |Tamil - தமிழ்       |
|te |Telugu - తెలుగు      |
|ur |Urdu - اُردُو         |

## Usage

### Python Library

Import the wrapper for transliteration engine by:
```py
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
- `beam_width` increases beam search size, resulting in improved accuracy but increases time/compute. (Default: `4`)
- `topk` returns only specified number of top results. (Default: `4`)
- `rescore` returns the reranked suggestions after using a dictionary. (Default: `True`)


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
# output: {'ta': 'வணக்கம் உலகம்'}
```

Note:
- Only single top most prediction is returned for each word in sentence.

**Example 4** : Using Multiple language Transliteration

```py
e = XlitEngine(["ta", "ml"], beam_width=6)
# leave empty or use "all" to load all available languages
# e = XlitEngine("all)

out = e.translit_word("amma", topk=3)
print(out)
# output: {'ta': ['அம்மா', 'அம்ம', 'அம்மை'], 'ml': ['അമ്മ', 'എമ്മ', 'അമ']}

out = e.translit_sentence("hello world")
print(out)
# output: {'ta': 'ஹலோ வார்ல்ட்', 'ml': 'ഹലോ വേൾഡ്'}

## Specify language name to get only specific language result
out = e.translit_word("amma", target_lang = "ml", topk=5)
print(out)
# output: ['അമ്മ', 'എമ്മ', 'അമ', 'എഎമ്മ', 'അഎമ്മ']
```

**Example 5** : Transliteration for all available languages
```py
e = XlitEngine(beam_width=10)
out = e.translit_sentence("Hello World")
print(out)
# sample output: {'bn': 'হেল ওয়ার্ল্ড', 'gu': 'હેલો વર્લ્ડ', 'hi': 'हेलो वर्ल्ड', 'kn': 'ಹೆಲ್ಲೊ ವರ್ಲ್ಡ್', 'ml': 'ഹലോ വേൾഡ്', 'pa': 'ਹੇਲੋ ਵਰਲਡ', 'si': 'හිලෝ වර්ල්ඩ්', 'ta': 'ஹலோ வார்ல்ட்', 'te': 'హల్లో వరల్డ్', 'ur': 'ہیلو وارڈ'}
```

---

### Web API Server

Running a flask server using a 3-line script:
```py
from ai4bharat.transliteration import xlit_server
app, engine = xlit_server.get_app()
app.run(host='0.0.0.0', port=8000)
```

Then on browser (or) curl, use link as `http://{IP-address}:{port}/tl/{lang-id}/{word_in_eng_script}`

Example:
http://localhost:8000/tl/ta/amma
http://localhost:8000/languages

---

## Debugging errors

If you face any of the following errors:
> ValueError: numpy.ndarray size changed, may indicate binary incompatibility. Expected 88 from C header, got 80 from PyObject
> ValueError: Please build (or rebuild) Cython components with `python setup.py build_ext --inplace`.

Run: `pip install --upgrade numpy`

---

## Release Notes

This package contains applications built around the Transliteration engine. The contents of this package can also be downloaded from [our GitHub repo](https://github.com/AI4Bharat/IndicXlit).

All the NN models of Indic-Xlit are released under MIT License.
