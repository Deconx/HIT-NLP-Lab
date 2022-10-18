# -*- coding: gbk -*-
import re


class Vocab:
    def __init__(self, data_file='../data/199801_seg&pos.txt', target_file='../data/dict.txt'):
        self.data_file = data_file
        self.target_file = target_file
        # ���ִ�ͳһΪ<n>
        self.pad = '<n>'
        # ����ʵ�
        self.d = dict()
        # ����������ʽƥ�����ֺ�������е��ַ�
        self.s = set()
        # ��������ƥ�����
        self.pattern_numrate = re.compile(r'((��*(�ٷ�֮|��)?([��-��]+|[0-9]+|[����һ�����������߰˾�ʮ��]+|[��-��]+|[��-��]+|-)+([��ǧ����]?)['
                                          r'.������ã�]?([��-��]*|[0-9]*|[ '
                                          r'����һ�����������߰˾�ʮ]*)([��ǧ����]?)([����ǧ�ڸ�����])*)+)')

    def padding_words(self, word):
        """
        :param word: ����ĵ���
        :return: ���ݵ���ƥ��������ʽ�����ƥ��ɹ������滻Ϊpad
        """
        # 19980112-09-001-001
        # ��ĸ��
        # 51073
        # pattern_index = re.compile(r'((\d|-|��|��|��|[��-��]|��|[��-��]|[��-��]|��)+)')
        # ����
        # pattern_numrate = re.compile(r'((��?(�ٷ�֮|��)?([��-��]+|[0-9]+|[����һ�����������߰˾�ʮ��]+)([��ǧ����]?)[.������]?([��-��]+|[0-9]+|['
        #                             r'����һ�����������߰˾�ʮ]+)([��ǧ����]?)([����ǧ�ڸ�����])*)+)|((\d|-|��|��|��|[��-��]|��|[��-��]|[��-��]|��)+)')
        # pattern_sentence = re.compile(r'')

        # ��ΪPython��������̫���ˣ�ֻ������
        m = self.pattern_numrate.match(word)
        if m is not None:
            # print(m.group(0))
            # print(m.span(0))
            index = m.span()
            # print(index)
            # ��ȫƥ��
            if index[1] == len(word):
                print(word)
                # ��word�滻Ϊpad
                word = self.pad
        return word

    def make_vocab(self):
        """
        :return: ����dict.txt
        """
        with open(self.data_file, encoding='gbk') as f:
            lines = f.readlines()
            # ���ո�ָ�
            for line in lines:
                if line is None:
                    continue
                word_list = line.split()
                for word in word_list:
                    # word.replace('[', '') �޷������滻
                    if word[0] == '[':
                        new_word = word[1:]
                        word = new_word
                    word.replace(']', '')
                    # print(word)
                    w = word.split('/')
                    single_word = w[0]
                    single_word = self.padding_words(single_word)

                    if single_word not in self.d:
                        self.d[single_word] = 1
                    else:
                        self.d[single_word] += 1
            f.close()

        with open(self.target_file, 'w', encoding='gbk') as f:
            words = get_sorted_list(self.d)
            for word in words:
                f.write(word[0])
                f.write('\t')
                f.write(str(word[1]))
                if word is not words[-1]:
                    f.write('\n')
            f.close()

    def get_paddedwords(self):
        """
        :return: ���ر�padding���Ŀ��ܵ��ַ�
        """
        return self.s.copy()

    def get_pattern(self):
        """
        :return: ������ĸ�����õ��������
        """
        return self.pattern_numrate


def get_sorted_list(dict_in, reverse=False):
    """
    ���ʵĴ�С����
    :param dict_in: �ʵ�
    :param reverse: False Ϊ����TrueΪ����
    :return: ����õ��б�
    """
    return sorted(dict_in.items(), key=lambda x: len(x[0]), reverse=reverse)


if __name__ == '__main__':
    vocab = Vocab()
    vocab.make_vocab()
