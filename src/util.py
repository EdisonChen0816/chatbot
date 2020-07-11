# encoding=utf-8
import os
import re


def load_data_from_dir(path):
    for dir_path, dir_names, file_names in os.walk(path):
        for file in file_names:
            full_path = os.path.join(dir_path, file)
            for line in open(full_path, encoding='UTF-8'):
                yield line.strip().split("\t")


def remove_punctuation(query):
    # 去掉标点
    punctuation = "[\s+\.\!\?\/_,$%(+\"\']+|[+——！，。？、~@#￥%……&（）]+"  # 去掉标点
    return re.sub(punctuation, '', query)