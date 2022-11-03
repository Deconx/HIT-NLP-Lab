# HIT-NLP-Lab

哈工大 2022 秋季学期《自然语言处理》课程实验

## 实验一：汉语分词系统

项目结构：
```
├── data
|  ├── 199801_seg&pos.txt
|  ├── 199801_sent.txt
|  ├── 199802.txt
|  ├── 199803.txt
|  ├── dict.txt
|  ├── name.txt
|  ├── seg_BMM.txt
|  ├── seg_FMM.txt
|  └── seg_Unigram.txt
├── score.txt
├── scores.py
├── tokenizers
|  ├── fmm_bmm
|  ├── ngram
|  └── oov
└── vocab
|  ├── Vocab.py
|  └── VocabData.py
```
- `data`：文件夹存放语料库，标准分词结果和构建的词典

- `vocab`包：用于从语料库中读出词典和构建词典数据结构
  - `Vocab.py`：从语料库中分出词典，生成`dict.txt`文件存放在`data`文件夹中
  - `VocabData.py`：构建词典数据结构，支持插入和搜索操作。我这里实现了两种实现类，`VocabList`使用**列表**实现，`VocabSet`使用**哈希表**实现
- `tokenizers`包：用于分词
  - `BMM.py`：**反向最大匹配分词**实现，分词结果生成`seg_BMM.txt`文件存放在`data`文件夹中
  - `FMM.py`：**正向最大匹配分词**实现，分词结果生成`seg_FMM.txt`文件存放在`data`文件夹中
  - 此外，分词时还会记录分词所耗费的时间，结果保存在同级目录下的`TimeCost.txt`中
- `scores.py`：对分词算法的结果进行评价，分别计算**准确率**，**召回率**和 **F-评价**，结果生成`score.txt`文件