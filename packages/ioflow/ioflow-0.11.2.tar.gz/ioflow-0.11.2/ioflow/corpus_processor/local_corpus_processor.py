import functools
import os

import numpy as np
from tokenizer_tools.tagset.offset.corpus import Corpus
from nlp_utils.text.load_text import load_text

from ioflow.corpus_processor.corpus_processor_base import CorpusProcessorBase


@functools.lru_cache(maxsize=2)
def generator_fn(input_file):
    return Corpus.read_from_file(input_file)


class LocalCorpusProcessor(CorpusProcessorBase):
    def __init__(self, config):
        super(LocalCorpusProcessor, self).__init__(config)

    def prepare(self):
        self.dataset_mapping[self.TRAIN] = functools.partial(
            generator_fn, os.path.abspath(self.config["train"])
        )
        self.dataset_mapping[self.EVAL] = functools.partial(
            generator_fn, os.path.abspath(self.config["test"])
        )

        self.meta_info = {
            "tags": load_text(self.config["tags"]) if self.config.get("tags") else None,
            "labels": load_text(self.config["labels"])
            if self.config.get("labels")
            else None,
        }
