# -*- coding: gbk -*-
import time

import tqdm

from lab1.tokenizers.MM import MM, write_file


class FMM(MM):
    def __init__(self, datatype='list', data_file='../data/199801_sent.txt', target_file='../data/seg_FMM.txt'):
        super().__init__(datatype=datatype)
        self.data_file = data_file
        self.target_file = target_file

    def tokenize(self):
        with open(self.data_file) as f:
            lines = f.readlines()
            tf = open(self.target_file, 'w')
            for line in tqdm.tqdm(lines):
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
            # ��ֹ����ƥ����ȷ���
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
            tryWord = line[0:length]
            while tryWord not in self.vocabData:
                if len(tryWord) == 1:
                    break
                tryWord = tryWord[0:len(tryWord) - 1]
            segList.append(tryWord)
            line = line[len(tryWord):]
        print(segList)
        write_file(segList, tf)


if __name__ == '__main__':
    fmm_list = FMM(datatype='list')
    fmm_set = FMM(datatype='set')

    f = open('./TimeCost.txt', 'w')

    # �Ż�ǰ��ʱ
    #time_begin = time.time()
    #fmm_list.tokenize()
    #time_end = time.time()
    #f.write(f'FMM��\n'
    #        f'�Ż�ǰ��{time_end - time_begin}s\n')

    time_begin = time.time()
    fmm_set.tokenize()
    time_end = time.time()
    f.write(f'�Ż���{time_end - time_begin}s\n\n')
    f.close()
