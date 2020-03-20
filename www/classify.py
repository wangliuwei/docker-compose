import random
import functools
from ml_logging import setup_logging


setup_logging(__name__)


def read_from_file(file_name, dimension_num, split_char):
    '''从文件读取数据
       file_name: 数据源文件名
       dimension_num: 选择的数据维度数量
       split_char: 数据分隔符
    '''
    def list_to_float(
            line, dimension_num=dimension_num, split_char=split_char):
        l = [float(x) for x in line.replace("\n", "").split(
            split_char)[:dimension_num]]
        return l

    try:
        with open(file_name, 'r') as data:
            # 若每行数据源为a1 a2 a3
            # 返回格式为float数值
            # [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]
            dataset = [list_to_float(x) for x in data]
    except IOError:
        pass
    return dataset


def cluster_random(dataset, chuster_num):
    '''随机选择质点
       dataset: 数据源
       chuster_num: 质点数量
    '''
    return random.sample(dataset, chuster_num)


def cal_distance(a, b):
    '''计算两个数据源之间的欧几里得距离
       dataset: 数据源
       chuster_num: 质点数量
    '''
    return functools.reduce(
        lambda x, y: x+y, [(x - y) ** 2 for x, y in zip(a, b)]) ** 0.5


def cal_multi(cluster_list, dataset):
    '''把每一个点分到最近的质心，返回分组后的情况
       cluster_list: 质心列表
       dataset: 数据源
    '''
    di = {}
    for i in dataset:
        ans = list(map(lambda x: cal_distance(i, x), cluster_list))
        cluster_index = ans.index(min(ans))
        di.setdefault(cluster_index, []).append(i)
        # di返回的格式应该如下：
        # di = {
        #          1: [[a1, a2], [c1, c2]],
        #          2: [[b1, b2], [d1, d2]]
        #      }
    return di


def new_cluster(cluster_dict):
    '''获取新的聚簇点
       cluster_dict: 包含分组信息的字典
    '''
    def average(nums):
        return sum(nums)/len(nums)

    return list(
        map(lambda x: (average(n) for n in zip(*x.values())), cluster_dict))


def main(file_name, dimension_num, split_char, k):
    # 读取数据
    dataset = read_from_file(file_name, dimension_num, split_char)
    # 选择初始的k个质点
    cluster_list = cluster_random(dataset, k)
    # 这是第一次分组
    cluster_before = False
    # 默认分组为空
    cluster_dict = {}
    while 1:
        if cluster_before:
            # 根据现有分组情况计算新的质心
            new_cluster(cluster_dict)
        else:
            cur_dict = cal_multi(cluster_list, dataset)
            cluster_before = True
            if cur_dict == cluster_dict:
                break
            else:
                cluster_dict = cur_dict