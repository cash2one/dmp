#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
'''
日志的封装
'''
import logging
import logging.config
import os
import config


logger = None
conf = config.get_config()
__all__ = ['get_logger']


def get_logger():
    global logger

    if logger is None:
        # 只要文件夹名
        log_path = conf.get('log', 'dir')
        cur_path = os.path.abspath(os.path.dirname(__file__))
        log_path = os.path.join(cur_path, '..', log_path)
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        filename = conf.get('log', 'file')
        filename = os.path.join(log_path, filename)

        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s|%(lineno)d %(message)s')
        file_handler.setFormatter(formatter)

        logger = logging.getLogger('dmp')
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

    return logger


if __name__ == '__main__':
    l = get_logger()
    l.info('test log')
