from ai4bharat.transliteration import xlit_server
app, engine = xlit_server.get_app()
app.run(host='0.0.0.0', port=8888) # debug=True, use_reloader=False, 
