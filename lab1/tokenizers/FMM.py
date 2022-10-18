# -*- coding: gbk -*-
from lab1.tokenizers.MM import MM
import re


class FMM(MM):
    def __init__(self, datatype='list', data_file='../data/199801_sent.txt', target_file='../data/seg_FMM.txt'):
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

    def write_file(self, line, tf):
        """
        把分词列表写入文件
        :param line: 分词列表
        :param tf: 文件
        :return:
        """
        for l in line:
            if l == '\n':
                tf.write('\n')
                break
            tf.write(l)
            tf.write('/ ')

    def tokenize_line(self, line, tf):
        # 先用正则匹配分出数字字母串
        l = self.pattern.finditer(line)
        # 先用正则添加词典中
        for w in l:
            # 正则匹配到的下标
            (i, j) = w.span()
            # 过滤一下第一个日期部分
            if i == 0 and j > 19:
                j = 19
            self.vocabData.add(line[i:j])
        # print(self.vocabData)
        # 正向最大匹配算法
        segList = []
        maxlen = self.vocabData.maxlen
        while len(line) > 0:
            length = self.vocabData.maxlen
            if len(line) < maxlen:
                length = len(line)
            tryWord = line[0:length]
            while tryWord not in self.vocabData:
                if len(tryWord) == 1:
                    break
                tryWord = tryWord[0:len(tryWord) - 1]
            segList.append(tryWord)
            line = line[len(tryWord):]
        self.write_file(segList, tf)


if __name__ == '__main__':
    fmm = FMM()
    fmm.tokenize()
