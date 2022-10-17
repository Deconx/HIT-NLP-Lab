# -*- coding: gbk -*-
from lab1.tokenizers.MM import MM
import re


class FMM(MM):
    def __init__(self, data_file='../data/199801_sent.txt', target_file='../data/seg_FMM.txt'):
        super().__init__()
        self.data_file = data_file
        self.target_file = target_file

    def tokenize(self):
        with open(self.data_file) as f:
            lines = f.readlines()
            for line in lines:
                self.tokenize_line(line)
            f.close()

    def tokenize_line(self, line):
        pattern_index = re.compile(r'((\d|-|��|��|��|[��-��]|��|[��-��]|[��-��]|��)+)')
        # ����
        pattern_numrate = re.compile(r'(��?(�ٷ�֮|��)?([��-��]+|[0-9]+|[����һ�����������߰˾�ʮ��]+)([��ǧ����]?)[.������]?([��-��]+|[0-9]+|['
                                     r'����һ�����������߰˾�ʮ]+)([��ǧ����]?)([����ǧ�ڸ�����])*)+')
        # ��������ƥ��ֳ�������ĸ��
        l1 = pattern_index.finditer(line)
        l2 = pattern_numrate.finditer(line)
        f = open(self.target_file)
        for i in l1:
            print(i.span())



if __name__ == '__main__':
    fmm = FMM()
    fmm.tokenize()


