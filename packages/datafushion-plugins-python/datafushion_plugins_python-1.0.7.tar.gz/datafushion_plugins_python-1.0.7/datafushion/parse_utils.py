#  Copyright (c) XiaoLinpeng 2020.

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   parse_utils.py
@Contact :   1553990434@qq.com
@License :   (C)Copyright 2019-Present, XiaoLinpeng

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-04-08 22:09   肖林朋      1.0         不同格式文件解析
"""
import json
from datafushion.args import FileExtractFormatEnum


def parse_file_2_map_list(file_path, file_type):
    if file_type == FileExtractFormatEnum.CSV.value:
        return __parse_sv_file_2_map_list(file_path, ',')
    elif file_type == FileExtractFormatEnum.TSV.value:
        return __parse_sv_file_2_map_list(file_path, '\t')
    elif file_type == FileExtractFormatEnum.JSON.value:
        return __parse_json_2_map_list(file_path)
    elif file_type == FileExtractFormatEnum.GENERAL.value:
        return __parse_general_file_2_map_list(file_path)


def __parse_sv_file_2_map_list(file_path, separator):
    """
    解析Csv文件至MapList形式
    :param file_path:CSV文件路径
    :return: 数据的MapList
    """
    res = []
    index_columns_map = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        read_lines = f.read().splitlines()
        columns = read_lines.pop(0)
        split = columns.split(separator)
        for index, value in enumerate(split):
            index_columns_map[index] = value
        for item in read_lines:
            columns = item.split(separator)
            item_map = {}
            for k, v in index_columns_map.items():
                item_map[v] = columns[k]
            res.append(item_map)

    return res


def __parse_json_2_map_list(file_path):
    """
    解析Json文件至MapList形式
    :param file_path:JSON文件路径
    :return: 数据的MapList
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith("[") and content.endswith("]"):
            res = json.loads(content)
        else:
            trans = "[" + content + "]"
            res = json.loads(trans)

    return res


def __parse_general_file_2_map_list(file_path):
    """
        解析普通文件至MapList形式
        :param file_path:JSON文件路径
        :return: 数据的MapList
        """
    res = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        content_map = {
            'value': content
        }
        res.append(content_map)
    return res
