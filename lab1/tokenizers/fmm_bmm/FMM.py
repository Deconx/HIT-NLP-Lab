# -*- coding: gbk -*-
import time

import tqdm

from lab1.tokenizers.fmm_bmm.MM import MM, write_file


class FMM(MM):
    def __init__(self, datatype='list', data_file='../../data/origin_data_set/199801_sent.txt', target_file='../../data/test_output/seg_FMM.txt'):
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
        # 先用正则匹配分出数字字母串
        l = self.pattern.finditer(line)
        # 先用正则添加词典中
        for w in l:
            # 正则匹配到的下标
            (i, j) = w.span()
            # 防止正则匹配过度泛化
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
        print(segList)
        write_file(segList, tf)


if __name__ == '__main__':
    fmm_list = FMM(datatype='list')
    fmm_set = FMM(datatype='set')

    f = open('TimeCost.txt', 'w')

    # 优化前耗时
    # time_begin = time.time()
    # fmm_list.tokenize()
    # time_end = time.time()
    # f.write(f'FMM：\n'
    #        f'优化前：{time_end - time_begin}s\n')

    time_begin = time.time()
    fmm_set.tokenize()
    time_end = time.time()
    f.write(f'优化后：{time_end - time_begin}s\n\n')
    f.close()
