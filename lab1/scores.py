# -*- coding: gbk -*-
CHECK_FILE = './data/199801_seg&pos.txt'
BMM_FILE = './data/seg_BMM.txt'
FMM_FILE = './data/seg_FMM.txt'


def get_num(data_file):
    """
    �õ�ĳ�ļ��зִ�����
    :return: �ļ��зִ�����
    """
    f = open(data_file)
    s = f.read()
    return s.count('/')


def get_wordstr(line):
    """
    ���ļ���һ�仰�ָ�Ϊ�����б�
    """
    words = []
    word_list = line.split()
    for word in word_list:
        # word.replace('[', '') �޷������滻
        if word[0] == '[':
            new_word = word[1:]
            word = new_word
        word.replace(']', '')
        # print(word)
        w = word.split('/')
        words.append(w[0])
    return words


def word2inval(words):
    """
    ���ִ�ת��Ϊ��Ӧλ�õ�����
    """
    inval = []
    start = 0
    for word in words:
        end = start + len(word)
        inval.append((start, end))
        start = end
    return inval


def get_check(test_file, data_file):
    """
    �õ���ȷ�ִ�����
    :return: ��ȷ�ִ�����
    """
    tf = open(test_file)
    df = open(data_file)
    t_lines = tf.readlines()
    d_lines = df.readlines()
    # �ִʸ���
    count = 0
    for t_line, d_line in zip(t_lines, d_lines):
        t_words = get_wordstr(t_line)
        d_words = get_wordstr(d_line)
        # print(t_words)
        # print(d_words)
        t_inval = word2inval(t_words)
        d_inval = word2inval(d_words)
        # print(t_inval)
        # print(d_inval)
        # ���ڲ���ʹ�ü����󽻼����������￼�Ǳ���ö��
        # ע�⣺����������Ѵ�ת�����˹���λ�õ�Ԫ���ʾ��ǰ����ͬ�ĵ��ʵı�ʾ�ǲ�ͬ�ģ��������󽻼��İ취�ǿ��е�
        for t in t_inval:
            for d in d_inval:
                if t == d:
                    count += 1
                    break
    return count


if __name__ == '__main__':
    BMM_right_num = get_check(CHECK_FILE, BMM_FILE)
    BMM_pre_num = get_num(BMM_FILE)
    FMM_right_num = get_check(CHECK_FILE, FMM_FILE)
    FMM_pre_num = get_num(FMM_FILE)
    CHECK_num = get_num(CHECK_FILE)

    f = open('./score.txt', 'w')
    BMM_P = float(BMM_right_num) / float(BMM_pre_num)
    BMM_R = float(BMM_right_num) / float(CHECK_num)

    FMM_P = float(FMM_right_num) / float(FMM_pre_num)
    FMM_R = float(FMM_right_num) / float(CHECK_num)
    f.write(f'FMM��\n׼ȷ�ʣ�{FMM_P}\n'
            f'�ٻ��ʣ�{FMM_R}\n'
            f'F-���ۣ�{2 * FMM_P * FMM_R / (FMM_R + FMM_P)}\n\n'
            f'BMM��\n׼ȷ�ʣ�{BMM_P}\n'
            f'�ٻ��ʣ�{BMM_R}\n'
            f'F-���ۣ�{2 * BMM_P * BMM_R / (BMM_R + BMM_P)}')
    f.close()

