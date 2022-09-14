def XlitEngine(
    lang2use = "all", beam_width=4, rescore=True,
    model_type = "transformer",
    src_script_type = "roman",
):
    if model_type == "transformer":
        if src_script_type in {"roman", "latin", "en"}:
            from .transformer import XlitEngineTransformer_En2Indic
            return XlitEngineTransformer_En2Indic(lang2use, beam_width=beam_width, rescore=rescore)
        elif src_script_type == "indic":
            from .transformer import XlitEngineTransformer_Indic2En
            return XlitEngineTransformer_Indic2En(beam_width=beam_width, rescore=rescore)
    
    elif model_type == "rnn":
        assert src_script_type in {"roman", "latin", "en"}
        from .rnn.engine import XlitEngineRNN
        return XlitEngineRNN(lang2use, beam_width=beam_width, rescore=rescore)
           
    raise NotImplementedError()
