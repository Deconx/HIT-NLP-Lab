# -*- coding: gbk -*-
from lab1.tokenizers.oov.utils import IdDate_all
from lab1.tokenizers.fmm_bmm.MM import write_file
from lab1.tokenizers.oov.utils import decode
from lab1.scores import get_score
from unigram import Unigram
from math import log
import tqdm


def bi_calc(words, pre_graph, follow_graph, route):
    for word in words:
        if word == '<BOS>':
            route[word] = (0.0, '<BOS>')
        else:
            if word in follow_graph:
                nodes = follow_graph[word]
            else:
                route[word] = (-100000, '<BOS>')
                continue
            route[word] = max((pre_graph[node][word] + route[node][0], node) for node in nodes)


class Bigram(Unigram):
    def __init__(self, uni_dict, bi_dict):
        # һԪǰ׺�ʵ䣺lfreq, ������ltoal
        super().__init__(uni_dict)
        self.filename = bi_dict
        # �����Ԫǰ׺�ʵ�
        self.bi_lfreq = {}
        # ���ɶ�Ԫ�ʵ�
        self.gen_bi_pfdict()

    def gen_bi_pfdict(self):
        """
        ����ǰ׺�ʵ�
        :param filename: �ʵ�
        :return: ��Ƶ������
        """
        with open(self.filename, encoding='gbk') as fp:
            line = fp.readline()
            while len(line) > 0:
                word1, word2, freq = line.strip().split()[0:3]
                freq = int(freq)
                if word2 not in self.bi_lfreq:
                    self.bi_lfreq[word2] = {word1: freq}
                else:
                    self.bi_lfreq[word2][word1] = freq
                line = fp.readline()

    def log_p(self, words):
        """
        ���� log(w_1 | w_2)
        :param words: ��ԪԪ�飬��������
        :return: ���� log(w_1 | w_2)
        """
        assert len(words) == 2
        (w1, w2) = words
        p_w1 = 0.01 if w1 not in self.lfreq else self.lfreq[w1]
        p_w12 = 0.01 if w2 not in self.bi_lfreq or w1 not in self.bi_lfreq[w2] else self.bi_lfreq[w2][w1]
        p_w1 += 0.01
        p_w12 += 0.01
        return log(p_w12) - log(p_w1)

    def search(self, sentence):
        """
        �ִ�
        :param sentence:
        :return: ·��
        """
        # δ��¼�ʣ��������ִ�
        # �ĸ��ȼ���, �滻
        sentence, pad_dict = IdDate_all(sentence)

        # ���뿪ͷ����β
        sentence = '<BOS>' + sentence + '<EOS>'
        # ����DAGͼ���� Unigram ����ͬ
        # print(sentence)
        DAG = self._get_DAG(sentence)
        # print(DAG)
        pre_graph = {}
        pre_graph['<BOS>'] = {}
        follow_graph = {}
        # ȥ��<BOS>�ĵ�һ����
        for x in DAG[5]:
            pre_graph['<BOS>'][(5, x + 1)] = self.log_p(("<BOS>", sentence[5:x + 1]))
        # print(pre_graph['<BOS>'])
        # ��ÿһ���ֿ��ܵķִʷ�ʽ������һ���ʵĴʵ�
        n = len('<BOS>')
        while n < (len(sentence) - len('<EOS>')):
            i = DAG[n]
            for x in i:
                pre = sentence[n:x + 1]
                current = x + 1
                current_idx = DAG[x + 1]
                temp = {}
                for char_i in current_idx:
                    word = sentence[current:char_i + 1]
                    # <EOS> ���⴦��
                    if word == "<":
                        temp['<EOS>'] = self.log_p((pre, '<EOS>'))
                    else:
                        temp[(current, char_i + 1)] = self.log_p((pre, word))
                pre_graph[(n, x + 1)] = temp
            n += 1

        words = list(pre_graph.keys())
        for pre in words:
            for word in pre_graph[pre].keys():  # ����pre_word�ĺ�һ����
                follow_graph[word] = follow_graph.get(word, list())
                follow_graph[word].append(pre)
        words.append('<EOS>')

        route = {}
        bi_calc(words, pre_graph, follow_graph, route)
        sentence_words = []
        idx = "<EOS>"
        while idx != '<BOS>':
            idx = route[idx][1]
            if idx != '<BOS>':
                (i, j) = idx
                sentence_words.insert(0, sentence[i:j])
        # print(sentence_words)
        # ��pad��ԭ
        decode(sentence_words, pad_dict)
        # print(sentence_words)
        return sentence_words

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
                segList = self.search(line)
                # print(segList)
                write_file(segList, tf)
            f.close()
            tf.close()


if __name__ == '__main__':
    bi = Bigram('../../data/dict.txt', '../../data/bi_dict.txt')
    # bi.search("19980101-01-001-004�����£����գ��й���������ǡ�������ϯ�����񷢱������������꽲�����������ϣ���������͡������»�����ߺ���㣩")
    # bi.tokenize('../../data/199801_sent.txt', '../../data/seg_Bigram.txt')
    bi.tokenize('../../data/test_in.txt', '../../data/seg_test.txt')
    # print(get_score('../../data/199801_seg&pos.txt', '../../data/seg_Bigram.txt'))
