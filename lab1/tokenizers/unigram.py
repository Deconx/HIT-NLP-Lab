# -*- coding: gbk -*-
from math import log


class DynamicSearch:
    def __init__(self, dict):
        self.filename = dict
        self.lfreq = {}  # ����ǰ׺�ʵ�
        self.ltotal = 0  # �����ܵĴ���

    def search(self, sentence):
        """
        �ִ�
        :param sentence:
        :return: ·��
        """
        # ����ǰ׺�ʵ�
        self.gen_pfdict()
        DAG = self._get_DAG(sentence)
        route = {}
        self._clac(sentence, DAG, route)
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

    def _clac(self, sentence, DAG, route):
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
                (log(self.lfreq[sentence[idx:x + 1]] or 1) - logtotal + route[x + 1][0], x) for x in DAG[idx])


if __name__ == '__main__':
    d1 = DynamicSearch('../data/dict.txt')
    print(d1.search("��0 ��1 ��2 ��3 ��4 ��5 ��6 ��7 ��8 ��9 Ҫ10 ȥ11 ��12 ��13 ��14 ��15 ��16 ��17 ��18 ��19 ��20"))

