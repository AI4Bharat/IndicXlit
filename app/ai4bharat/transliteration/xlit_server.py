"""
Expose Transliteration Engine as an HTTP API.

USAGE:
```
from ai4bharat.transliteration import xlit_server
app, engine = xlit_server.get_app()
app.run(host='0.0.0.0', port=8000)
```
Sample URLs:
    http://localhost:8000/tl/ta/amma
    http://localhost:8000/languages

FORMAT:
    Based on the Varnam API standard
    https://api.varnamproject.com/tl/hi/bharat
"""

from flask import Flask, jsonify, request, make_response
from uuid import uuid4
from datetime import datetime
import traceback
import enum

from .utils import LANG_CODE_TO_DISPLAY_NAME

class XlitError(enum.Enum):
    lang_err = "Unsupported langauge ID requested ;( Please check available languages."
    string_err = "String passed is incompatable ;("
    internal_err = "Internal crash ;("
    unknown_err = "Unknown Failure"
    loading_err = "Loading failed ;( Check if metadata/paths are correctly configured."

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

## ----------------------------- Xlit Engine -------------------------------- ##

from .xlit_src import XlitEngine

MAX_SUGGESTIONS = 8
DEFAULT_NUM_SUGGESTIONS = 6

engine = XlitEngine(beam_width=MAX_SUGGESTIONS, rescore=True, model_type="transformer")
engine.exposed_langs = [
    {
        "LangCode": lang_code, # ISO-639 code
        "Identifier": lang_code, # ISO-639 code
        "DisplayName": LANG_CODE_TO_DISPLAY_NAME[lang_code],
        "Author": "AI4Bharat", # Name of developer / team
        "CompiledDate": "09-April-2022", # date on which model was trained
        "IsStable": True, # Set `False` if the model is experimental
    } for lang_code in sorted(engine.langs)
]

def get_app():
    return app, engine

## ---------------------------- API End-points ------------------------------ ##

@app.route('/languages', methods = ['GET', 'POST'])
def supported_languages():
    # Format - https://xlit-api.ai4bharat.org/languages
    response = make_response(jsonify(engine.exposed_langs))
    if 'xlit_user_id' not in request.cookies:
        # host = request.environ['HTTP_ORIGIN'].split('://')[1]
        host = '.ai4bharat.org'
        response.set_cookie('xlit_user_id', uuid4().hex, max_age=365*24*60*60, domain=host, samesite='None', secure=True, httponly=True)
    return response

@app.route('/tl/<lang_code>/<eng_word>', methods = ['GET', 'POST'])
def xlit_api(lang_code, eng_word):
    # Format: https://xlit-api.ai4bharat.org/tl/ta/bharat
    response = {
        'success': False,
        'error': '',
        'at': str(datetime.utcnow()) + ' +0000 UTC',
        'input': eng_word.strip(),
        'result': ''
    }

    if lang_code not in engine.langs:
        response['error'] = 'Invalid scheme identifier. Supported languages are'+ str(engine.langs)
        return jsonify(response)

    try:
        ## Limit char count to --> 70
        xlit_result = engine.translit_word(eng_word[:70], lang_code, topk=DEFAULT_NUM_SUGGESTIONS)
    except Exception as e:
        xlit_result = XlitError.internal_err


    if isinstance(xlit_result, XlitError):
        response['error'] = xlit_result.value
        print("XlitError:", traceback.format_exc())
    else:
        response['result'] = xlit_result
        response['success'] = True

    return jsonify(response)

@app.route('/rtl/<lang_code>/<word>', methods = ['GET', 'POST'])
def reverse_xlit_api(lang_code, word):
    # Format: https://api.varnamproject.com/rtl/hi/%E0%A4%AD%E0%A4%BE%E0%A4%B0%E0%A4%A4
    response = {
        'success': False,
        'error': '',
        'at': str(datetime.utcnow()) + ' +0000 UTC',
        'input': word,
        'result': ''
    }
    # TODO: Implement?
    response['error'] = 'Not yet implemented!'
    return jsonify(response)

@app.route('/transliterate', methods=['POST'])
def ulca_api():
    '''
    ULCA-compliant endpoint. See for sample request-response:
    https://github.com/ULCA-IN/ulca/tree/master/specs/examples/model/transliteration-model
    '''
    data = request.get_json(force=True)
    
    if "input" not in data or "config" not in data:
        return jsonify({
            "status": {
                "statusCode": 400,
                "message": "Ensure `input` and `config` fields missing."
            }
        }), 400
    
    if data["config"]["language"]["sourceLanguage"] != "en" or data["config"]["language"]["targetLanguage"] not in engine.langs:
        return jsonify({
            "status": {
                "statusCode": 501,
                "message": "The mentioned language-pair is not supported yet."
            }
        }), 501
    
    is_sentence = data["config"]["isSentence"] if "isSentence" in data["config"] else False
    num_suggestions = 1 if is_sentence else (data["config"]["numSuggestions"] if "numSuggestions" in data["config"] else 5)
    target_lang_code = data["config"]["language"]["targetLanguage"]

    outputs = []
    for item in data["input"]:
        if is_sentence:
            item["target"] = [engine.translit_sentence(item["source"], lang_code=target_lang_code)]
        else:
            item["source"] = item["source"][:32]
            item["target"] = engine.translit_word(item["source"], lang_code=target_lang_code, topk=num_suggestions)
    
    return {
        "output": data["input"],
        # "status": {
        #     "statusCode": 200,
        #     "message" : "success"
        # }
    }, 200
