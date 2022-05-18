from flask import Flask, jsonify, make_response
from datetime import datetime
# import xlit_translit
from ai4bharat.transliteration import XlitEngine

import logging
logging.basicConfig(level=logging.WARNING)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

## ---------------------------- API End-points ------------------------------ ##
# NUM_SUGGESTIONS = 10

LANGS = {
        'as': 'Assamese',
        'bn': 'Bengali',
        'brx': 'Bodo',
        'gu' : 'Gujarati',
        'hi': 'Hindi',
        'kn': 'Kannada',
        'ks': 'Kashmiri',
        'gom': 'Konkani',
        'mai': 'Maithili',
        'ml': 'Malayalam',
        'mni': 'Manipuri',
        'mr': 'Marathi',
        'ne': 'Nepali',
        'or': 'Oriya',
        'pa': 'Panjabi',
        'sa': 'Sanskrit',
        'sd': 'Sindhi',
        'si': 'Sinhala',
        'ta': 'Tamil',
        'te': 'Telugu',
        'ur': 'Urdu'
        }

EXPOSED_LANGS = [{
        "Author": "AI4Bharat", # or your name
        "CompiledDate": "9-April-2021", # date on which model was trained
        "IsStable": True,
        "DisplayName": lang,
        "Identifier": code, #ISO 639-1 code
        "LangCode": code, # ISO 639-2 code
    } for code, lang in LANGS.items()
]


e = XlitEngine(beam=10, nbest=10)


@app.route('/languages', methods = ['GET', 'POST'])
def supported_languages():
    SUPPORTED_LANGS_RESPONSE = make_response(jsonify(EXPOSED_LANGS))
    # Format: https://xlit-api.ai4bharat.org/languages
    return SUPPORTED_LANGS_RESPONSE

@app.route('/tl/<lang_code>/<eng_word>', methods = ['GET', 'POST'])
def xlit_api(lang_code, eng_word):
    # Format: https://xlit-api.ai4bharat.org/tl/hi/bharat
    response = {
        'success': True,
        'error': '',
        'at': str(datetime.utcnow()) + ' +0000 UTC',
        'input': eng_word.strip(),
        'result': ''
    }

    if lang_code not in LANGS:
        response['success'] = False
        response['error'] = 'Invalid scheme identifier. Supported languages are: '+ str(LANGS)
        return jsonify(response)

    response['result'] = e.translit_word(eng_word, target_lang=lang_code, rescore=1)[lang_code]
    # response['result'] = transliterate_word(eng_word, lang_code, NUM_SUGGESTIONS)
    return jsonify(response)

if __name__ == '__main__':
    from flask_cors import CORS, cross_origin
    cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.run(debug=True, host='0.0.0.0', port=8001)
