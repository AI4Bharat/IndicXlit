from ai4bharat.transliteration import xlit_server

DEBUG = False
PORT = 8888

app, engine = xlit_server.get_app()

if DEBUG:
    app.run(debug=DEBUG, use_loader=False, port=PORT)
else:
    from flask_cors import CORS, cross_origin
    from gevent.pywsgi import WSGIServer

    cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    http_server = WSGIServer((PORT), app)

    print("Starting production server...")
    http_server.serve_forever()
