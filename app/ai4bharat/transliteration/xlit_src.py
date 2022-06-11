from .transformer.core import XlitEngineTransformer

def XlitEngine(
    lang2use = "all", beam_width=4, rescore=True,
    model_type = "transformer"
):
    if model_type == "transformer":
        from .transformer.core import XlitEngineTransformer
        return XlitEngineTransformer(lang2use, beam_width, rescore)
    
    return None
