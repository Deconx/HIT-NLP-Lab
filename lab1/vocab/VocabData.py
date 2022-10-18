# -*- coding: gbk -*-
from abc import abstractmethod

from lab1.vocab.Vocab import Vocab


def init_vocab(datafile='../data/dict.txt', datatype=list):
    """
    ��̬����������ָ��ĳ�����ݽṹ������ʼ���ʵ�
    :param datafile: �ʵ��ŵı����ļ�
    :param datatype: ָ�����ݽṹ
    :return: ����ָ�����ݽṹ���ɵĴʵ�
    """
    vocab_data = VocabData()
    if datatype == "list":
        vocab_data = VocabList()
    f = open(datafile, encoding='gbk')
    lines = f.readlines()
    for line in lines:
        if line is None:
            continue
        word = line.split('\t')[0]
        vocab_data.add(word)
    return vocab_data


class VocabData:
    """
    �����ඨ���ֵ�洢�����ݽṹ
    """

    def __init__(self):
        self.vocab = Vocab()
        self.maxlen = 0

    def maxLen(self):
        """
        :return:�ʵ������ʵĳ���
        """
        return self.maxlen

    @abstractmethod
    def __contains__(self, item):
        """
        ��д__contains__���������ڲ��Ҵʵ�
        :param item: Ҫ���ҵ��ַ���
        :return: BOOL���Ƿ����
        """
        pass

    @abstractmethod
    def add(self, item):
        """
        ��ʵ����Ԫ��
        :param item: Ԫ��
        :return: None
        """
        pass


class VocabList(VocabData):
    """
    ʹ��Python��list�洢�ʵ䣬��Ӧ��3.2
    """

    def __init__(self):
        super(VocabList, self).__init__()
        self.dict = list()

    def __contains__(self, item):
        return self.dict.__contains__(item)

    def add(self, item):
        self.dict.append(item)
        # ά�����ִʳ���
        self.maxlen = max(self.maxlen, len(item))

    def __repr__(self):
        return self.dict.__repr__()

    def __len__(self):
        return len(self.dict)
