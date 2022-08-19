# AI4Bharat Indic-Transliteration

An AI-based transliteration engine for 21 major languages of the Indian subcontinent.

This package provides support for:  
1. Python Library for transliteration from Roman to Native script
2. HTTP API server that can be hosted for interaction with web applications

## About

This library is based on our [research work](https://ai4bharat.org/transliteration) called **Indic-Xlit** to build tools that can translit text between Indic languages and colloquially-typed content (in English alphabet). We support both Roman-to-Native back-transliteration (English script to Indic language conversion), as well as Native-to-Roman transliteration (Indic to English alphabet conversion).

An online demo is available here: https://xlit.ai4bharat.org

## Languages Supported

|ISO 639 code | Language |
|---|--------------------|
|as |Assamese - অসমীয়া   |
|bn |Bangla - বাংলা       |
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
out = e.translit_word("namasthe", topk=5)
print(out)
# output: {'hi': ['नमस्ते', 'नमस्थे', 'नामस्थे', 'नमास्थे', 'नमस्थें']}
```

Arguments:
- `beam_width` increases search size, resulting in improved accuracy but increases time/compute. (Default: `4`)
- `topk` returns only specified number of top results. (Default: `4`)
- `rescore` returns the reranked suggestions after using a dictionary. (Default: `True`)

Romanization: 
- By default, `XlitEngine` will load English-to-Indic model (default: `src_script_type="roman"`)
- To load Indic-to-English model, use `src_script_type="indic"`

For example: (also applicable for all other examples below)

```py
e = XlitEngine(src_script_type="indic", beam_width=10, rescore=False)
out = e.translit_word("नमस्ते", lang_code="hi", topk=5)
print(out)
# output: ['namaste', 'namastey', 'namasthe', 'namastay', 'namste']
```

**Example 2** : word Transliteration without rescoring
```py
e = XlitEngine("hi", beam_width=10, rescore=False)
out = e.translit_word("namasthe", topk=5)
print(out)
# output: {'hi': ['नमस्थे', 'नामस्थे', 'नमास्थे', 'नमस्थें', 'नमस्ते']}
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
# output: {'ml': ['അമ്മ', 'എമ്മ', 'അമ'], 'ta': ['அம்மா', 'அம்ம', 'அம்மை']}

out = e.translit_sentence("vandhe maatharam")
print(out)
# output: {'ml': 'വന്ധേ മാതരം', 'ta': 'வந்தே மாதரம்'}

## Specify language name to get only specific language result
out = e.translit_word("amma", lang_code = "ml", topk=5)
print(out)
# output: ['അമ്മ', 'എമ്മ', 'അമ', 'എഎമ്മ', 'അഎമ്മ']
```

**Example 5** : Transliteration for all available languages
```py
e = XlitEngine(beam_width=10)
out = e.translit_sentence("namaskaar bharat")
print(out)
# sample output: {'bn': 'নমস্কার ভারত', 'gu': 'નમસ્કાર ભારત', 'hi': 'नमस्कार भारत', 'kn': 'ನಮಸ್ಕಾರ್ ಭಾರತ್', 'ml': 'നമസ്കാർ ഭാരത്', 'pa': 'ਨਮਸਕਾਰ ਭਾਰਤ', 'si': 'නමස්කාර් භාරත්', 'ta': 'நமஸ்கார் பாரத்', 'te': 'నమస్కార్ భారత్', 'ur': 'نمسکار بھارت'}
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
