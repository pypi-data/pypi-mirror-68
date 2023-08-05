## LAC的Python调用

### 安装说明
代码兼容Python2/3
- 全自动安装: `pip install lac`
- 半自动下载：先下载[http://pypi.python.org/pypi/lac/](http://pypi.python.org/pypi/lac/) ，解压后运行 `python setup.py install`

### 功能与使用
#### 分词
- 代码示例：
```python
from LAC import LAC

# 装载分词模型
lac = LAC(mode='seg')

# 单个样本输入，输入为Unicode编码的字符串
text = u"LAC是个优秀的分词工具"
seg_result = lac.run(text)

# 批量样本输入, 输入为多个句子组成的list，速率会更快
texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司"]
seg_result = lac.run(texts)
```
- 输出：

```text
【单样本】：seg_result = [LAC, 是, 个, 优秀, 的, 分词, 工具]
【批量样本】：seg_result = [[LAC, 是, 个, 优秀, 的, 分词, 工具], [百度, 是, 一家, 高科技, 公司]]
```

#### 词性标注与实体识别
- 代码示例：
```python
from LAC import LAC

# 装载LAC模型
lac = LAC(mode='lac')

# 单个样本输入，输入为Unicode编码的字符串
text = u"LAC是个优秀的分词工具"
lac_result = lac.run(text)

# 批量样本输入, 输入为多个句子组成的list，平均速率更快
texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司"]
lac_result = lac.run(texts)
```
- 输出：

>每个句子的输出其切词结果word_list以及对每个单词的标注tags_list，其格式为（word_list, tags_list)
```text
【单样本】： seg_result = ([百度, 是, 一家, 高科技, 公司], [ORG, v, m, n, n])
【批量样本】：seg_result = [
                    ([百度, 是, 一家, 高科技, 公司], [ORG, v, m, n, n]),
                    ([LAC, 是, 个, 优秀, 的, 分词, 工具], [nr, v, q, a, u, n, n])
                ]
```

词性和专名类别标签集合如下表，其中我们将最常用的4个专名类别标记为大写的形式。

| 标签 | 含义     | 标签 | 含义     | 标签 | 含义     | 标签 | 含义     |
| ---- | -------- | ---- | -------- | ---- | -------- | ---- | -------- |
| n    | 普通名词 | f    | 方位名词 | s    | 处所名词  | nw   | 作品名   |
| nz   | 其他专名 | v    | 普通动词 | vd   | 动副词   | vn   | 名动词   |
| a    | 形容词   | ad   | 副形词   | an   | 名形词   | d    | 副词     |
| m    | 数量词   | q    | 量词     | r    | 代词     | p    | 介词     |
| c    | 连词     | u    | 助词     | xc   | 其他虚词 | w    | 标点符号 |
| PER  | 人名     | LOC  | 地名     | ORG  | 机构名   | TIME | 时间     |

#### 模型干预
- 干预文件custom.txt示例
> 字典文件可同时设置单词及其标注，并且支持多个词组成的短语片段，使得干预更为精准。
```text
一/m 家/r
高科技公司
```
- 代码示例
```python
from LAC import LAC
lac = lac()

# 输入示例
text = u"百度是一家高科技公司"

干预前结果
origin_result = lac.run(text)


# 装载干预词典
lac.load_customization('custom.txt')
"""custom.txt
一/m 家/r
高科技公司
"""

# 干预后结果
custom_result = lac.run(text)
```

- 输出：
> 因为干预词典中包含，“一家”、“高科技公司”这两个词，装载干预词典后，模型预测结果变化如下所示：
```text
origin_result = ([百度, 是, 一家, 高科技, 公司], [ORG, v, m, n, n])
custom_result = ([百度, 是, 一, 家, 高科技公司], [ORG, v, m, r, n])
```
- 干预词典说明
每行表示一个干预的item，由一个单词或多个连续的单词组成，每个单词后使用'/'表示标签，如果没有'/'则表示使用模型默认的标签。每个item单词数越多，干预效果会越精准。


#### 增量训练
针对用户自己提供的数据，进行增量训练，首先需要将数据转换为输入的格式，样例可参考：https://baidu-nlp.bj.bcebos.com/lexical_analysis-dataset-2.0.0.tar.gz

- 代码示例
```python
from LAC import LAC
LAC = LAC()

# 训练和测试数据集
train_file = "./data/train.tsv"
test_file = "./data/test.tsv"
lac.train(model_save_dir='./my_model/',train_data=train_file, test_data=test_file)

# 使用自己训练好的模型
my_lac = LAC(model_path='my_model')
```
