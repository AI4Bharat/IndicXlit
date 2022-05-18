from flask import Flask, jsonify, request, make_response
from uuid import uuid4
from datetime import datetime
import traceback
import enum

class XlitError(enum.Enum):
    lang_err = "Unsupported langauge ID requested ;( Please check available languages."
    string_err = "String passed is incompatable ;("
    internal_err = "Internal crash ;("
    unknown_err = "Unknown Failure"
    loading_err = "Loading failed ;( Check if metadata/paths are correctly configured."

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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
        xlit_result = engine.translit_word(eng_word[:70], lang_code)
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

## ----------------------------- Xlit Engine -------------------------------- ##

from .xlit_src import XlitEngine
engine = XlitEngine()
engine.exposed_langs = [
    {
        "LangCode": code,
        "Identifier": code,
        "DisplayName": name,
        "Author": "AI4Bharat",
        "CompiledDate": "16-May-2021",
        "IsStable": True
    } for code, name in engine.langs.items()
]

def get_app():
    return app, engine
