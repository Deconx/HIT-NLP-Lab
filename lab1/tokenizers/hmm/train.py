# -*- coding: gbk -*-
import pickle
import re
from math import log
import tqdm

pre = {'B': 'ES', 'M': 'MB', 'S': 'SE', 'E': 'BM'}  # ��־���Գ����ڵ�ǰ״̬֮ǰ��״̬
states = ['B', 'M', 'E', 'S']  # ״̬��
date_pattern = '[0-9]*[-][0-9]*[-][0-9]{3}[-][0-9]{3}'


class train():
    """
    ʹ��EM�㷨��HMM�Ĳ�������ѵ��
    """

    def __init__(self):
        self.pi = {}  # ��ʼ״̬��
        self.A = {}  # ״̬ת�Ƹ���
        self.B = {}  # �������
        self.line_num = 0  # ͳ�ƾ�����
        self.word_dic = set()  # ������ֹ��Ĵ�
        self.state_num = {}  # ��¼ÿһ��״̬���ֵĴ���
        for state in states:
            self.state_num[state] = 0.0
            self.pi[state] = 0.0
            self.A[state] = {}
            self.B[state] = {}
            for temp_state in states:
                self.A[state][temp_state] = 0.0  # state->temp_state��ת�Ƹ��ʳ�ʼ��

    def write_res(self, save_model_path):
        """
        ����ѵ���õ��Ĳ���
        :param save_model_path:�����ַ
        :return:
        """
        with open(save_model_path, "wb") as f:
            pickle.dump(self.pi, f)
            pickle.dump(self.A, f)
            pickle.dump(self.B, f)
        f.close()

    def tag_line(self, line):
        """
        ��һ���ı���ע������һ����ÿһ���ֶ�Ӧ��[B,M,E,S]
        :param line:��Ҫ��ע���ı�
        :return:��ע���
        """
        line_word = []
        line_tag = []
        for word in line.split():
            word = word[1 if word[0] == '[' else 0:word.index('/')]
            self.line_num += 1
            if len(word) == 0:
                continue
            if word[-1] == ']':
                word = word[0:-1]

            line_word.extend(list(word))
            self.word_dic.add(word)
            # �Ծ���״̬���м�¼
            if len(word) == 1:
                self.pi['S'] += 1
                line_tag.append('S')
            else:
                self.pi['B'] += 1
                self.pi['E'] += 1
                self.pi['M'] += len(word) - 2
                line_tag.append('B')
                line_tag.extend(['M'] * (len(word) - 2))
                line_tag.append('E')
        assert len(line_tag) == len(line_word)
        return line_word, line_tag

    def tag_text(self, res_path, train_file=None):

        if train_file is None:
            train_file = ['../../data/199801_seg&pos.txt', '../../data/199802.txt', '../../data/199803.txt',
                          '../../data/name_pre.txt']

        assert train_file is not None

        for file in train_file:
            with open(file, encoding='gbk', errors='ignore') as f:
                lines = f.readlines()
                for line in tqdm.tqdm(lines):
                    if line is None or line == '\n':
                        continue
                    line = re.sub(date_pattern, '', line)
                    word,tag = self.tag_line(line)
                    # print(word)
                    # print(tag)
                    for i in range(len(tag)):
                        self.state_num[tag[i]] += 1
                        self.B[tag[i]][word[i]] = self.B[tag[i]].get(word[i], 0) + 1  # �������
                        # print(self.B[tag[i]].get(word[i], 0))
                        if i > 0:  # ת�Ƹ���
                            self.A[tag[i - 1]][tag[i]] += 1
                f.close()

        # ���²���
        for state in states:
            a = 0.00001
            # ����״̬
            self.pi[state] = log((self.pi[state] + a) / (self.line_num + a * 4))
            for temp_state in states:
                self.A[state][temp_state] = log((self.A[state][temp_state] + a) / (self.state_num[state] + a * 4))
            for word in self.B[state].keys():
                self.B[state][word] = log((self.B[state][word] + a) / (self.state_num[state] + a * len(self.word_dic)))
        self.write_res(res_path)


if __name__ == '__main__':
    h1 = train()
    h1.tag_text('../../data/h.pkl')
    print(h1.pi)
    print(h1.A)
    print(h1.B)
