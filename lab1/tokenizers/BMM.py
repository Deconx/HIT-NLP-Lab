# -*- coding: gbk -*-
from lab1.tokenizers.MM import MM, write_file
import re


class BMM(MM):
    def __init__(self, datatype='list', data_file='../data/199801_sent.txt', target_file='../data/seg_BMM.txt'):
        super().__init__(datatype=datatype)
        self.data_file = data_file
        self.target_file = target_file

    def tokenize(self):
        with open(self.data_file) as f:
            lines = f.readlines()
            tf = open(self.target_file, 'w')
            for line in lines:
                self.tokenize_line(line, tf)
            f.close()
            tf.close()

    def tokenize_line(self, line, tf):
        # ��������ƥ��ֳ�������ĸ��
        l = self.pattern.finditer(line)
        # ����������Ӵʵ���
        for w in l:
            # ����ƥ�䵽���±�
            (i, j) = w.span()
            # ����һ�µ�һ�����ڲ���
            if i == 0 and j > 19:
                j = 19
            self.vocabData.add(line[i:j])
        # print(self.vocabData)
        # �������ƥ���㷨
        segList = []
        maxlen = self.vocabData.maxlen
        while len(line) > 0:
            length = self.vocabData.maxlen
            if len(line) < maxlen:
                length = len(line)
            tryWord = line[len(line)-length:]
            while tryWord not in self.vocabData:
                if len(tryWord) == 1:
                    break
                tryWord = tryWord[1:]
            segList.insert(0, tryWord)
            line = line[:len(line)-len(tryWord)]
        write_file(segList, tf)


if __name__ == '__main__':
    bmm = BMM()
    bmm.tokenize()
