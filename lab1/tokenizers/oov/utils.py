# -*- coding: gbk -*-
from lab1.vocab.Vocab import Vocab

padding = ['#', '^', '_', '&']
v = Vocab()
patterns = v.get_pattern()


def IdDate(sentence):
    """
    ʹ�����򣬸��ݴ������ľ���ʶ�����ڵ�
    :param sentence:
    :return: ���������±��б�
    """
    # �õ��ʵ����õ�����ƥ�䴮
    data_list = []
    for pattern in patterns:
        l = pattern.finditer(sentence)
        # ����������Ӵʵ���
        for w in l:
            # ����ƥ�䵽���±�
            (i, j) = w.span()
            # print((i,j))
            # ��ֹ����ƥ����ȷ���
            if i == 0 and j > 19:
                data_list.append((20, j))
                j = 19
            data_list.append((i, j))
    return data_list


def IdDate_all(sentence):
    """
    ʹ�����򣬷��ؾ����ַ���
    :param sentence: ����ľ���
    :return: �����б�����ƥ��
    """
    pad_list = []
    i = 0
    for pattern in patterns:
        pad = padding[i]
        i += 1
        tmp = pattern.findall(sentence)
        # print(tmp)
        tmp_pad_list = []
        if tmp is None:
            pad_list.append(tmp_pad_list)
            continue
        for tuple_date in tmp:
            word = list(tuple_date)[0]
            if i == 2 and len(word) > 19:
                word = word[:19]
            old_sentence = sentence
            sentence = sentence.replace(word, pad, 1)
            # �滻�ɹ�
            if sentence != old_sentence:
                tmp_pad_list.append(word)
        pad_list.append(tmp_pad_list)
    pad_dict = {'#': pad_list[0], '^': pad_list[1], '_': pad_list[2], '&': pad_list[3]}
    # print(pad_list)
    return sentence, pad_dict


def decode(words, pad_dict):
    """
    ����#���ǵ�δ��¼�ʻ�ԭ
    :param words: ���Ǻ�ľ���
    :param words_cache: ����ǰ���ʻ���
    :return: ��
    """
    indexs = {'#': 0, '^': 0, '_': 0, '&': 0}
    for i in range(len(words)):
        if words[i] not in padding:
            continue
        pad = words[i]
        words[i] = pad_dict[pad][indexs[pad]]
        indexs[pad] += 1
