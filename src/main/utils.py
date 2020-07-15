# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/4/29 18:14
@File      : utils.py
@Version   : 1.0
@Description: 
"""
import configparser
import logging
from six import PY3
import os
config = configparser.ConfigParser()
fp_dir = os.getcwd() #取得的是exe文件路径
path = os.path.join(fp_dir, "config.ini") #拼接上配置文件名称目录
def read_config_key(section, key):
    # config.read(os.path.dirname(__file__) + '\\config.ini')
    config.read(path)
    return config[section][key]

def write_config_key(section, key, value):
    config[section][key] = value
    # with open(os.path.dirname(__file__) + '\\config.ini', 'w') as configfile:  # save
    with open(path, 'w') as configfile:  # save
        config.write(configfile)

def get_default_logger(name):
    """Get a logger from default logging manager. If no handler
    is associated, add a default NullHandler"""

    logger = logging.getLogger(name)
    if not logger_has_handlers(logger):
        # If logging is not configured in the current project, configure
        # this logger to discard all logs messages. This will prevent
        # the 'No handlers could be found for logger XXX' error on Python 2,
        # and avoid redirecting errors to the default 'lastResort'
        # StreamHandler on Python 3
        logger.addHandler(logging.NullHandler())
    return logger

# Additional log methods
def logger_has_handlers(logger):
    """Since Python 2 doesn't provide Logger.hasHandlers(), we have to
    perform the lookup by ourself."""

    if PY3:
        return logger.hasHandlers()
    else:
        c = logger
        rv = False
        while c:
            if c.handlers:
                rv = True
                break
            if not c.propagate:
                break
            else:
                c = c.parent
        return rv

if __name__ == '__main__':
    read_config_key("USER", "password")
    write_config_key("USER", "password", "3")