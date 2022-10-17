# -*- coding: gbk -*-
from lab1.vocab.Vocab import Vocab

class MM:
    """
    ���ƥ������࣬��ΪFMM��BMM�ĸ���
    """

    def __init__(self):
        vocab = Vocab()
        self.vocab_list = vocab.get_vocab_list()
        self.maxLen = self.getmaxlen()

    def getmaxlen(self):
        """
        ����ʵ�����ʵĳ���
        :return: ������ʳ���
        """
        maxLen = 0
        for word in self.vocab_list:
            if len(word) > maxLen:
                maxLen = len(word)
        return maxLen

    def tokenize(self):
        raise NotImplemented
