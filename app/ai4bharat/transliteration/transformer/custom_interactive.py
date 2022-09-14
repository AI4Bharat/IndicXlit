#!/usr/bin/env python3 -u
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Translate raw text with a trained model. Batches data on-the-fly.
"""

import ast
import fileinput
import logging
import math
import os
import sys
import time
from argparse import Namespace
from collections import namedtuple

import numpy as np
import torch

from fairseq import checkpoint_utils, distributed_utils, options, tasks, utils
from fairseq.dataclass.configs import FairseqConfig
from fairseq.dataclass.utils import convert_namespace_to_omegaconf
from fairseq.token_generation_constraints import pack_constraints, unpack_constraints
from fairseq_cli.generate import get_symbols_to_strip_from_output

Batch = namedtuple("Batch", "ids src_tokens src_lengths constraints")
Translation = namedtuple("Translation", "src_str hypos pos_scores alignments")

def make_batches(lines, cfg, task, max_positions, encode_fn):
    def encode_fn_target(x):
        return encode_fn(x)


    if cfg.generation.constraints:
        # Strip (tab-delimited) contraints, if present, from input lines,
        # store them in batch_constraints
        batch_constraints = [list() for _ in lines]
        for i, line in enumerate(lines):
            if "\t" in line:
                lines[i], *batch_constraints[i] = line.split("\t")

        # Convert each List[str] to List[Tensor]
        for i, constraint_list in enumerate(batch_constraints):
            batch_constraints[i] = [
                task.target_dictionary.encode_line(
                    encode_fn_target(constraint),
                    append_eos=False,
                    add_if_not_exist=False,
                )
                for constraint in constraint_list
            ]

    if cfg.generation.constraints:
        constraints_tensor = pack_constraints(batch_constraints)
    else:
        constraints_tensor = None

    tokens, lengths = task.get_interactive_tokens_and_lengths(lines, encode_fn)

    itr = task.get_batch_iterator(
        dataset=task.build_dataset_for_inference(
            tokens, lengths, constraints=constraints_tensor
        ),
        max_tokens=cfg.dataset.max_tokens,
        max_sentences=cfg.dataset.batch_size,
        max_positions=max_positions,
        ignore_invalid_inputs=cfg.dataset.skip_invalid_size_inputs_valid_test,
    ).next_epoch_itr(shuffle=False)
    for batch in itr:
        ids = batch["id"]
        src_tokens = batch["net_input"]["src_tokens"]
        src_lengths = batch["net_input"]["src_lengths"]
        constraints = batch.get("constraints", None)

        yield Batch(
            ids=ids,
            src_tokens=src_tokens,
            src_lengths=src_lengths,
            constraints=constraints,
        )


# added
class Transliterator:
    def __init__(
        self, data_bin_dir, model_checkpoint_path, lang_pairs_csv, lang_list_file, beam, batch_size = 32,
    ):

        self.parser = options.get_interactive_generation_parser()

        # buffer_size is currently not used but we just initialize it to batch
        # size + 1 to avoid any assertion errors.
        
        self.parser.set_defaults(
            path = model_checkpoint_path,
            num_wokers = -1,
            batch_size = batch_size,
            buffer_size = batch_size + 1,
            task = "translation_multi_simple_epoch",
            beam = beam,
            # nbest = nbest,
            # source_lang = 'en' ,
            # target_lang = 'mlt' ,
            # encoder_langtok = "tgt" ,
            # lang_dict = "lang_list.txt"
        )
        
        self.args = options.parse_args_and_arch(self.parser, input_args = [data_bin_dir] )
        
        self.args.skip_invalid_size_inputs_valid_test = False
        # self.args.lang_pairs = "en-as,en-bn,en-gom,en-gu,en-hi,en-kn,en-ks,en-mai,en-ml,en-mr,en-ne,en-or,en-pa,en-sa,en-sd,en-si,en-ta,en-te,en-ur"
        self.args.lang_pairs = lang_pairs_csv
        # self.args.source_lang = 'en'
        # self.args.target_lang = 'bn'
        # self.args.encoder_langtok = 'tgt'
        self.args.lang_dict = lang_list_file

        self.cfg = convert_namespace_to_omegaconf(self.args)

        if isinstance(self.cfg, Namespace):
            self.cfg = convert_namespace_to_omegaconf(self.cfg)

        # start_time = time.time()
        self.total_translate_time = 0

        utils.import_user_module(self.cfg.common)

        if self.cfg.interactive.buffer_size < 1:
            self.cfg.interactive.buffer_size = 1
        if self.cfg.dataset.max_tokens is None and self.cfg.dataset.batch_size is None:
            self.cfg.dataset.batch_size = 1

        assert (
            not self.cfg.generation.sampling or self.cfg.generation.nbest == self.cfg.generation.beam
        ), "--sampling requires --nbest to be equal to --beam"
        assert (
            not self.cfg.dataset.batch_size
            or self.cfg.dataset.batch_size <= self.cfg.interactive.buffer_size
        ), "--batch-size cannot be larger than --buffer-size"


        # FIXME: Following lines are commented out by GokulNC due to some erros on CPU
        # GokulNC: Why do we need seeding for inference? What is stochastic decoding?

        # # Fix seed for stochastic decoding
        # if self.cfg.common.seed is not None and not self.cfg.generation.no_seed_provided:
        #     np.random.seed(self.cfg.common.seed)
        #     utils.set_torch_seed(self.cfg.common.seed)

        self.use_cuda = torch.cuda.is_available() and not self.cfg.common.cpu

        # Setup task, e.g., translation
        self.task = tasks.setup_task(self.cfg.task)

        # Load ensemble
        overrides = ast.literal_eval(self.cfg.common_eval.model_overrides)
        # logger.info("loading model(s) from {}".format(self.cfg.common_eval.path))
        self.models, _model_args = checkpoint_utils.load_model_ensemble(
            utils.split_paths(self.cfg.common_eval.path),
            arg_overrides=overrides,
            task=self.task,
            suffix=self.cfg.checkpoint.checkpoint_suffix,
            strict=(self.cfg.checkpoint.checkpoint_shard_count == 1),
            num_shards=self.cfg.checkpoint.checkpoint_shard_count,
        )

        # Set dictionaries
        self.src_dict = self.task.source_dictionary
        self.tgt_dict = self.task.target_dictionary
        
        # print("src dict",self.src_dict)
        # print("src dict",self.tgt_dict)
        # print("self.src_dict.__len__() : ",self.src_dict.symbols)
        # print("self.src_dict.__len__() : ",self.tgt_dict.symbols)

        # self.cfg.common.fp16 = True
        # Optimize ensemble for generation
        for i in range(len(self.models)):
            if self.models[i] is None:
                continue
            if self.cfg.common.fp16:
                self.models[i].half()
            
            if self.use_cuda and not self.cfg.distributed_training.pipeline_model_parallel:
                self.models[i].cuda()
            self.models[i].prepare_for_inference_(self.cfg)
            # # Quantize
            # self.models[i] = torch.quantization.quantize_dynamic(
            #     self.models[i], {torch.nn.Linear}, dtype=torch.qint8
            # )
            # # Torchscript
            # self.models[i] = torch.jit.script(self.models[i])

        # Initialize generator
        self.generator = self.task.build_generator(self.models, self.cfg.generation)

        # Handle tokenization and BPE
        self.tokenizer = self.task.build_tokenizer(self.cfg.tokenizer)
        self.bpe = self.task.build_bpe(self.cfg.bpe)

        # Load alignment dictionary for unknown word replacement
        # (None if no unknown word replacement, empty if no path to align dictionary)
        self.align_dict = utils.load_align_dict(self.cfg.generation.replace_unk)

        self.max_positions = utils.resolve_max_positions(
            self.task.max_positions(), *[model.max_positions() for model in self.models]
        )

    def encode_fn(self, x):
        if self.tokenizer is not None:
            x = self.tokenizer.encode(x)
        if self.bpe is not None:
            x = self.bpe.encode(x)
        return x

    def decode_fn(self, x):
        if self.bpe is not None:
            x = self.bpe.decode(x)
        if self.tokenizer is not None:
            x = self.tokenizer.decode(x)
        return x

    def translate(self, inputs, nbest=1):

        start_id = 0
        # for inputs in buffered_read(self.cfg.interactive.input, self.cfg.interactive.buffer_size):

        results = []
        for batch in make_batches(inputs, self.cfg, self.task, self.max_positions, self.encode_fn):
            bsz = batch.src_tokens.size(0)
            src_tokens = batch.src_tokens
            src_lengths = batch.src_lengths
            constraints = batch.constraints
            if self.use_cuda:
                src_tokens = src_tokens.cuda()
                src_lengths = src_lengths.cuda()
                if constraints is not None:
                    constraints = constraints.cuda()

            sample = {
                "net_input": {
                    "src_tokens": src_tokens,
                    "src_lengths": src_lengths,
                },
            }

            translate_start_time = time.time()
            translations = self.task.inference_step(
                self.generator, self.models, sample, constraints=constraints
            )
            translate_time = time.time() - translate_start_time
            self.total_translate_time += translate_time
            list_constraints = [[] for _ in range(bsz)]
            if self.cfg.generation.constraints:
                list_constraints = [unpack_constraints(c) for c in constraints]
            for i, (id, hypos) in enumerate(zip(batch.ids.tolist(), translations)):
                src_tokens_i = utils.strip_pad(src_tokens[i], self.tgt_dict.pad())
                constraints = list_constraints[i]
                results.append(
                    (
                        start_id + id,
                        src_tokens_i,
                        hypos,
                        {
                            "constraints": constraints,
                            "time": translate_time / len(translations),
                        },
                    )
                )

        # sort output to match input order
        result_str = ""
        for id_, src_tokens, hypos, info in sorted(results, key=lambda x: x[0]):

            src_str = ""
            if self.src_dict is not None:
                src_str = self.src_dict.string(src_tokens, self.cfg.common_eval.post_process)

                
                # print("S-{}\t{}".format(id_, src_str))
                result_str += "S-{}\t{}".format(id_, src_str) + '\n'

                # print("W-{}\t{:.3f}\tseconds".format(id_, info["time"]))
                result_str += "W-{}\t{:.3f}\tseconds".format(id_, info["time"]) + '\n'

                for constraint in info["constraints"]:
                    # print(
                    #     "C-{}\t{}".format(
                    #         id_,
                    #         self.tgt_dict.string(constraint, self.cfg.common_eval.post_process),
                    #     )
                    # )
                    result_str += "C-{}\t{}".format(
                            id_,
                            self.tgt_dict.string(constraint, self.cfg.common_eval.post_process),
                        ) + '\n'

            # Process top predictions
            for hypo in hypos[: min(len(hypos), nbest)]:
                hypo_tokens, hypo_str, alignment = utils.post_process_prediction(
                    hypo_tokens=hypo["tokens"].int().cpu(),
                    src_str=src_str,
                    alignment=hypo["alignment"],
                    align_dict=self.align_dict,
                    tgt_dict=self.tgt_dict,
                    remove_bpe=self.cfg.common_eval.post_process,
                    extra_symbols_to_ignore=get_symbols_to_strip_from_output(self.generator),
                )
                detok_hypo_str = self.decode_fn(hypo_str)
                score = hypo["score"] / math.log(2)  # convert to base 2
                # original hypothesis (after tokenization and BPE)
                # print("H-{}\t{}\t{}".format(id_, score, hypo_str))
                result_str += "H-{}\t{}\t{}".format(id_, score, hypo_str) + '\n'

                # detokenized hypothesis
                # print("D-{}\t{}\t{}".format(id_, score, detok_hypo_str))
                result_str += "D-{}\t{}\t{}".format(id_, score, detok_hypo_str) + '\n'
                
                # print(
                #     "P-{}\t{}".format(
                #         id_,
                #         " ".join(
                #             map(
                #                 lambda x: "{:.4f}".format(x),
                #                 # convert from base e to base 2
                #                 hypo["positional_scores"].div_(math.log(2)).tolist(),
                #             )
                #         ),
                #     )
                # )
                result_str += "P-{}\t{}".format(
                        id_,
                        " ".join(
                            map(
                                lambda x: "{:.4f}".format(x),
                                # convert from base e to base 2
                                hypo["positional_scores"].div_(math.log(2)).tolist(),
                            )
                        ),
                    ) + '\n'

                if self.cfg.generation.print_alignment:
                    alignment_str = " ".join(
                        ["{}-{}".format(src, tgt) for src, tgt in alignment]
                    )
                    # print("A-{}\t{}".format(id_, alignment_str))
                    result_str += "A-{}\t{}".format(id_, alignment_str) + '\n'

            # # update running id_ counter
            # start_id += len(inputs)
        return result_str
