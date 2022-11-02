# -*- coding: gbk -*-
from lab1.vocab.Vocab import Vocab


def IdDate(sentence):
    """
    ʹ�����򣬸��ݴ������ľ���ʶ�����ڵ�
    :param sentence:
    :return: ���������±��б�
    """
    # �õ��ʵ����õ�����ƥ�䴮
    v = Vocab()
    patterns = v.get_pattern()
    data_list = []
    for pattern in patterns:
        l = pattern.finditer(sentence)
        # ����������Ӵʵ���
        for w in l:
            # ����ƥ�䵽���±�
            (i, j) = w.span()
            # ��ֹ����ƥ����ȷ���
            if i == 0 and j > 19:
                data_list.append((20, j))
                j = 19
            data_list.append((i, j))
    return data_list
