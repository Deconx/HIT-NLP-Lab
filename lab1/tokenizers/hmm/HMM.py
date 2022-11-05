# -*- coding: gbk -*-
import pickle

import tqdm

from lab1.tokenizers.fmm_bmm.MM import write_file
from lab1.tokenizers.oov.utils import begging_number

# ��Сֵ
MIN = -3.14e100
pre = {'B': 'ES', 'M': 'MB', 'S': 'SE', 'E': 'BM'}  # ��־���Գ����ڵ�ǰ״̬֮ǰ��״̬
states = ['B', 'M', 'E', 'S']  # ״̬��


class HMM:
    def __init__(self, model_path='../../data/hmm_model/h.pkl'):
        """
        ��ʼ��
        :param model_path: ģ�Ͳ����洢��ַ
        """
        # ��ʼ״̬�ֲ�
        self.pi = {}
        # ״̬ת�ƾ���
        self.A = {}
        # �������
        self.B = {}
        # ���ز���
        self.load_model(model_path)

    def viterbi(self, text):
        """
        viterbi�㷨
        :param text: ������ı�
        :return: ��ע
        """
        V = [{}]
        path = {}
        # ���п��ܵ���һ��״̬
        for y in states:
            V[0][y] = self.pi[y] + self.B[y].get(text[0], MIN)
            path[y] = [y]
        for t in range(1, len(text)):
            V.append({})
            newpath = {}
            for y in states:
                em_p = self.B[y].get(text[t], MIN)
                (prob, state) = max(
                    [(V[t - 1][y0] + self.A[y0].get(y, MIN) + em_p, y0) for y0 in pre[y]])
                V[t][y] = prob
                # ��һ������״̬+��һʱ��״̬
                newpath[y] = path[state] + [y]
            path = newpath

        (prob, state) = max((V[len(text) - 1][y], y) for y in 'ES')

        return prob, path[state]

    def merge(self, words):
        """
        �����ʴ�
        :param words: �����б�
        :return: �ִʽ��
        """
        if len(words) == 1:
            return words
        seg_list = self.viterbi(words)[1]
        res = ''
        for i in range(len(words)):
            tag = seg_list[i]
            if tag == 'B' or tag == 'M':
                res += words[i]
            elif tag == 'E' or tag == 'S':
                res += words[i] + '/'
        res = res.rstrip()
        res = res.split('/')[0:-1]
        return res

    def line_seg(self, word_list):
        """
        �Էִʽ�����еĵ��ֽ��кϲ�
        :param word_list: �ִʽ��
        :return: �ϲ���ķִʽ��
        """
        sentence_seg = []
        i = 0
        while i < len(word_list):
            tmp = []
            j = i
            while j < len(word_list) and len(word_list[j]) == 1:
                tmp.append(word_list[j])
                j += 1
            if len(tmp) > 0:
                sentence_seg.extend(self.merge(tmp))
            tmp.clear()
            i = j
            if i < len(word_list):
                sentence_seg.append(word_list[i])
            i += 1
        return sentence_seg

    def cut_sentence(self, sentence):
        """
        ����jieba�Ĵ��룬д�ıȽ�����
        :param sentence:
        :return:
        """
        global emit_P
        prob, pos_list = self.viterbi(sentence)
        begin, nexti = 0, 0
        # print pos_list, sentence
        for i, char in enumerate(sentence):
            pos = pos_list[i]
            if pos == 'B':
                begin = i
            elif pos == 'E':
                yield sentence[begin:i + 1]
                nexti = i + 1
            elif pos == 'S':
                yield char
                nexti = i + 1
        if nexti < len(sentence):
            yield sentence[nexti:]

    def tokenizer(self, data_file='../../data/origin_data_set/199801_sent.txt', target_file='../../data/test_output/seg_HMM.txt'):
        """
        ʹ��HMM���ı����зִ�
        :param target_file: ���ִ��ı�
        :param data_file: ���
        :param text_path: ��Ҫ�ִʵ��ı����ڵ�ַ
        :param io_path:�ִʽ�������ַ
        :return:
        """
        with open(data_file, encoding='gbk') as f:
            lines = f.readlines()
            tf = open(target_file, 'w')
            # f_words = []
            for line in tqdm.tqdm(lines):
                segList = []
                line = begging_number(line, segList)
                list_iter = self.cut_sentence(line)
                for i in list_iter:
                    segList.append(i)
                # print(segList)
                # print(f_words)
                write_file(segList, tf)
            f.close()
            tf.close()

    def load_model(self, model_path):
        """
        ����ģ�ͣ���ʼ��������������
        :param model_path: ģ�͵�ַ
        :return:
        """
        with open(model_path, "rb") as f:
            self.pi = pickle.load(f)
            self.A = pickle.load(f)
            self.B = pickle.load(f)
        f.close()


if __name__ == "__main__":
    hmm = HMM('../../data/hmm_model/h.pkl')
    hmm.tokenizer()
