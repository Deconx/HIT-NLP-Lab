# -*- coding: gbk -*-
from abc import abstractmethod

from lab1.vocab.Vocab import Vocab
from lab1.vocab.VocabData import init_vocab


class MM:
    """
    ���ƥ������࣬��ΪFMM��BMM�ĸ���
    """

    def __init__(self, datatype='list'):
        vocab = Vocab()
        self.vocabData = init_vocab(datatype=datatype)
        self.pattern = vocab.get_pattern()

    @abstractmethod
    def tokenize(self):
        pass
