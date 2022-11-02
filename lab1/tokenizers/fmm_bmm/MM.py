# -*- coding: gbk -*-
from abc import abstractmethod

from lab1.vocab.Vocab import Vocab
from lab1.vocab.VocabData import init_vocab


def write_file(line, tf):
    """
    �ѷִ��б�д���ļ�
    :param line: �ִ��б�
    :param tf: �ļ�
    :return:
    """
    for l in line:
        if l == '\n':
            tf.write('\n')
            break
        tf.write(l)
        tf.write('/ ')


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
