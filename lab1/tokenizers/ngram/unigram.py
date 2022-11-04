# -*- coding: gbk -*-
from math import log

import tqdm

from lab1.tokenizers.oov.utils import IdDate
from lab1.scores import get_score
from lab1.tokenizers.fmm_bmm.MM import write_file


def IdDate_route(line, route):
    """
    �滻route
    :param line:
    :param route:
    :return:
    """
    data_idx = IdDate(line)
    # ����δ��¼�ʱ��޸�·��
    # ������㷨���ܲ�̫�ã�������Ҫ�Ľ� TODO
    for (i, j) in data_idx:
        # print((i, j))
        for ii in range(i, j - 1):
            # �������ʵ��յ㶼�ĳ�j
            # tupleֻ�ɶ�����д
            route[ii] = (route[ii][0], j - 1)
    return route


class Unigram:
    def __init__(self, dict):
        self.filename = dict
        self.lfreq = {}  # ����ǰ׺�ʵ�
        self.ltotal = 0  # �����ܵĴ���
        # ����ǰ׺�ʵ�
        self.gen_pfdict()

    def search(self, sentence):
        """
        �ִ�
        :param sentence:
        :return: ·��
        """
        DAG = self._get_DAG(sentence)
        route = {}
        self._calc(sentence, DAG, route)
        return route

    def gen_pfdict(self):
        """
        ����ǰ׺�ʵ�
        :param filename: �ʵ�
        :return: ��Ƶ������
        """
        with open(self.filename, encoding='gbk') as fp:
            line = fp.readline()
            while len(line) > 0:
                word, freq = line.strip().split()[0:2]
                freq = int(freq)
                self.lfreq[word] = freq
                self.ltotal += freq
                # �������ߴʵ��ÿ���ʣ���ȡ��ǰ׺��
                for ch in range(len(word)):
                    wfrag = word[:ch + 1]
                    if wfrag not in self.lfreq:
                        self.lfreq[wfrag] = 0
                line = fp.readline()

    def _get_DAG(self, sentence):
        """
        ����DAGͼ
        :param sentence: Ŀ�����
        :param lfreq: ǰ׺��Ƶ
        :return: DAGͼ
        """
        DAG = {}
        N = len(sentence)
        for k in range(N):
            tmplist = []
            i = k
            frag = sentence[k]
            while i < N and frag in self.lfreq:
                if self.lfreq[frag] > 0:
                    tmplist.append(i)
                i += 1
                frag = sentence[k:i + 1]
            if not tmplist:
                tmplist.append(k)
            DAG[k] = tmplist
        return DAG

    def _calc(self, sentence, DAG, route):
        """
        ��̬�滮����
        :param sentence: ����
        :param DAG: ���ɵ�DAGͼ
        :param route: ��̬�滮·��
        :param lfreq: ǰ׺��Ƶ
        :param ltotal: �ܴ���
        """
        N = len(sentence)
        route[N] = (0, 0)
        logtotal = log(self.ltotal)
        for idx in range(N - 1, -1, -1):
            route[idx] = max(
                (log(1 or self.lfreq[sentence[idx:x + 1]]) - logtotal + route[x + 1][0], x) for x in DAG[idx])

    def tokenize(self, data_file, target_file):
        """
        ���շִʳ���
        :param data_file: ���ִʵ��ı�
        :param target_file: �ִʽ������Ŀ���ı�
        """
        with open(data_file) as f:
            lines = f.readlines()
            tf = open(target_file, 'w')
            for line in tqdm.tqdm(lines):
                segList = []
                route = self.search(line)
                # δ��¼��ʶ�����ڣ����ִ���
                IdDate_route(line, route)
                # print(route)
                i = 0
                while i < len(line):
                    segList.append(line[i:route[i][1] + 1])
                    i = route[i][1] + 1
                write_file(segList, tf)
            f.close()
            tf.close()


if __name__ == '__main__':
    d1 = Unigram('../../data/dict.txt')
    d1.tokenize('../../data/199801_sent.txt', '../../data/seg_Unigram.txt')
    print(get_score('../../data/199801_seg&pos.txt', '../../data/seg_Unigram.txt'))
    print(get_score('../../data/199801_seg&pos.txt', '../../data/seg_Bigram.txt'))
