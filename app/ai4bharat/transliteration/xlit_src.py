def XlitEngine(
    lang2use = "all", beam_width=4, rescore=True,
    model_type = "transformer"
):
    if model_type == "transformer":
        from .transformer.engine import XlitEngineTransformer
        return XlitEngineTransformer(lang2use, beam_width=beam_width, rescore=rescore)
    
    if model_type == "rnn":
        from .rnn.engine import XlitEngineRNN
        return XlitEngineRNN(lang2use, beam_width=beam_width, rescore=rescore)
    
    return None
