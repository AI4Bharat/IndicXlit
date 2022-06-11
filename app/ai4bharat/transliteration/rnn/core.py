import os
import torch
import numpy as np
import pandas as pd
import json

from .network import Encoder, Decoder, Seq2Seq

##===================== Glyph handlers =======================================

class GlyphStrawboss():
    def __init__(self, glyphs = 'en'):
        """ list of letters in a language in unicode
        lang: ISO Language code
        glyphs: json file with script information
        """
        if glyphs == 'en':
            # Smallcase alone
            self.glyphs = [chr(alpha) for alpha in range(97, 122+1)]
        else:
            self.dossier = json.load(open(glyphs, encoding='utf-8'))
            self.glyphs = self.dossier["glyphs"]
            self.numsym_map = self.dossier["numsym_map"]

        self.char2idx = {}
        self.idx2char = {}
        self._create_index()

    def _create_index(self):

        self.char2idx['_'] = 0  #pad
        self.char2idx['$'] = 1  #start
        self.char2idx['#'] = 2  #end
        self.char2idx['*'] = 3  #Mask
        self.char2idx["'"] = 4  #apostrophe U+0027
        self.char2idx['%'] = 5  #unused
        self.char2idx['!'] = 6  #unused

        # letter to index mapping
        for idx, char in enumerate(self.glyphs):
            self.char2idx[char] = idx + 7 # +7 token initially

        # index to letter mapping
        for char, idx in self.char2idx.items():
            self.idx2char[idx] = char

    def size(self):
        return len(self.char2idx)


    def word2xlitvec(self, word):
        """ Converts given string of gyphs(word) to vector(numpy)
        Also adds tokens for start and end
        """
        try:
            vec = [self.char2idx['$']] #start token
            for i in list(word):
                vec.append(self.char2idx[i])
            vec.append(self.char2idx['#']) #end token

            vec = np.asarray(vec, dtype=np.int64)
            return vec

        except Exception as error:
            print("XlitError: In word:", word)
            exit("Error Char not in Token: " + error)

    def xlitvec2word(self, vector):
        """ Converts vector(numpy) to string of glyphs(word)
        """
        char_list = []
        for i in vector:
            char_list.append(self.idx2char[i])

        word = "".join(char_list).replace('$','').replace('#','') # remove tokens
        word = word.replace("_", "").replace('*','') # remove tokens
        return word


class VocabSanitizer():
    def __init__(self, data_file):
        '''
        data_file: path to file conatining vocabulary list
        '''
        extension = os.path.splitext(data_file)[-1]
        if extension == ".json":
            self.vocab_set  = set( json.load(open(data_file, encoding='utf-8')) )
        elif extension == ".csv":
            self.vocab_df = pd.read_csv(data_file).set_index('WORD')
            self.vocab_set = set( self.vocab_df.index )
        else:
            print("XlitError: Only Json/CSV file extension supported")

    def reposition(self, word_list):
        '''Reorder Words in list
        '''
        new_list = []
        temp_ = word_list.copy()
        for v in word_list:
            if v in self.vocab_set:
                new_list.append(v)
                temp_.remove(v)
        new_list.extend(temp_)

        return new_list


##=============== INSTANTIATION ================================================

class XlitPiston():
    """
    For handling prediction & post-processing of transliteration for a single language

    Class dependency: Seq2Seq, GlyphStrawboss, VocabSanitizer
    Global Variables: F_DIR
    """
    def __init__(self, weight_path, tglyph_cfg_file, iglyph_cfg_file = "en",
                        vocab_file=None, device = "cpu" ):

        self.device = device
        self.in_glyph_obj = GlyphStrawboss(iglyph_cfg_file)
        self.tgt_glyph_obj = GlyphStrawboss(glyphs = tglyph_cfg_file)
        if vocab_file:
            self.voc_sanitizer = VocabSanitizer(vocab_file)
        else:
            self.voc_sanitizer = None

        self._numsym_set = set(json.load(open(tglyph_cfg_file, encoding='utf-8'))["numsym_map"].keys() )
        self._inchar_set = set("abcdefghijklmnopqrstuvwxyz")
        self._natscr_set = set().union(self.tgt_glyph_obj.glyphs,
                            sum(self.tgt_glyph_obj.numsym_map.values(),[]) )


        ## Model Config Static                TODO: add defining in json support
        input_dim = self.in_glyph_obj.size()
        output_dim = self.tgt_glyph_obj.size()
        enc_emb_dim = 300
        dec_emb_dim = 300
        enc_hidden_dim = 512
        dec_hidden_dim = 512
        rnn_type = "lstm"
        enc2dec_hid = True
        attention = True
        enc_layers = 1
        dec_layers = 2
        m_dropout = 0
        enc_bidirect = True
        enc_outstate_dim = enc_hidden_dim * (2 if enc_bidirect else 1)

        enc = Encoder(  input_dim= input_dim, embed_dim = enc_emb_dim,
                        hidden_dim= enc_hidden_dim,
                        rnn_type = rnn_type, layers= enc_layers,
                        dropout= m_dropout, device = self.device,
                        bidirectional= enc_bidirect)
        dec = Decoder(  output_dim= output_dim, embed_dim = dec_emb_dim,
                        hidden_dim= dec_hidden_dim,
                        rnn_type = rnn_type, layers= dec_layers,
                        dropout= m_dropout,
                        use_attention = attention,
                        enc_outstate_dim= enc_outstate_dim,
                        device = self.device,)
        self.model = Seq2Seq(enc, dec, pass_enc2dec_hid=enc2dec_hid, device=self.device)
        self.model = self.model.to(self.device)
        weights = torch.load( weight_path, map_location=torch.device(self.device))

        self.model.load_state_dict(weights)
        self.model.eval()

    def character_model(self, word, beam_width = 1):
        in_vec = torch.from_numpy(self.in_glyph_obj.word2xlitvec(word)).to(self.device)
        ## change to active or passive beam
        p_out_list = self.model.active_beam_inference(in_vec, beam_width = beam_width)
        p_result = [ self.tgt_glyph_obj.xlitvec2word(out.cpu().numpy()) for out in p_out_list]

        if self.voc_sanitizer:
            return self.voc_sanitizer.reposition(p_result)

        #List type
        return p_result

    def numsym_model(self, seg):
        ''' tgt_glyph_obj.numsym_map[x] returns a list object
        '''
        if len(seg) == 1:
            return  [seg] + self.tgt_glyph_obj.numsym_map[seg]

        a = [self.tgt_glyph_obj.numsym_map[n][0] for n in seg]
        return [seg] + ["".join(a)]


    def _word_segementer(self, sequence):

        sequence = sequence.lower()
        accepted = set().union(self._numsym_set, self._inchar_set, self._natscr_set)
        # sequence = ''.join([i for i in sequence if i in accepted])

        segment = []
        idx = 0
        seq_ = list(sequence)
        while len(seq_):
            # for Number-Symbol
            temp = ""
            while len(seq_) and seq_[0] in self._numsym_set:
                temp += seq_[0]
                seq_.pop(0)
            if temp != "": segment.append(temp)

            # for Target Chars
            temp = ""
            while len(seq_) and seq_[0] in self._natscr_set:
                temp += seq_[0]
                seq_.pop(0)
            if temp != "": segment.append(temp)

            # for Input-Roman Chars
            temp = ""
            while len(seq_) and seq_[0] in self._inchar_set:
                temp += seq_[0]
                seq_.pop(0)
            if temp != "": segment.append(temp)

            temp = ""
            while len(seq_) and seq_[0] not in accepted:
                temp += seq_[0]
                seq_.pop(0)
            if temp != "": segment.append(temp)

        return segment

    def inferencer(self, sequence, beam_width = 10):

        seg = self._word_segementer(sequence[:120])
        lit_seg = []

        p = 0
        while p < len(seg):
            if seg[p][0] in self._natscr_set:
                lit_seg.append([seg[p]])
                p+=1

            elif seg[p][0] in self._inchar_set:
                lit_seg.append(self.character_model(seg[p], beam_width=beam_width))
                p+=1

            elif seg[p][0] in self._numsym_set: # num & punc
                lit_seg.append(self.numsym_model(seg[p]))
                p+=1
            else:
                lit_seg.append([ seg[p] ])
                p+=1

        ## IF segment less/equal to 2 then return combinotorial,
        ## ELSE only return top1 of each result concatenated
        if len(lit_seg) == 1:
            final_result = lit_seg[0]

        elif len(lit_seg) == 2:
            final_result = [""]
            for seg in lit_seg:
                new_result = []
                for s in seg:
                    for f in final_result:
                        new_result.append(f+s)
                final_result = new_result

        else:
            new_result = []
            for seg in lit_seg:
                new_result.append(seg[0])
            final_result = ["".join(new_result) ]

        return final_result
